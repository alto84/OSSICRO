# SMALL-FIXES — consolidated, de-duplicated apply list

Synthesized 2026-07-11 from the persona reviews in `docs/review/` (physician, manufacturer,
regulator, ethics, compliance, developer). **persona-patient.md had not been delivered at
synthesis time** — if it lands with [SMALL-FIX] items, append them here before applying.

Every "current" string below was verified verbatim against the working tree this pass, and the
test suites were grepped for pins on every changed string — **no test pins any of them**
(the one string change that IS test-pinned, `v1.0`, includes its test edit in the same group).
Apply serially, top to bottom. Line numbers are as of this verification pass.

**Totals: 20 fix items (26 individual edits) across 10 files. 1 raw [SMALL-FIX] dropped, 5 de-duplicated (see end).**

---

## README.md

### R1. Hard-constraint list understated (HC1–HC5 → HC1–HC7)  [physician #4 + compliance F1 — identical]
Line 7. Current:
```
(HC1–HC5: no non-delegable act, no fabrication, computed statutory clocks, provenance/verbatim integrity, Part-11 attribution)
```
Replace with:
```
(HC1–HC7: no non-delegable act, no fabrication, computed statutory clocks, provenance/verbatim integrity, Part-11 attribution, no exculpatory consent language, no drafting-process leakage)
```

### R2. Stale test count  [compliance F3 + developer F4 — developer's fuller wording chosen]
Line 14. Current:
```
**9/9 tests pass**
```
Replace with:
```
**336/336 tests pass** (`python -m pytest engine/tests/ app/tests/ -q`)
```

### R3. README advertises the superseded Form 1571 item number as the fix  [compliance F2]
Line 59. Current:
```
Fixed now: the confirmed Form 1571 CRO-disclosure field (Field 16 -> **Field 14**).
```
Replace with:
```
Fixed now: the confirmed Form 1571 CRO-disclosure field (Field 16 -> **item 15**, per Form FDA 1571 (03/19); item 14 is "Contents of Application" — see qa/REVISE-LOG.md).
```

---

## app/static/index.html

### H1. Working-day parenthetical inverts the engine's behavior  [physician #1]
Lines ~657–658. Current:
```
          Each deadline is computed from a <b>physician-entered trigger date</b>, counted in working
          days or calendar days (weekends and observed federal holidays included). If no trigger
```
Replace with:
```
          Each deadline is computed from a <b>physician-entered trigger date</b>, counted in working
          days (weekends and observed federal holidays excluded) or calendar days (included). If no trigger
```

### H2. "Never leaves this machine" is deployment-coupled  [physician #5]
Lines ~585–586. Current:
```
        Your chart data is parsed locally and never leaves this machine; nothing here becomes part of
        the submission until you confirm it — field by field, below.
```
Replace with:
```
        Your chart data goes only to your local OSSICRO server on this machine and never beyond it; nothing here becomes part of
        the submission until you confirm it — field by field, below.
```
*Note:* strictly more accurate than the current text and safe to apply now, but the BLOCKER
(B1, concept-reviewer egress — see INVENTORY.md) must revisit this line again: with a live
`ANTHROPIC_API_KEY`, rendered documents containing confirmed chart values DO leave the machine.

### H3. Commit-card "values are never stored" is ambiguous  [physician #6]
Lines ~638–639. Current:
```
        The commit stores your name, the time, and a SHA-256 fingerprint of each confirmed value.
        The values themselves are never stored.
```
Replace with:
```
        The commit stores your name, the time, and a SHA-256 fingerprint of each confirmed value.
        The commit record itself stores no values — the intake values remain in the case file as usual.
```

### H4. "Not advice" disclaimer never reaches the app UI  [compliance F5]
Lines ~905–906 (footer). Current:
```
    non-delegable acts (consent, IRB approval, causality, signatures, submission) are never performed by software.
  </footer>
```
Replace with:
```
    non-delegable acts (consent, IRB approval, causality, signatures, submission) are never performed by software.
    Not medical, legal, or regulatory advice.
  </footer>
```

### H5. Manufacturer-view claim "No patient identifiers appear" is overbroad  [manufacturer #1]
Line ~1013. Current:
```
      "Synthetic cases only through the pilot. No patient identifiers appear in this view.",
```
Replace with:
```
      "Synthetic cases only through the pilot. No direct patient identifiers appear in this view — the patient is shown by coded ID only.",
```

### H6. Patient-view stage heading claims treatment has begun  [ethics #14]
Lines ~1094–1095. Current:
```
      "enrollment": "The formal treatment process has begun",
      "enrolled": "The formal treatment process has begun"
```
Replace with:
```
      "enrollment": "Your enrollment has been recorded",
      "enrolled": "Your enrollment has been recorded"
```

### H7. Green readiness banner omits the third-party acts  [physician #7]
Lines ~2431–2432. Current:
```
      What remains: the physician's review, the required signatures, and the physician's
      own act of submission to FDA. OSSICRO does not file.</div>`;
```
Replace with:
```
      What remains: the physician's review and signatures, the third-party acts tracked in the
      ledger (manufacturer LOA, IRB concurrence, informed consent), and the physician's
      own act of submission to FDA. OSSICRO does not file.</div>`;
```

### H8. Match panel overstates what left the machine  [physician #2]
Lines ~2575–2576. Current:
```
    <p class="muted small" style="margin:8px 0 0"><b>De-identified search terms sent.</b> Everything
      that left the case is shown below; it contains no names, dates, geography, or identifiers:</p>
```
Replace with:
```
    <p class="muted small" style="margin:8px 0 0"><b>De-identified search terms used.</b> The full set
      is shown below — only the condition codes and drug token are sent to registries; age band, sex,
      and route are compared locally and never sent. None of it contains names, dates, geography, or identifiers:</p>
```

---

## engine/registry/routes.json

### J1. plan_version help invites a double "v" prefix ("vv1.0" in the rendered ICF)  [ethics #11a — apply with F1/T1/E-fixture below as one group]
Line 29, the `help` value. Current:
```
"help": "e.g. v1.0. Feeds the consent form's version field so amendments are traceable."
```
Replace with:
```
"help": "e.g. 1.0 (the form adds the 'v'). Feeds the consent form's version field so amendments are traceable."
```

### J2. Help text promises a default that cannot happen (`submission.date` is not a schema field)  [physician #3 + manufacturer #4 — manufacturer's wording chosen]
Line 46, the `help` value. Current:
```
"help": "Arms the 30-calendar-day IND-effective clock. Defaults to the submission date if left blank."
```
Replace with:
```
"help": "Arms the 30-calendar-day IND-effective clock. If left blank, the clock stays unarmed until this date is entered."
```

### J3. 15-working-day clock `basis` uses the imprecise subsection  [regulator F4]
Line 133. Current:
```
"basis": "21 CFR 312.310(d)"
```
Replace with:
```
"basis": "21 CFR 312.310(d)(2)"
```

---

## engine/ossicro/clocks.py

### C1. Module docstring conflates 56.104(c) with the quorum/waiver path  [regulator F5 + compliance F4 — regulator's fuller wording chosen]
Lines 15–16. Current:
```
- 5 WORKING DAYS — IRB notification after emergency/single-patient use where the
  expedited/less-than-quorum path is used (21 CFR 56.104(c) / 56.108).
```
Replace with:
```
- 5 WORKING DAYS — IRB notification after emergency use of the test article
  (21 CFR 56.104(c)); the clock runs from the emergency use (first treatment).
```
*Note:* this docstring fix does NOT resolve backlog item M1 (the wrong anchor date in
`expanded_access_emergency_deadlines` / `_enrollment_obligations`) — both compliance and
the regulator flag that separately as a MAJOR code change.

### C2. "Day 31 is the earliest dose day" contradicts the returned date  [regulator F7]
Lines 152–153 (docstring of `ind_30_day_deadline`). Current:
```
    """21 CFR 312.40(b)(1): the IND goes into effect 30 calendar days after FDA
    receipt (absent hold or earlier notification). Day 31 is the earliest dose day."""
```
Replace with:
```
    """21 CFR 312.40(b)(1): the IND goes into effect 30 calendar days after FDA
    receipt (absent hold or earlier notification). The returned date is the
    IND-effective date (30 calendar days after receipt) and the earliest day
    treatment may begin absent earlier FDA notification."""
```

---

## engine/ossicro/ea_generators.py

### G1. Cover-letter enclosure list promises "IRB concurrence evidence" the package does not contain  [ethics #12 + regulator F6 — ethics' exact-line wording chosen]
Lines 370–371 (`_COVER_TEMPLATE`). Current:
```
6. ENCLOSURES. Form FDA 3926; expanded-access treatment plan; manufacturer
   Letter of Authorization; IRB concurrence evidence; informed consent form.
```
Replace with:
```
6. ENCLOSURES. Form FDA 3926; expanded-access treatment plan; manufacturer
   Letter of Authorization; IRB concurrence request (the IRB's concurrence
   evidence is attached when received); informed consent form.
```
*Note:* the "manufacturer Letter of Authorization" entry in the same list has its own MAJOR
(M2 — enclosure asserts a letter the manufacturer never issued); that reword rides with M2.

### G2. 15-working-day clock citations use 312.310(d) instead of (d)(2) — three sites  [regulator F4]
(a) Line 427. Current:
```
                "312.310(d))." % (auth, written.due.isoformat())
```
Replace with:
```
                "312.310(d)(2))." % (auth, written.due.isoformat())
```
(b) Line 432. Current:
```
                "compute the 15-working-day written-3926 deadline (21 CFR 312.310(d))."
```
Replace with:
```
                "compute the 15-working-day written-3926 deadline (21 CFR 312.310(d)(2))."
```
(c) Line 434. Current:
```
        clock_cite = "21 CFR 312.310(d)"
```
Replace with:
```
        clock_cite = "21 CFR 312.310(d)(2)"
```
*Scope note:* only the deadline/clock citations move to (d)(2). The other bare `312.310(d)`
occurrences (routes.json lines 43/44/50/106, ea_generators 464/479/543/548, server.py 82/330)
cite the emergency pathway generally and correctly stay at (d).

### G3. FMV/anti-kickback proposition attributed to the wrong statute  [manufacturer #2]
Lines 753–755 (LOA-request template). Current:
```
5. FDA authorization of expanded access does NOT obligate supply. The supply
   decision, the LOA signature, and any fair-market-value / anti-kickback
   judgment are the manufacturer's alone (FDCA 561A).
```
Replace with:
```
5. FDA authorization of expanded access does NOT obligate supply. The supply
   decision, the LOA signature, and any fair-market-value / anti-kickback
   judgment (42 U.S.C. 1320a-7b) are the manufacturer's alone (FDCA 561A).
```

---

## engine/ossicro/generate.py

### N1. ICF element 1 runs purpose and duration into one unpunctuated sentence  [ethics #13]
Line 123 (template `informed-consent-form-part50`, element 1). Current:
```
   {{purpose}} Expected duration of participation: {{duration}}
```
Replace with:
```
   {{purpose}}
   Expected duration of participation: {{duration}}
```
(The verbatim-locked span for element 1 is the heading line only; `R-ICF-50.25` hashes are
undisturbed — verified by the ethics reviewer.)

---

## engine/fixtures/ea_sample_case.json

### F1. Sample fixture carries the "v" the template re-adds  [ethics #11b — same group as J1]
Line 31. Current:
```
    "treatment.plan_version": "v1.0",
```
Replace with:
```
    "treatment.plan_version": "1.0",
```

---

## engine/ossicro/fhir_ingest.py

### I1. Derived default carries the "v" the template re-adds  [ethics #11c — same group as J1]
Line 895. Current:
```
    out.append(_proposal("treatment.plan_version", "v1.0", "(none)",
```
Replace with:
```
    out.append(_proposal("treatment.plan_version", "1.0", "(none)",
```

---

## engine/tests/test_fhir_ingest.py

### T1. Test pin for the value changed in I1  [ethics #11d — MUST apply together with J1/F1/I1]
Line 170. Current:
```
        self.assertEqual(by["treatment.plan_version"]["value"], "v1.0")
```
Replace with:
```
        self.assertEqual(by["treatment.plan_version"]["value"], "1.0")
```

---

## docs/route-3926-submission-spec.md

### S1. Same FMV/AKS citation defect as G3, in the governing spec  [manufacturer #3]
Line 157. Current:
```
5. A statement that FDA authorization of expanded access does **not** obligate supply, and that the decision, LOA signature, and any FMV/anti-kickback judgment are the manufacturer's (FDCA §561A) — set expectations honestly (CP4).
```
Replace with:
```
5. A statement that FDA authorization of expanded access does **not** obligate supply, and that the decision, LOA signature, and any FMV/anti-kickback judgment (42 U.S.C. §1320a-7b) are the manufacturer's (FDCA §561A) — set expectations honestly (CP4).
```

---

## Dropped and de-duplicated

**Dropped (1):**
- **Regulator F8** (move `irb-concurrence-request` from the eCTD Module-5 `doc_ids` to Module 1,
  routes.json lines 95/130): labeled [SMALL-FIX] by the persona but supplied no exact
  replacement text, requires editing two JSON arrays consumed by assembly/ledger code, and the
  persona itself called it optional/lowest-priority. Moved to the INVENTORY backlog as MINOR.

**De-duplicated (5 pairs, one entry kept each):**
- README.md:7 HC list — physician #4 ≡ compliance F1 (identical replacement) → R1.
- README.md:14 test count — compliance F3 vs developer F4 (same intent, different wording;
  developer's kept because it documents the run command) → R2.
- routes.json:46 help text — physician #3 vs manufacturer #4 (differ only "the date"/"this
  date"; manufacturer's kept) → J2.
- clocks.py:15–16 docstring — regulator F5 vs compliance F4 (regulator's kept: also states the
  correct first-treatment anchor) → C1.
- ea_generators.py:370–371 enclosures — regulator F6 vs ethics #12 (ethics' kept: exact
  line-shaped replacement) → G1.

**Verification performed:** every "current" string grep-confirmed present at the cited
location; `engine/tests/` and `app/tests/` grepped for pins on every changed string — none
found except test_fhir_ingest.py:170, which is included as T1 in the same apply group.
After applying, run `python -m pytest engine/tests/ app/tests/ -q` (expect 336 passed).
