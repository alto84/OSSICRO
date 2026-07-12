"""Feature C: the matching engine — a REGISTRY-SEARCH ORGANIZER (Wave 2).

This module is deliberately NOT a recommender. The line it must never cross
is the FDA 2022 Non-Device CDS line: software that lets the physician
independently review the BASIS of every candidate stays on the organizer
side; software that manufactures certainty (a score, a ranking, a
"best match") becomes a device. Named design constraints:

- FDA-2022 Non-Device CDS criterion 4: every candidate carries the exact
  criteria it matched, failed, or could not be verified against — the
  physician reviews the basis, the software never asserts a conclusion.
- NO confidence numbers, NO relevance ranking. Candidates render as
  matched / unmatched / unverifiable CRITERIA, in registry order.
- ABSENCE framing: an empty result renders "no candidates found in the
  queried registries as of <date>" — registry lag must never tell a
  physician that no options exist.
- v1 SCOPE = open trials + expanded-access records ONLY. Diagnosis->drug
  ranking (the most CDS-shaped third) is deferred until GAP-4 (a
  human-confirmed manufacturer/drug registry) and the eval harness exist;
  any other record kind an adapter returns is dropped here, structurally.
- Every candidate is a physician-confirmed PROPOSAL. Nothing here acts.

All queries go through ``ossicro.egress.egress_query`` — the single
sanctioned outbound constructor (INV-4): only de-identified, decomposed
predicates reach an adapter, and every query is audit-logged. Age / sex /
route are compared LOCALLY in this module, never sent. This module imports
no network client and never sees chart data — only the closed
``DeidentifiedPredicates`` struct.
"""

from __future__ import annotations

import copy
import json
import os
import re
from typing import Dict, List, Optional, Tuple

from .egress import DeidentifiedPredicates, egress_query

__all__ = ["MockRegistryAdapter", "match", "ABSENCE_MESSAGE_TEMPLATE"]

_FIXTURES_DIR = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "fixtures")
DEFAULT_REGISTRY_FIXTURE = os.path.join(_FIXTURES_DIR, "registry_sample.json")

# The exact absence framing (BLOCKER 1): "found in the queried registries as
# of <date>", never "no options exist".
ABSENCE_MESSAGE_TEMPLATE = ("no candidates found in the queried registries "
                            "as of %s")

# v1 scope: open trials + expanded-access records ONLY (Fable SERIOUS 5 /
# BLOCKER 1). Anything else an adapter hands back is dropped.
_V1_KINDS = frozenset({"trial", "ea_record"})

_ICD10_CATEGORY_RE = re.compile(r"^[A-Za-z]\d{2}$")


class MockRegistryAdapter:
    """Fixture-backed registry adapter — the ONLY adapter that exists while
    live egress is disabled. Serves synthetic records from
    ``engine/fixtures/registry_sample.json`` and answers the decomposed
    query shape the egress gateway sends (condition codes + drug identity;
    never age/sex — those are filtered locally by ``match``)."""

    def __init__(self, fixture_path: Optional[str] = None):
        path = fixture_path or DEFAULT_REGISTRY_FIXTURE
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        self.records: List[dict] = list(data.get("records", []))
        self.registries: List[str] = sorted(
            {r.get("source_registry", "") for r in self.records if r.get("source_registry")})

    def search(self, destination: str, condition_codes: List[str],
               drug_name: Optional[str] = None,
               drug_rxnorm: Optional[str] = None) -> List[dict]:
        """Records from ``destination`` whose eligibility condition codes
        overlap the (possibly rolled-up) query codes. A rolled ICD-10
        category code ('C22') matches its extension codes ('C22.1')."""
        out = []
        for rec in self.records:
            if rec.get("source_registry") != destination:
                continue
            rec_codes = (rec.get("eligibility") or {}).get("condition_codes", [])
            if _codes_overlap(condition_codes, rec_codes):
                out.append(copy.deepcopy(rec))
        return out


def _codes_overlap(query_codes: List[str], record_codes: List[str]) -> bool:
    for qc in query_codes:
        for rc in record_codes:
            if rc == qc:
                return True
            if _ICD10_CATEGORY_RE.match(qc) and str(rc).startswith(qc + "."):
                return True
    return False


# ---------------------------------------------------------------------------
# Local criteria comparison (the decomposed query's second half): age, sex,
# route, drug, and exact condition codes are evaluated HERE, against each
# candidate's STRUCTURED eligibility — never in the outbound query.
# ---------------------------------------------------------------------------

def _band_range(age_band: str) -> Tuple[int, int]:
    if age_band == "90+":
        return 90, 200
    lo, hi = age_band.split("-")
    return int(lo), int(hi)


def _criteria(predicates: DeidentifiedPredicates,
              eligibility: dict) -> Tuple[List[str], List[str], List[str]]:
    """(matched, unmatched, unverifiable) criterion strings for ONE candidate.

    Every string names the criterion and the basis — the physician can see
    exactly what was compared (Non-Device CDS criterion 4). Anything the
    structured data cannot settle is UNVERIFIABLE, never guessed green.
    """
    matched: List[str] = []
    unmatched: List[str] = []
    unverifiable: List[str] = []

    # Condition — exact code overlap with the FULL (un-rolled) predicates.
    rec_codes = [str(c) for c in eligibility.get("condition_codes", [])]
    exact = sorted(set(rec_codes) & set(predicates.condition_codes))
    if exact:
        matched.append("condition code %s" % ", ".join(exact))
    elif rec_codes:
        # Returned via the rolled-up category query: same code family, but
        # the exact predicate code is not listed — the physician verifies.
        unverifiable.append(
            "condition (candidate lists %s; returned by rolled-up code "
            "category — exact condition code not listed)"
            % ", ".join(sorted(rec_codes)))

    # Age — compared LOCALLY (never sent outbound).
    has_age_rule = ("age_min" in eligibility) or ("age_max" in eligibility)
    if has_age_rule:
        lo = eligibility.get("age_min")
        hi = eligibility.get("age_max")
        label = "age %s-%s" % ("" if lo is None else lo,
                               "no upper limit" if hi is None else hi)
        if predicates.age_band is None:
            unverifiable.append(
                "%s (no age band in the de-identified predicates)" % label)
        else:
            band_lo, band_hi = _band_range(predicates.age_band)
            lo_v = 0 if lo is None else int(lo)
            hi_v = 200 if hi is None else int(hi)
            if band_lo >= lo_v and band_hi <= hi_v:
                matched.append("%s (age band %s)" % (label, predicates.age_band))
            elif band_hi < lo_v or band_lo > hi_v:
                unmatched.append("%s (age band %s)" % (label, predicates.age_band))
            else:
                unverifiable.append(
                    "%s (age band %s straddles the limit — exact age not "
                    "verifiable from a 5-year band)" % (label, predicates.age_band))

    # Sex — compared LOCALLY.
    rec_sex = eligibility.get("sex")
    if rec_sex:
        if rec_sex == "all":
            matched.append("sex: all")
        elif predicates.sex is None:
            unverifiable.append("sex: %s (no sex in the de-identified "
                                "predicates)" % rec_sex)
        elif predicates.sex == rec_sex:
            matched.append("sex: %s" % rec_sex)
        else:
            unmatched.append("sex: %s (predicates: %s)" % (rec_sex, predicates.sex))

    # Drug identity (expanded-access records are drug-specific).
    rec_drug = eligibility.get("drug_name")
    if rec_drug:
        if predicates.drug_name is None:
            unverifiable.append("drug: %s (no drug in the predicates)" % rec_drug)
        elif str(rec_drug).lower() == predicates.drug_name.lower():
            matched.append("drug: %s" % rec_drug)
        else:
            unmatched.append("drug: %s (predicates: %s)"
                             % (rec_drug, predicates.drug_name))

    # Unstructured eligibility text can NEVER be verified from structured
    # predicates — honest unverifiable, never silently ignored.
    for criterion in eligibility.get("unstructured", []) or []:
        unverifiable.append(
            "not verifiable from structured data: %s" % criterion)

    # MINOR-4: any structured eligibility key this comparator does not evaluate
    # (route, pregnancy exclusions, ECOG limits, ...) is surfaced as
    # unverifiable, never silently dropped — the physician sees that the record
    # carries a criterion OSSICRO did not compare.
    for key in sorted(eligibility):
        if key not in _EVALUATED_ELIGIBILITY_KEYS:
            unverifiable.append("not evaluated from structured data: %s" % key)

    return matched, unmatched, unverifiable


# The eligibility keys _criteria actually compares. Route is deliberately
# WITHHELD from egress and, today, not compared locally either — so it lands in
# the catch-all above rather than being silently ignored.
_EVALUATED_ELIGIBILITY_KEYS = frozenset({
    "condition_codes", "age_min", "age_max", "sex", "drug_name", "unstructured",
})


# ---------------------------------------------------------------------------
# The organizer
# ---------------------------------------------------------------------------

def match(predicates: DeidentifiedPredicates, adapter, *,
          trail: List[dict], as_of: str, actor: str = "") -> Dict[str, object]:
    """Query every registry the adapter serves and organize the results.

    Returns the shared /match contract body: candidates (each with
    matched / unmatched / unverifiable CRITERIA — no score, no ranking, in
    registry order), the absence framing, the queried registries, the
    predicates used, and ``as_of``. ``trail`` is the case audit trail —
    every registry query writes one ``egress_query`` record through the
    INV-4 gateway. ``as_of`` is supplied by the caller (the engine never
    reads the wall clock).
    """
    queried = list(getattr(adapter, "registries", []))
    candidates: List[dict] = []
    seen_ids = set()
    for destination in queried:
        for rec in egress_query(predicates, destination, adapter=adapter,
                                trail=trail, actor=actor):
            kind = rec.get("kind")
            if kind not in _V1_KINDS:        # v1 scope, structurally enforced
                continue
            rec_id = str(rec.get("id", ""))
            if rec_id and rec_id in seen_ids:
                continue
            if rec_id:
                seen_ids.add(rec_id)
            m, u, v = _criteria(predicates, rec.get("eligibility") or {})
            candidates.append({
                "kind": kind,
                "id": rec_id,
                "title": rec.get("title", ""),
                "source_registry": rec.get("source_registry", ""),
                "source_url": rec.get("source_url", ""),
                "matched_criteria": m,
                "unmatched_criteria": u,
                "unverifiable_criteria": v,
            })

    absence = not candidates
    return {
        "candidates": candidates,
        "absence": absence,
        "absence_message": (ABSENCE_MESSAGE_TEMPLATE % as_of) if absence else "",
        "queried_registries": queried,
        "predicates_used": predicates.as_dict(),
        "as_of": as_of,
    }
