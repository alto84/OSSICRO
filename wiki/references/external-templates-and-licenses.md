---
title: "External Templates and Licenses"
section: "references"
status: mixed
governing_authority:
  - "17 U.S.C. § 105 (works of the US Government — no domestic copyright)"
  - "Individual institutional and consortium license terms (per row)"
tags: [status/interpretive, ossicro/engine, entity/institutional, lifecycle/activation]
aliases: ["template provenance", "seed templates", "license status"]
updated: 2026-07-09
---

# External Templates and Licenses

> [!authority] Governing authority
> 17 U.S.C. § 105 (US Government works carry no domestic copyright — the public-domain basis for the FDA/NIH seed layer); otherwise the license terms of each originating institution or consortium, recorded per row. Status: **Mixed** — license facts are confirmed where the source states them; every unverified reuse position below is flagged, and the reuse *policy* is an OSSICRO interpretive position.

OSSICRO ships a document-template library (~80 templates enumerated in `docs/template-manifest.json`, spanning the [[document-catalog]] from [[form-fda-1571-ind-cover|the 1571]] to the [[clinical-study-report]]). Because OSSICRO is open source, every template's provenance and license status must be clean enough to redistribute — a template silently derived from gated consortium IP or an institution's unlicensed work product is a legal defect in the repository, not just a courtesy lapse. This page records where each seed came from, what its license status is, and the rules that govern how external material may be used. It pairs with [[institutional-resources]] (the full resource survey) and `sources/MANIFEST.md` (the 1,015-document source library with per-document license class).

## License classes

The source library manifest assigns every downloaded document one of six classes (counts as of the manifest date):

| Class | Count | Meaning | Template use permitted? |
|---|---|---|---|
| `public-domain` | 536 | US Government work (17 U.S.C. § 105) or equivalent | Yes — verbatim fork, modify, redistribute |
| `open/CC` | 263 | Explicit open license (CC-BY etc.) | Yes, per license terms (attribution etc.) |
| `redistributable` | 115 | Source states free redistribution without a formal license | Yes, with provenance note; prefer confirmation |
| `open-government` | 30 | Non-US government open publication | Yes, per issuing government's terms |
| `unknown-verify` | 42 | No stated terms | **Schema reference only** until verified |
| `gated-cite-only` | 29 | Registration-walled or explicit consortium/commercial IP | **Cite only — never embed** |

## Tier 1 — Public-domain government seeds (the base layer)

These are the preferred seeds: verbatim-forkable, no clearance needed.

| Seed | Source | License | Feeds templates |
|---|---|---|---|
| FDA Forms 1571, 1572, 3454, 3455, 3500A, 3926, 3674 (+ official instructions) | [FDA IND forms hub](https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-forms-and-instructions) | **Public domain** | The seven `form-fda-*` templates; field rules for the [[generate-check-validate-engine]]. See [[fda-form-index]] |
| NIH-FDA Clinical Trial Protocol Template for Phase 2/3 IND/IDE Studies (v1.0, 2017; e-Protocol tool) | NIH Office of Science Policy / FDA ([mirror PDF](https://mrctcenter.org/diversity-in-clinical-research/wp-content/uploads/sites/8/2022/06/MRCT-Center-NIH-Protocol-Template-Version-1.0.pdf)) · Local: `../sources/protocol-template/nih-fda-protocol-template-v1.0-2017.docx` | **Public domain** — no registration | `clinical-protocol-*`, `protocol-synopsis`; the open default for the [[sponsor-investigator]] use case |
| Sample DSMB charters — NIDDK (2013 PDF) and NIA (2023 .docx, directly forkable); NIAID DSMB Policy v5 | [NIDDK](https://www.niddk.nih.gov/-/media/Files/Research-Funding/Process/sample-DSMB-charter-082213.pdf) · [NIA](https://www.nia.nih.gov/sites/default/files/2023-03/sample_data_and_safety_monitoring_board_dsmb_charter.docx) · [NIAID](https://www.niaid.nih.gov/sites/default/files/dsmbpolicyv5.pdf) | **Public domain** | `dsmb-charter-single-site-low-risk`, `dsmb-charter-multisite-high-risk`; see [[dsmb-charter]] |
| NIMH / NIDCR / NIAMS operational templates (delegation-of-authority log, IP accountability logs, note-to-file, MOP templates, clinical-monitoring-plan templates, DSMB report templates, deviation logs) | NIH institute toolboxes · Local: `../sources/institutional-template/nimh_*`, `../sources/monitoring/nidcr_*`, `niams_*` | **Public domain** | `delegation-of-authority-log`, `drug-accountability-log`, `note-to-file`, `risk-based-monitoring-plan`, DSMB reporting set |
| NIDA CTN and NINDS protocol templates; NIH BSSR template | NIH institutes · Local: `../sources/protocol-template/nida_ctn_protocol_template.pdf`, `ninds_protocol_template_508c.pdf` | **Public domain** | Protocol variants |
| NCI CTEP templates (ETCTN protocol template, generic ICF template, sample forms); DAIDS essential-documents policy + SCORE tools | NCI / NIAID DAIDS · Local: `../sources/protocol-template/ctep_etctn_protocol_template.docx`, `../sources/ethics/ctep_generic_informed_consent_template.docx`, `../sources/institutional-template/daids_*` | **Public domain** | `informed-consent-form-part50`, essential-records matrix cross-check ([[document-catalog]]) |
| FDA guidance PDFs (e.g., Sponsor-Investigator IND draft 2015) | FDA | **Public domain** (flag draft status per [[fda-guidance-map]]) | Instructional text within templates |

**ICH documents** (E6(R3), M11 CeSHarP template and technical specification, E2 family, E3): freely published on [database.ich.org](https://database.ich.org) with no registration wall, expressly for implementation by regulators and industry. They are **not** US Government works; ICH's own legal notice governs reproduction. OSSICRO treats them as freely implementable — structure and data fields are built into `clinical-protocol-ich-m11-ceshharp` and the [[statistical-analysis-plan]]/[[clinical-study-report]] templates — while verbatim wholesale re-hosting of guideline text stays out of the template library (link the ICH PDF instead). *(Interpretive reuse position.)*

## Tier 2 — Institutional libraries (schema reference; verify before verbatim reuse)

The strongest institutional template sets found in the [[institutional-resources|sweeps]]. None states an open license unless noted; until terms are confirmed with the named contact, these are **structure/coverage references only** — OSSICRO templates are authored fresh against the underlying regulation, then checked against these for completeness.

| Institution | Resource | Stated terms | Verification path |
|---|---|---|---|
| U. Pittsburgh (ECS-HSR) | Full IND lifecycle template set (initial IND, protocol/CMC/pharm-tox sections, annual/safety/final reports, six amendment types) — maps ~1:1 to 21 CFR 312 Subpart B; the amendment taxonomy behind OSSICRO's six `*-amendment` templates | Not stated | [Pitt ECS-HSR page](https://www.ecshsr.pitt.edu/ind-ide-support/investigational-new-drug-ind-templates); confirm with Pitt HRPO |
| Penn Medicine (OCR/ITMAT) | Numbered document-control library (IND/IDE applications, IB template + addendum log, DSMP, TMF work instructions); the doc-ID scheme (e.g., 03.01.01) adopted as OSSICRO's numbering convention in [[data-model]] | Not stated | [Penn OCR page](https://www.med.upenn.edu/clinicalresearch/forms-tools-templates.html) |
| UNC Lineberger | IIT Toolkit: Investigator's Brochure template (Word) + SOP-30/WI-30 (IB drafting and amending) | Not stated | [UNC IIT toolkit](https://unclineberger.org/iit/); contact LCCC_IND@unc.edu |
| Stanford (Spectrum/CRQ) | IND/IDE Regulatory Binder tables of contents — the model for [[regulatory-binder-isf-index]] | Not stated; distributed via Stanford Box | [Stanford CRQ page](https://med.stanford.edu/spectrum/researcher-resources/clinical-research-quality-crq/ind_ide-tools-and-templates.html); contact regulatory-spectrum@lists.stanford.edu |
| Duke (ORAQ, via ReGARDD) | IND and IDE Sponsor/Investigator training modules (~1 hr, with assessments) | **Explicitly free to academic institutions outside Duke** via ReGARDD request — the clearest external license found | [Duke ORAQ page](https://medschool.duke.edu/research/research-support/research-support-offices/office-regulatory-affairs-and-quality/sponsor-0) |
| Weill Cornell CTSC (CTSA Collaborative DSMB Workgroup) | DSMB Training Manual for Investigator-Initiated Studies — NCATS-funded cross-institutional consensus; primary source for [[dsmb-workflow]] | Free PDF, positioned as a public network resource; no formal license | [Weill Cornell page](https://ctscweb.weill.cornell.edu/research-resources/ethics-regulatory-consultation-services/dsmb-training-manual) |
| Vanderbilt (VICTR) | V-CAP customized-action-plan methodology | Published methodology ([PMC3767144](https://pmc.ncbi.nlm.nih.gov/articles/PMC3767144/)) — citable and independently reimplementable; the tool itself is not distributed | See [[prior-art-vcap-irex-smartirb]] |
| Mayo Clinic (ORRS) | Sponsor-investigator reporting-obligation schedule (report type × trigger × deadline) — the encodable rule-set model for the validate pass | Published institutional policy; cite, reimplement rules independently | [Mayo document](https://www.mayo.edu/research/documents/38-reporting-req-for-sponsor-investigational-devicepdf/doc-10027871) |
| Johns Hopkins (ICTR/DDRS) | IND Annual Progress Report guidance/template v3.0 | **Unverified** — page 403'd to automated fetch; existence confirmed only via search snippet | Re-verify at [JHU DDRS](https://ictr.johnshopkins.edu/service/drug-device/ddrs/) before citing specifics |
| Northwestern (NUCATS) | Regulatory Toolkit (screening/enrollment log, ICF supplements, CTA template, deviation log, accountability logs, DOA log) | Not stated | [NUCATS page](https://www.nucats.northwestern.edu/training/research-staff-development/nucats-on-demand/regulatory-toolkit-document-templates.html) |
| MIT (COUHES) | Core IRB forms (ICF, assent 8–17, waiver requests, HIPAA authorization, deviation reporting, continuing review) | Not stated; public IRB page | [COUHES forms](https://couhes.mit.edu/forms-templates) |
| U. Utah (OQC), UAB, BU CRRO, OHSU, U. Colorado Anschutz | Site-operations logs, SOP sets, regulatory-binder checklists (local under `../sources/institutional-template/`, `../sources/protocol-template/`) | Not stated (`unknown-verify`) | Schema reference only |

## Tier 3 — Consortium / commercial (gated; cite-only)

| Source | Resource | Status | OSSICRO handling |
|---|---|---|---|
| TransCelerate BioPharma | Common Protocol Template (CPT; realigned to ICH M11/USDM) | Free but **gated behind a download-request form; consortium member-company IP**; redistribution terms for an open-source project unconfirmed | **Never embedded.** ICH M11 (freely published) is the structured-protocol target instead; CPT used only as a published cross-check. Confirm terms with TransCelerate before any deeper use |
| WCG / Advarra | Central-IRB template libraries (consent templates HRP-50x, reliance forms HRP-23x, expanded-access worksheets) — local copies under `../sources/institutional-template/wcg_*`, `../sources/ethics/advarra_*` | **Proprietary / platform-gated** (`gated-cite-only`) | Cite as workflow precedent for [[single-irb-mandate-and-central-irbs]]; never fork |
| SMART IRB / NCATS IREx | Master reliance agreement (v1.2/v3.0), joinder samples, SOPs — local under `../sources/reliance-agreement/` | Network resource, free to participating institutions; NCATS-supported | Reliance *mechanics* modeled in [[single-irb-mandate-and-central-irbs]]; the agreement instrument belongs to the SMART IRB network — sites execute the network's own instrument, OSSICRO does not redistribute a modified fork |
| CTTI (Duke/FDA) | Quality-by-Design toolkit and recommendations | Freely published recommendations, FDA-cited | Basis for CtQ logic in [[monitoring-plan]]; cite and implement |

## Reuse policy (the rules the repo follows)

1. **Public domain first.** Every template that *can* be seeded from a US Government work *is* (FDA forms, NIH-FDA protocol template, NIH DSMB charters, NIH institute logs). This covers the majority of the manifest.
2. **Regulation is the skeleton, institutions are the checklist.** Section structures that regulation itself dictates (the 21 CFR 312.23 content headings; ICH E6(R3) Appendix C record list; 21 CFR 50.25 consent elements) are drawn directly from the authority. Institutional templates are used to *verify coverage*, not as copy sources, unless their terms are confirmed.
3. **Provenance is recorded per template.** Each shipped template carries a provenance record (seed source, license class, verification date, authority citations) in the template manifest — the same discipline [[draft-provenance-model]] applies to generated documents, applied to the library itself.
4. **Gated sources never enter the repo.** `gated-cite-only` material is cited in the wiki with attribution and never committed, quoted at length, or paraphrased into templates.
5. **Changes are watched.** License re-verifications and institutional-page changes are tracked in the [[regulatory-change-log]] alongside regulatory motion.

> [!warning] Non-delegable
> Final license clearance — deciding that an `unknown-verify` institutional template may be redistributed verbatim in an open-source repository, or negotiating terms with a consortium — is a legal judgment for a qualified human (counsel or the responsible maintainer corresponding with the named institutional contact), not an inference the engine or an authoring agent may make from a webpage's silence. Absence of a stated license is **not** permission.

> [!interpretive] OSSICRO position
> The tier system above is an OSSICRO risk policy, not a statement of copyright law. It is deliberately conservative: the project's credibility with institutional partners (several of which — Harvard Catalyst, Duke/ReGARDD — are candidate collaborators, per [[prior-art-vcap-irex-smartirb]] and the [[micro-cro-operating-model]]) is worth more than any single borrowed template.

## Related
- [[institutional-resources]]
- [[index|References — how to cite in OSSICRO]]
- [[document-catalog]]
- [[generate-check-validate-engine]]
- [[draft-provenance-model]]
- [[data-model]]
- [[dsmb-charter]]
- [[clinical-protocol-and-synopsis]]
- [[regulatory-binder-isf-index]]
- [[prior-art-vcap-irex-smartirb]]
- [[regulatory-change-log]]

## Sources
- [17 U.S.C. § 105 — Subject matter of copyright: United States Government works](https://www.law.cornell.edu/uscode/text/17/105)
- [FDA — IND Forms and Instructions](https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-forms-and-instructions)
- [NIH-FDA Protocol Template v1.0 (mirror)](https://mrctcenter.org/diversity-in-clinical-research/wp-content/uploads/sites/8/2022/06/MRCT-Center-NIH-Protocol-Template-Version-1.0.pdf)
- [NIDDK sample DSMB charter](https://www.niddk.nih.gov/-/media/Files/Research-Funding/Process/sample-DSMB-charter-082213.pdf) · [NIA sample DSMB charter (.docx)](https://www.nia.nih.gov/sites/default/files/2023-03/sample_data_and_safety_monitoring_board_dsmb_charter.docx) · [NIAID DSMB policy v5](https://www.niaid.nih.gov/sites/default/files/dsmbpolicyv5.pdf)
- [ICH database (M11 final template; E6(R3))](https://database.ich.org)
- [TransCelerate Common Protocol Template request page](https://www.transceleratebiopharmainc.com/assets/common-protocol-template/assets-download-request/)
- [U. Pittsburgh ECS-HSR IND templates](https://www.ecshsr.pitt.edu/ind-ide-support/investigational-new-drug-ind-templates)
- [Penn Medicine OCR forms/tools/templates](https://www.med.upenn.edu/clinicalresearch/forms-tools-templates.html)
- [Vanderbilt V-CAP methodology (PMC3767144)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3767144/)
- [Weill Cornell CTSC — DSMB Training Manual](https://ctscweb.weill.cornell.edu/research-resources/ethics-regulatory-consultation-services/dsmb-training-manual)
- Source library manifest with per-document license class: `../sources/MANIFEST.md`
- Template list: `../docs/template-manifest.json`
