"""ASSEMBLE pass: turn generated documents into the two views that matter.

``assemble_submission`` composes ``ossicro.pipeline.run_check`` (it never
re-implements or weakens a check, and it never clears a gate) and produces:

- the **FDA reviewer's view**: the eCTD module map, the cover letter, and a
  SHA-256 hash-manifest of every FDA-facing document (HC4 provenance substrate);
- the **manufacturer's view**: the LOA-request the physician sends and a short
  cover note — the manufacturer acts on a request, not on a filing;
- ``submission_ready`` + ``blocking``: the package is ready for the physician to
  review, sign, and file only when no FDA-facing document is red (missing content
  or failed validation). Pending non-delegable gates (amber) are surfaced
  separately in the check's gate packet — they are human acts at/after filing,
  not documentation gaps, and OSSICRO never clears them.

Nothing here files, signs, supplies, or approves. It assembles and validates.
"""

from __future__ import annotations

import datetime
import hashlib
from typing import Any, Dict, List, Optional

from .check import ledger_totals
from .ea_generators import compute_clocks, derive_as_of
from .models import Document, Gate, Study
from .pipeline import CheckResult, run_check
from .review_port import ConceptReviewer


def _sha256(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def _package_digest(doc_hashes: List[str]) -> str:
    """Package-level digest: SHA-256 over the sorted per-document hashes,
    newline-joined. Order-independent, so the same document set always yields
    the same digest regardless of route ordering."""
    return hashlib.sha256("\n".join(sorted(doc_hashes)).encode("utf-8")).hexdigest()


def assemble_submission(
    study: Study,
    documents: Dict[str, Document],
    route: Dict[str, Any],
    doc_registry: Dict[str, dict],
    gate_registry: Dict[str, Gate],
    reviewer: Optional[ConceptReviewer] = None,
    check: Optional[CheckResult] = None,
    as_of: Optional[datetime.date] = None,
) -> Dict[str, Any]:
    """Assemble the reviewer package and the manufacturer packet for a route.

    Concept integrity: pass either the ``reviewer`` that reviewed the drafts or
    the precomputed ``check`` (CheckResult) the human already saw, so the
    package reflects the SAME review -- never a silently different one. The
    reviewing model is recorded on the package (``reviewer_model``). A reviewer
    exception inside run_check escalates to a blocking red; it never aborts
    assembly.
    """
    if check is None:
        check = run_check(study, documents, doc_registry, gate_registry, reviewer=reviewer)
    ledger_by_doc = {item.doc_id: item for item in check.ledger}

    route_docs = route.get("documents", [])
    fda_docs = route.get("fda_package", route_docs)

    # eCTD module map (route-declared), carrying only doc ids that were generated.
    ectd_map: List[Dict[str, Any]] = []
    for module in route.get("ectd_map", []):
        present = [d for d in module.get("doc_ids", []) if d in documents]
        ectd_map.append({
            "module": module["module"],
            "title": module["title"],
            "doc_ids": present,
        })

    # Hash manifest over EVERY route document (provenance substrate) -- not
    # just the FDA-facing subset -- plus the rendered documents themselves so
    # the package is self-verifiable: a standalone verifier recomputes
    # sha256(rendered.utf8) and matches the manifest. A route document that was
    # never generated appears as an explicit ABSENT entry (null hash), so the
    # manifest always accounts for the full declared set.
    manifest: List[Dict[str, Any]] = []
    bundled_documents: List[Dict[str, str]] = []
    doc_hashes: List[str] = []
    for doc_id in route_docs:
        doc = documents.get(doc_id)
        if doc is None:
            title = doc_registry.get(doc_id, {}).get("title", doc_id)
            manifest.append({
                "doc_id": doc_id,
                "title": title,
                "sha256": None,
                "absent": True,
            })
            continue
        digest = _sha256(doc.rendered)
        doc_hashes.append(digest)
        manifest.append({
            "doc_id": doc_id,
            "title": doc.title,
            "sha256": digest,
            "absent": False,
        })
        bundled_documents.append({
            "doc_id": doc_id,
            "title": doc.title,
            "rendered": doc.rendered or "",
        })

    cover_doc = documents.get("expanded-access-cover-letter")
    cover_letter = cover_doc.rendered if cover_doc else ""

    # Blocking = every FDA-facing document that is RED (missing content / failed
    # validation). These are the hard blockers to a complete, signable package.
    blocking: List[Dict[str, Any]] = []
    for doc_id in fda_docs:
        item = ledger_by_doc.get(doc_id)
        if item is not None and item.status == "red":
            blocking.append({
                "doc_id": doc_id,
                "title": item.title,
                "questions": item.questions,
                "message": "%s — %s" % (item.title, " ".join(item.questions)),
            })

    # Route-level completeness (spec §10.3): an LOA cross-reference OR a
    # documented FDA-division contact must be present.
    ind_on_file = str(study.resolve("manufacturer.ind_on_file") or "true").strip().lower() not in ("false", "0", "no")
    has_loa_ref = study.resolve("manufacturer.ind_dmf_reference") is not None
    has_division_contact = study.resolve("manufacturer.fda_division_contact") is not None
    if not has_loa_ref and not (not ind_on_file and has_division_contact):
        q = ("Provide the manufacturer IND/DMF number for the LOA cross-reference "
             "(21 CFR 312.23(b)); or, if no IND is on file, document the FDA review-"
             "division contact that establishes the supporting information FDA needs "
             "(21 CFR 312.305(b)(1)).")
        blocking.append({
            "doc_id": "manufacturer-letter-of-authorization",
            "title": "Manufacturer cross-reference",
            "questions": [q],
            "message": "Manufacturer cross-reference — " + q,
        })

    if as_of is None:
        as_of = derive_as_of(study)
    clocks = compute_clocks(study, route, as_of=as_of)

    manufacturer_packet = _manufacturer_packet(study, documents)

    totals = ledger_totals(check.ledger)

    return {
        "route_id": route.get("route_id"),
        "emergency": bool(route.get("emergency")),
        "as_of": as_of.isoformat() if as_of is not None else None,
        "reviewer_model": check.reviewer_model,
        "ectd_map": ectd_map,
        "cover_letter": cover_letter,
        "documents": bundled_documents,
        "manifest": manifest,
        "package_sha256": _package_digest(doc_hashes),
        "manufacturer_packet": manufacturer_packet,
        "clocks": clocks,
        "totals": totals,
        "submission_ready": len(blocking) == 0,
        "blocking": blocking,
    }


def _manufacturer_packet(study: Study, documents: Dict[str, Document]) -> Dict[str, Any]:
    """The manufacturer's view: the LOA-request and a short cover note."""
    req = documents.get("manufacturer-loa-request")
    loa_request = req.rendered if req else ""
    manufacturer = study.resolve("manufacturer.name") or "the manufacturer"
    drug = study.resolve("drug.name") or "the investigational drug"
    physician = study.resolve("investigator.name") or "the requesting physician"
    supply_committed = str(study.resolve("manufacturer.supply_committed") or "").strip().lower() in ("true", "1", "yes")
    cover = (
        "To %s: %s requests single-patient expanded-access supply of %s and a "
        "Letter of Authorization for FDA cross-reference (21 CFR 312.23(b); FDCA "
        "561A). FDA authorization does not obligate supply — the supply decision "
        "and LOA signature are yours. Supply commitment on file: %s."
        % (manufacturer, physician, drug, "YES" if supply_committed else "not yet recorded")
    )
    return {"loa_request": loa_request, "cover": cover}
