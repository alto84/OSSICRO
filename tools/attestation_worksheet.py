"""Generate the HITL-2 citation + statutory-clock attestation worksheet.

This is the highest-risk human-in-the-loop pass in OSSICRO (review roadmap
HITL-2): a qualified human verifies, one by one, that every regulatory citation
the engine emits is correct for what it asserts, and that every statutory clock
is computed per the regulation. AI review does not substitute for a qualified
human signing "I verified this against the primary source" — and this project
already caught one wrong citation (Form 1571 field 14 vs 16) only by checking
the primary source.

The worksheet is REGENERATED from the live registries + a sample render, so it
never drifts from the code the reviewer is attesting. Run:

    python tools/attestation_worksheet.py

Output: docs/hitl/citation-clock-attestation-worksheet.md
"""

from __future__ import annotations

import datetime
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "engine"))

from ossicro import clocks, routes  # noqa: E402
from ossicro.ea_generators import build_study, generate_route_documents  # noqa: E402
from ossicro.registry import load_documents  # noqa: E402

REG = os.path.join(REPO, "engine", "registry")
OUT = os.path.join(REPO, "docs", "hitl", "citation-clock-attestation-worksheet.md")

# A fixed, weekday anchor so the computed clock examples are reproducible and a
# reviewer can check the arithmetic by hand. 2026-07-15 is a Wednesday.
ANCHOR = datetime.date(2026, 7, 15)


def _load(name):
    with open(os.path.join(REG, name), encoding="utf-8") as f:
        return json.load(f)


def _clock_rows():
    rows = []
    routes_json = _load("routes.json")["routes"]
    for rid, route in routes_json.items():
        for c in route.get("clocks", []):
            basis = c.get("calendar", "calendar")
            n = c.get("days")
            if basis == "working":
                due = clocks.add_working_days(ANCHOR, n)
                rule = "%d WORKING days after the trigger (weekends + observed federal holidays skipped)" % n
            else:
                due = ANCHOR + datetime.timedelta(days=n)
                rule = "%d CALENDAR days after the trigger" % n
            rows.append({
                "route": rid,
                "id": c.get("id"),
                "label": c.get("label"),
                "citation": c.get("basis") or c.get("citation") or "—",
                "trigger": c.get("trigger_field"),
                "rule": rule,
                "example": "trigger %s → due %s" % (ANCHOR.isoformat(), due.isoformat()),
            })
    return rows


def _citation_rows_from_registries():
    """Distinct citations from gates, rules, and intake fields, with where-used."""
    seen = {}

    def add(citation, where, asserts):
        if not citation:
            return
        seen.setdefault(citation, {"where": set(), "asserts": set()})
        seen[citation]["where"].add(where)
        seen[citation]["asserts"].add(asserts)

    for g in _load("gates.json").get("gates", _load("gates.json")) if isinstance(_load("gates.json"), dict) else _load("gates.json"):
        if isinstance(g, dict) and g.get("citation"):
            add(g["citation"], "gate:%s" % g.get("id"), g.get("label") or g.get("id"))
    rules = _load("rules.json")
    for r in (rules.get("rules") if isinstance(rules, dict) else rules):
        if isinstance(r, dict) and r.get("citation"):
            add(r["citation"], "rule:%s" % r.get("id"), r.get("statement") or r.get("id"))
    for f in _load("routes.json").get("intake_fields", []):
        if isinstance(f, dict) and f.get("citation"):
            add(f["citation"], "field:%s" % f.get("id"), f.get("label") or f.get("id"))
    return seen


def _citation_rows_from_render():
    """Citations actually emitted into generated documents (provenance)."""
    fields = json.load(open(os.path.join(REPO, "engine", "fixtures", "ea_sample_case.json"),
                             encoding="utf-8")).get("fields", {})
    emitted = {}
    for emergency in (False, True):
        route = routes.route_for_emergency(emergency)
        study = build_study(dict(fields), route)
        docs = generate_route_documents(study, route, load_documents())
        for d in docs:
            for rec in getattr(d, "provenance", []) or []:
                cit = getattr(rec, "citation", None)
                if cit:
                    emitted.setdefault(cit, set()).add("%s:%s" % (d.doc_id, getattr(rec, "span", "?")))
    return emitted


def _md_escape(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def main():
    clock_rows = _clock_rows()
    reg_cites = _citation_rows_from_registries()
    emitted_cites = _citation_rows_from_render()
    # union of registry + emitted citations
    all_cites = {}
    for cit, meta in reg_cites.items():
        all_cites[cit] = {"where": set(meta["where"]), "asserts": set(meta["asserts"])}
    for cit, spans in emitted_cites.items():
        all_cites.setdefault(cit, {"where": set(), "asserts": set()})
        for s in list(spans)[:6]:
            all_cites[cit]["where"].add("doc:%s" % s)

    lines = []
    W = lines.append
    W("# OSSICRO — Citation & Statutory-Clock Attestation Worksheet")
    W("")
    W("**Generated:** %s (regenerate with `python tools/attestation_worksheet.py`).  " % ANCHOR.isoformat())
    W("**Purpose (HITL-2).** Before any real use, a qualified human verifies every "
      "regulatory citation and every statutory clock the engine emits, against the "
      "**primary source** (eCFR / U.S.C.). This is the single highest-risk pass in the "
      "system: a wrong citation or an off-by-one deadline can delay a patient's access "
      "or get a submission rejected. AI review is **not** a substitute for a named "
      "qualified human's sign-off here.")
    W("")
    W("**How to use.** For each row: open the primary source, confirm the citation says "
      "what the *Asserts / used-for* column claims, mark ✅ or ✍️ (needs change), and "
      "initial + date. For clocks, also confirm the day-count, the working-vs-calendar "
      "basis, and the trigger against the regulation, then check the computed example by "
      "hand. Record any correction in *Notes*; corrections become code changes tracked "
      "separately.")
    W("")
    W("**Attester (fill in):** name ______________________  role ______________________  "
      "date __________  signature ______________________")
    W("")
    W("> This attestation certifies citation/clock correctness only. It is **not** an IRB "
      "> approval, informed consent, sponsor signature, or FDA submission — those remain "
      "> non-delegable human acts performed elsewhere (Constitution HC1).")
    W("")

    W("## 1. Statutory clocks (%d)" % len(clock_rows))
    W("")
    W("| ✔ | Clock | Route | Rule | Trigger field | Citation (primary source) | Computed example | Correct? | Init/Date | Notes |")
    W("|---|-------|-------|------|---------------|---------------------------|------------------|----------|-----------|-------|")
    for r in clock_rows:
        W("| ☐ | %s | `%s` | %s | `%s` | %s | %s | ☐ | | |" % (
            _md_escape(r["label"]), _md_escape(r["route"]), _md_escape(r["rule"]),
            _md_escape(r["trigger"]), _md_escape(r["citation"]), _md_escape(r["example"])))
    W("")
    W("_Federal-holiday basis for working-day clocks: 5 U.S.C. 6103 with the OPM "
      "weekend-observance rule (Saturday→Friday, Sunday→Monday). Verify the holiday "
      "table in `engine/ossicro/clocks.py::federal_holidays` against OPM for the "
      "relevant year._")
    W("")

    W("## 2. Citations (%d distinct)" % len(all_cites))
    W("")
    W("| ✔ | Citation | Asserts / used-for | Where used | Correct? | Init/Date | Notes |")
    W("|---|----------|--------------------|------------|----------|-----------|-------|")
    for cit in sorted(all_cites):
        meta = all_cites[cit]
        asserts = "; ".join(sorted(meta["asserts"])) if meta["asserts"] else "(see where-used)"
        where = ", ".join(sorted(meta["where"])[:8])
        if len(meta["where"]) > 8:
            where += " (+%d more)" % (len(meta["where"]) - 8)
        W("| ☐ | %s | %s | %s | ☐ | | |" % (
            _md_escape(cit), _md_escape(asserts[:180]), _md_escape(where)))
    W("")
    W("## 3. Sign-off")
    W("")
    W("- [ ] All statutory clocks verified against primary source (§1).")
    W("- [ ] All citations verified against primary source (§2).")
    W("- [ ] Corrections (if any) filed as code-change items and re-verified.")
    W("")
    W("Attester signature: ______________________  Date: __________")
    W("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("wrote %s" % OUT)
    print("  clocks: %d | distinct citations: %d" % (len(clock_rows), len(all_cites)))


if __name__ == "__main__":
    main()
