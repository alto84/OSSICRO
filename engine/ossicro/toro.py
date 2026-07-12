"""TORO — Transfer of Regulatory Obligations generator (21 CFR 312.52).

The micro-CRO's accountable layer is defined by exactly which sponsor
obligations it assumes in writing. This module turns an obligation election
into a DRAFT TORO document plus a structured obligation-to-owner map, and it
enforces the one line that must never move: the non-delegable obligations
(informed consent, IRB judgment, investigator conduct, the sponsor-investigator's
own signatures, DSMB deliberation, the manufacturer's supply decision) can never
be marked transferred. Attempting to transfer one raises TransferError — the
same fail-closed posture as the engine's other non-delegable gates (HC1).

21 CFR 312.52(a): a transfer must be described in writing; any obligation not
described is deemed NOT transferred. 312.52(b): a CRO that assumes an obligation
is subject to the same regulatory action as a sponsor for that obligation.

Pure stdlib. Nothing here signs, files, or executes the transfer — it drafts a
document for a qualified human to review and sign.
"""
from __future__ import annotations

import json
import pathlib
from typing import Any, Dict, List, Optional

REGISTRY_DIR = pathlib.Path(__file__).resolve().parent.parent / "registry"


class TransferError(ValueError):
    """An election would transfer an obligation that cannot be transferred, or
    names an unknown obligation, or uses an invalid scope. Fail closed."""


def load_sponsor_obligations() -> Dict[str, Any]:
    """The Subpart D sponsor-obligation menu (transferable + non_transferable)."""
    with open(REGISTRY_DIR / "sponsor_obligations.json", encoding="utf-8") as f:
        return json.load(f)


def _index(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {o["id"]: o for o in rows}


def build_toro(
    *,
    scope: str,
    transferred_ids: Optional[List[str]] = None,
    parties: Optional[Dict[str, Dict[str, str]]] = None,
    protocol: Optional[Dict[str, str]] = None,
    effective_date: Optional[str] = None,
    services_agreement_reference: str = "",
) -> Dict[str, Any]:
    """Build a DRAFT TORO from an obligation election.

    ``scope`` is ``"all"`` (a general transfer of all sponsor obligations, which
    21 CFR 312.52(a) permits to be stated generally) or ``"enumerated"`` (only
    the transferable obligations named in ``transferred_ids`` move; everything
    else is retained by operation of 312.52(a)).

    Refuses (``TransferError``) any attempt to transfer a non-delegable
    obligation or an unknown obligation id — checked BEFORE anything is drafted.
    """
    reg = load_sponsor_obligations()
    transferable = reg["transferable"]
    non_transferable = reg["non_transferable"]
    t_index = _index(transferable)
    nt_index = _index(non_transferable)

    if scope not in ("all", "enumerated"):
        raise TransferError("scope must be 'all' or 'enumerated' (21 CFR 312.52(a))")

    transferred_ids = list(transferred_ids or [])

    # Fail closed on any non-delegable or unknown id BEFORE drafting anything.
    for oid in transferred_ids:
        if oid in nt_index:
            o = nt_index[oid]
            raise TransferError(
                "cannot transfer %r: it is a non-delegable obligation held by the "
                "%s (%s). %s 21 CFR 312.52 reaches only sponsor obligations."
                % (oid, o["holder"], ", ".join(o["citations"]), o["reason"]))
        if oid not in t_index:
            raise TransferError(
                "unknown obligation id %r (not in the transferable Subpart D menu)"
                % oid)

    transferred_set = set(t_index) if scope == "all" else set(transferred_ids)

    table: List[Dict[str, Any]] = []
    owner_map: List[Dict[str, Any]] = []
    warnings: List[str] = []
    retained: List[str] = []
    for o in transferable:
        is_t = o["id"] in transferred_set
        table.append({
            "n": o["n"], "id": o["id"], "description": o["description"],
            "citations": o["citations"],
            "status": "Transferred" if is_t else "Retained",
        })
        owner_map.append({
            "obligation": o["id"], "description": o["description"],
            "citations": o["citations"], "holder": "CRO" if is_t else "sponsor",
            "transferable": True,
        })
        if not is_t:
            retained.append(o["id"])
        if is_t and o.get("requires_qualified_human"):
            warnings.append("%s — %s" % (o["id"], o["requires_qualified_human"]))

    # The non-delegable obligations are always named with their fixed holder:
    # an honest TORO shows what it CANNOT move, not only what it does.
    for o in non_transferable:
        owner_map.append({
            "obligation": o["id"], "description": o["description"],
            "citations": o["citations"], "holder": o["holder"],
            "transferable": False, "reason": o["reason"],
        })

    result: Dict[str, Any] = {
        "scope": scope,
        "transferred": sorted(transferred_set),
        "retained": retained,
        "deemed_not_transferred_note": (
            "By operation of 21 CFR 312.52(a), every sponsor obligation not marked "
            "'Transferred' above is deemed NOT transferred and remains with the "
            "sponsor. The non-delegable obligations are never transferable by any TORO."
        ),
        "obligation_table": table,
        "owner_map": owner_map,
        "warnings": warnings,
        "non_transferable_ids": sorted(nt_index),
    }
    result["rendered"] = _render(
        result, parties or {}, protocol or {}, effective_date,
        services_agreement_reference)
    return result


def _p(parties: Dict[str, Dict[str, str]], key: str, field: str, default: str) -> str:
    return str((parties.get(key) or {}).get(field) or default)


def _render(result, parties, protocol, effective_date, services_ref) -> str:
    sponsor = _p(parties, "sponsor", "legal_name", "[[MISSING: sponsor legal name]]")
    sponsor_addr = _p(parties, "sponsor", "address", "[[MISSING: sponsor address]]")
    cro = _p(parties, "cro", "legal_name", "[[MISSING: CRO / micro-CRO legal name]]")
    cro_addr = _p(parties, "cro", "address", "[[MISSING: CRO address]]")
    pnum = str(protocol.get("number") or "[[MISSING: protocol number]]")
    ptitle = str(protocol.get("title") or "[[MISSING: protocol title]]")
    ind = str(protocol.get("ind_number") or "[[MISSING: IND number]]")
    eff = str(effective_date or "[[MISSING: effective date]]")

    lines: List[str] = []
    lines.append("TRANSFER OF REGULATORY OBLIGATIONS")
    lines.append("Under 21 CFR 312.52")
    lines.append("")
    lines.append("DRAFT — for qualified human review and signature; not a filing, "
                 "not legal advice. OSSICRO drafts; the authorized officers of the "
                 "Sponsor and the CRO review and sign.")
    lines.append("")
    lines.append("Protocol No.: %s" % pnum)
    lines.append("Protocol Title: %s" % ptitle)
    lines.append("IND No.: %s" % ind)
    lines.append("Effective Date: %s" % eff)
    lines.append("Sponsor: %s, %s" % (sponsor, sponsor_addr))
    lines.append("Contract Research Organization: %s, %s" % (cro, cro_addr))
    lines.append("")
    lines.append("1. TRANSFER (21 CFR 312.52(a))")
    if result["scope"] == "all":
        lines.append("   Scope: ALL sponsor obligations set forth in 21 CFR Part 312 "
                     "are transferred to the CRO (a general statement of transfer of "
                     "all obligations satisfies 21 CFR 312.52(a)). The table below is "
                     "retained for operational clarity.")
    else:
        lines.append("   Scope: ENUMERATED. Only the obligations marked 'Transferred' "
                     "in Section 2 are transferred; all obligations not so marked are "
                     "retained by the Sponsor (21 CFR 312.52(a)).")
    lines.append("")
    lines.append("2. DESCRIPTION OF SPECIFIC OBLIGATIONS")
    lines.append("   #  | Sponsor obligation | Citation | Status")
    for row in result["obligation_table"]:
        lines.append("   %-2d | %s | %s | %s"
                     % (row["n"], row["description"],
                        "; ".join(row["citations"]), row["status"]))
    lines.append("")
    lines.append("   Deemed not transferred: %s" % result["deemed_not_transferred_note"])
    lines.append("")
    lines.append("3. NON-DELEGABLE OBLIGATIONS (never transferable by this instrument)")
    for entry in result["owner_map"]:
        if not entry["transferable"]:
            lines.append("   - %s (%s) — remains with the %s. %s"
                         % (entry["description"], "; ".join(entry["citations"]),
                            entry["holder"], entry.get("reason", "")))
    lines.append("")
    lines.append("4. CRO ACKNOWLEDGMENT (21 CFR 312.52(b))")
    lines.append("   For each obligation it assumes, the CRO is subject to the same "
                 "regulatory action as a sponsor for failure to comply, and all "
                 "references to 'sponsor' in 21 CFR Part 312 apply to the CRO to the "
                 "extent of the assumed obligations.")
    if result["warnings"]:
        lines.append("")
        lines.append("   Qualified-human conditions on assumed obligations:")
        for w in result["warnings"]:
            lines.append("   - %s" % w)
    lines.append("")
    lines.append("5. RETAINED OVERSIGHT")
    lines.append("   Notwithstanding any transfer, the Sponsor retains ultimate "
                 "responsibility for the quality and integrity of the trial data and "
                 "shall exercise appropriate oversight of CRO-performed activities "
                 "(ICH E6(R3) Annex 1).")
    lines.append("")
    lines.append("6. DOCUMENTATION TO FDA")
    lines.append("   The Sponsor identifies this transfer on Form FDA 1571, Field 16 "
                 "(Contract Research Organizations: the CRO's name and address and a "
                 "listing of the obligations transferred), and submits or references "
                 "this instrument in the IND. Any submission to FDA is a "
                 "human-authorized act; OSSICRO assembles, a human files.")
    if services_ref:
        lines.append("")
        lines.append("   Underlying services agreement: %s" % services_ref)
    lines.append("")
    lines.append("SIGNATURES (human legal acts — OSSICRO drafts, humans execute)")
    lines.append("   For Sponsor: Name ______  Title ______  Signature ______  Date ______")
    lines.append("   For CRO:     Name ______  Title ______  Signature ______  Date ______")
    return "\n".join(lines)
