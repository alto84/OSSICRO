# Institutional, CRO & Government Resources

## OSSICRO Institutional Resources

Academic, CRO, and government resources found in the sweeps, with reuse-license status. **Public-domain government sources are the preferred open-source base layer**; institutional and consortium resources are schema references pending license verification.

### Government / Regulator (public domain — freely reusable)

| Institution | Resource | URL | What it offers | Reuse / License |
|---|---|---|---|---|
| US FDA | Form 1572 + completion instructions + FAQ | https://www.fda.gov/media/78830/download | Canonical Statement of Investigator PDF, official field instructions | **Public domain** — freely reusable; ideal first engine target |
| US FDA | IND Forms & Instructions (1571/1572/3454/3455/3500A/3926/3674) | https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-forms-and-instructions | Full FDA form set | **Public domain** |
| US FDA | Sponsor-Investigator IND guidance (Draft 2015) | https://www.fda.gov/files/drugs/published/Investigational-New-Drug-Applications-Prepared-and-Submitted-by-Sponsor-Investigators.pdf | Most on-point doc for the S-I pathway | **Public domain** (flag draft status) |
| NIH OSP / FDA | NIH-FDA Phase 2/3 IND/IDE Protocol Template v1.07 | https://mrctcenter.org/.../MRCT-Center-NIH-Protocol-Template-Version-1.0.pdf | Government-authored protocol skeleton + e-writing tool | **Public domain** — no registration; best open default for S-I use case |
| NIH / NIDDK, NIA, NIAID, NIEHS | Sample DSMB Charters + NIAID DSMB policy | https://www.niddk.nih.gov/-/media/Files/Research-Funding/Process/sample-DSMB-charter-082213.pdf ; https://www.nia.nih.gov/sites/default/files/2023-03/sample_data_and_safety_monitoring_board_dsmb_charter.docx ; https://www.niaid.nih.gov/sites/default/files/dsmbpolicyv5.pdf | Risk-tiered DSMB charter variants; NIA .docx is directly forkable | **Public domain** |
| ICH | E6(R3), M11 CeSHarP, E8(R1), E9, E2A/B/D/F, E3 | https://database.ich.org | GCP standard + structured protocol schema | Freely published for implementation |
| NCATS | Toolkit "Prepare for Clinical Trials" | https://toolkit.ncats.nih.gov/module/prepare-for-clinical-trials/ | Plain-language S-I explainer layer | **Public domain** |
| NCATS | Trial Innovation Network / SMART IRB / IREx | https://ncats.nih.gov/ctsa/projects/network | sIRB reliance/joinder agreements, IREx platform — model for IRB-of-record coordination | Network resource; FDP-CTSA agreement template |
| NLM/NIH | ClinicalTrials.gov v2 API | https://clinicaltrials.gov/data-api | Program-matching integration target (phase/status enums) | Free, no registration; add own semantic layer |

### Academic Medical Centers / CTSAs (schema reference; verify reuse before verbatim adoption)

| Institution | Resource | URL | What it offers | Reuse / License |
|---|---|---|---|---|
| U Penn (ITMAT/OCR) | Numbered document-control template library | https://www.med.upenn.edu/clinicalresearch/forms-tools-templates.html | Richest found; full doc-ID taxonomy (e.g., 03.01.01), IND/IDE, IB, DSMP, PICA, TMF work-instructions | Not stated — schema reusable, confirm before verbatim |
| U Pittsburgh (ECS-HSR) | IND/IDE Templates (initial IND, protocol, CMC, pharm/tox, annual/safety/final, 6 amendment types, financial disclosure) | https://www.ecshsr.pitt.edu/ind-ide-support/investigational-new-drug-ind-templates | Maps ~1:1 to 21 CFR 312 Subpart B; strongest IND-template skeleton | Not stated — verify with Pitt HRPO |
| UNC Lineberger | IIT Toolkit + IB Template (Word) + SOP-30 + Work-Instruction-30 | https://unclineberger.org/iit/ | Best-structured public IIT lifecycle IA; SOP+WI convention | Not stated — contact LCCC_IND@unc.edu |
| Stanford (Spectrum/CRQ) | IND/IDE Regulatory Binder TOC + IND/IDE application templates | https://med.stanford.edu/spectrum/researcher-resources/clinical-research-quality-crq/ind_ide-tools-and-templates.html | Regulatory-binder TOC artifact; 3-way CRQ/RKS/RMG split model | Via Stanford Box; contact regulatory-spectrum@lists.stanford.edu |
| Harvard Catalyst | IND/IDE Consult Program + case studies ("Why Institutions Do Not Hold INDs", "Sharing an IND"); contributory-network model | https://catalyst.harvard.edu/regulatory/ind-ide-consulting/ | Direct confirmation of the S-I legal thesis; networked-support precedent | Publications public; partnership candidate |
| Duke (ORAQ / ReGARDD) | IND & IDE Sponsor/Investigator Training Modules | https://medschool.duke.edu/research/research-support/research-support-offices/office-regulatory-affairs-and-quality/sponsor-0 | ~1hr modules w/ assessment | **Explicitly free to non-Duke academic institutions via ReGARDD** — clearest external license found |
| Northwestern (NUCATS) | Regulatory Toolkit templates (screening/enrollment log, ICF + supplements, CTA, deviation log, drug/device accountability, DOA log) | https://www.nucats.northwestern.edu/training/research-staff-development/nucats-on-demand/regulatory-toolkit-document-templates.html | Participant-facing / site-ops layer | Not stated — verify |
| Weill Cornell (CTSC) / CTSA DSMB Workgroup | DSMB Training Manual for Investigator-Initiated Studies | https://ctscweb.weill.cornell.edu/research-resources/ethics-regulatory-consultation-services/dsmb-training-manual | Cross-CTSA consensus (NCATS-funded); multi-stakeholder authority | Free PDF; best candidate for liberal reuse (confirm) |
| Vanderbilt (VICTR) | V-CAP customized-action-plan methodology | https://pmc.ncbi.nlm.nih.gov/articles/PMC3767144/ | Published prior art: question-set → personalized approval checklist | Published methodology — reimplementable |
| U Michigan (MICHR) | IND/IDE Investigator Assistance Program (MIAP) | https://michr.umich.edu/offering/ind-ide-consultation/ | Fee model (free triage → $90/hr) = micro-CRO service-tier precedent | Service, not templates |
| Mayo Clinic (ORRS) | Sponsor-Investigator IDE IRB reporting-requirement schedule | https://www.mayo.edu/research/documents/38-reporting-req-for-sponsor-investigational-devicepdf/doc-10027871 | Encodable report-type × trigger × deadline rule set | Published policy |
| Johns Hopkins (ICTR/DDRS) | IND Annual Progress Report template v3.0; sponsor-investigator institutional-approval gate | https://ictr.johnshopkins.edu/service/drug-device/ddrs/ | Recurring-compliance template; internal-signoff-gate precedent | 403 to fetch — re-verify before citing specifics |
| MIT (COUHES) | Core IRB forms (ICF, assent 8-17, waiver, HIPAA auth, deviation report, continuing review) | https://couhes.mit.edu/forms-templates | Baseline ICF/assent set; confirms entity separation | Not stated; public IRB page |
| Yale (YCCI), WashU (ICTS), UCLA (CTSI), Columbia (Irving), Emory (Georgia CTSA), UW (ITHS) | Full-lifecycle regulatory consult services; Navigator/facilitator models | (various CTSA pages) | Confirm the canonical phase list and the consult-layer separation | Services; low direct template yield |
| MD Anderson | Annual per-IIT-IND audit cadence (IND Clinical Research Quality Specialist) | (internal) | Recurring-audit precedent for the validate engine | Internal-only |
| MSK | Institution-wide DSMP (NCI Cancer Centers Program) | https://cancercenters.cancer.gov/sites/default/files/DSMPMSKCC.pdf | Canonical risk-tiered DSMP type | Binary PDF — re-extract before citing thresholds |

### CRO / Commercial / Professional bodies

| Institution | Resource | URL | What it offers | Reuse / License |
|---|---|---|---|---|
| TransCelerate | Common Protocol Template (M11/USDM-aligned) | https://www.transceleratebiopharmainc.com/assets/common-protocol-template/assets-download-request/ | Industry protocol skeleton | **Gated; consortium IP** — confirm redistribution before embedding |
| CTTI (Duke/FDA) | Quality by Design Toolkit | https://ctti-clinicaltrials.org/about/ctti-projects/quality-by-design/ | RBM/risk-assessment logic; FDA-cited | Non-proprietary, defensible basis |
| Advarra | IRB Handbook v6 + CIRBI platform | https://www.advarra.com | Commercial central-IRB workflow reference | **Templates proprietary / CIRBI-gated — NOT reusable** |
| SOCRA / ACRP | Certification content outlines | https://acrpnet.org | SOP-category taxonomy check | Member-gated; taxonomy only |

**Scope exclusion:** Broad Institute has no hospital/IIT infrastructure — deliberate exclusion, not a research gap.