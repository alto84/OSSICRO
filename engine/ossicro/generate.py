"""GENERATE pass: instantiate templates from structured study data.

Simple ``{{field}}`` substitution over a template string. Every filled
field emits a ProvenanceRecord (span -> source datum -> citation).
Fields whose source datum is missing are left as an explicit
``[[MISSING: field]]`` marker in the rendered text and are NOT added to
``document.fields`` -- the CHECK pass turns each into a red ledger item
with the exact resolving question.

Output is always a DRAFT for qualified human review. Nothing generated
here is a signed or filed document.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

from .models import Document, ProvenanceRecord, Study

_PLACEHOLDER = re.compile(r"\{\{([A-Za-z0-9_]+)\}\}")

# ---------------------------------------------------------------------------
# Built-in template strings (prototype set; the full library lives in the
# OSSICRO template manifest -- 78 templates).
# ---------------------------------------------------------------------------

TEMPLATES: Dict[str, str] = {
    "form-fda-1571-ind-cover": """\
FORM FDA 1571 - INVESTIGATIONAL NEW DRUG APPLICATION (COVER)          [DRAFT]
Authority: 21 CFR 312.23(a)(1)

 1. NAME OF SPONSOR: {{sponsor_name}}
 2. ADDRESS: {{sponsor_address}}
 4. IND NUMBER: {{ind_number}}          5. SERIAL NUMBER: {{serial_number}}
 6. NAME(S) OF DRUG: {{drug_name}}
 8. PHASE(S) OF CLINICAL INVESTIGATION TO BE CONDUCTED: Phase {{phase}}
10. CONTENTS OF APPLICATION: protocol {{protocol_number}} - {{protocol_title}}
14. NAME AND TITLE OF PERSON RESPONSIBLE FOR MONITORING: {{contact_name}}
    TELEPHONE: {{contact_phone}}

COMMITMENTS: I agree not to begin clinical investigations until 30 days
after FDA's receipt of the IND unless I receive earlier notification by
FDA that the studies may begin (21 CFR 312.40(b)(1)). I agree that an
IRB compliant with 21 CFR Part 56 will be responsible for initial and
continuing review and approval of each study. I agree to conduct the
investigation in accordance with all other applicable regulatory
requirements.

15. SIGNATURE OF SPONSOR OR SPONSOR'S AUTHORIZED REPRESENTATIVE:
    ________________________________________________________________
    [NON-DELEGABLE HUMAN ACT - gate: ind-1571-signature. This engine
     drafts the form; only the sponsor-investigator may sign it.]
""",
    "form-fda-1572-statement-of-investigator": """\
FORM FDA 1572 - STATEMENT OF INVESTIGATOR                             [DRAFT]
Authority: 21 CFR 312.53(c)(1)

 1. NAME AND ADDRESS OF INVESTIGATOR
    {{investigator_name}}
    {{investigator_address}}
 2. EDUCATION, TRAINING, AND EXPERIENCE (CV attached per 312.53(c)(2))
    {{education_degrees}}
 3. NAME AND ADDRESS OF FACILITY WHERE THE STUDY WILL BE CONDUCTED
    {{site_name}}
    {{site_address}}
 4. NAME AND ADDRESS OF CLINICAL LABORATORY FACILITIES
    {{clinical_lab_name}}
    {{clinical_lab_address}}
 5. NAME AND ADDRESS OF THE IRB RESPONSIBLE FOR REVIEW AND APPROVAL
    {{irb_name}}
    {{irb_address}}
 6. NAMES OF SUBINVESTIGATORS
    {{subinvestigators}}
 7. NAME AND CODE NUMBER OF THE PROTOCOL(S)
    {{protocol_number}} - {{protocol_title}}
 8. PHASE OF CLINICAL INVESTIGATION: Phase {{phase}}   IND: {{ind_number}}
 9. COMMITMENTS: I agree to conduct the study(ies) in accordance with
    the relevant, current protocol(s); to personally conduct or
    supervise the described investigation(s); to inform any subjects
    that the drugs are being used for investigational purposes and to
    ensure that the requirements relating to obtaining informed consent
    (21 CFR Part 50) and IRB review and approval (21 CFR Part 56) are
    met; to report adverse experiences per 21 CFR 312.64; to maintain
    adequate and accurate records per 21 CFR 312.62 and to make those
    records available for inspection per 21 CFR 312.68.

10. SIGNATURE OF INVESTIGATOR                       11. DATE
    ______________________________________________  ____________
    [NON-DELEGABLE HUMAN ACT - gate: 1572-signature. This engine
     fills the form; only the named investigator may sign it.]
""",
    "delegation-of-authority-log": """\
DELEGATION OF AUTHORITY / SITE RESPONSIBILITY LOG                     [DRAFT]
Authority: ICH E6(R3) 2.7; FDA Guidance on Investigator Responsibilities (2009)

Protocol: {{protocol_number}} v{{protocol_version}} - {{protocol_title}}
IND: {{ind_number}}
Site: {{site_name}}
Principal Investigator: {{investigator_name}}
Log effective date: {{effective_date}}

+------------------+----------------+----------------------+--------+--------+---------------------+
| Staff name       | Study role     | Delegated tasks      | Start  | End    | PI initials / date  |
+------------------+----------------+----------------------+--------+--------+---------------------+
|                  |                |                      |        |        |                     |
+------------------+----------------+----------------------+--------+--------+---------------------+
Note: task delegation is documented here, but investigator supervision
responsibility is itself non-delegable (21 CFR 312.60).
""",
    "informed-consent-form-part50": """\
INFORMED CONSENT FORM                                                 [DRAFT]
Authority: 21 CFR 50.25 (basic elements), 21 CFR 50.27 (documentation)
STATUS: draft for IRB review. The consent EVENT is a non-delegable human
act between the investigator and the subject (gate: informed-consent).

Study: {{protocol_title}}
Protocol: {{protocol_number}} v{{protocol_version}}
Principal Investigator: {{investigator_name}}, {{site_name}}

1. RESEARCH STATEMENT, PURPOSE, DURATION, PROCEDURES - 50.25(a)(1)
   You are being asked to take part in a research study. Purpose:
   {{purpose}}
   Expected duration of participation: {{duration}}
   Procedures (experimental procedures identified): {{procedures}}

2. REASONABLY FORESEEABLE RISKS OR DISCOMFORTS - 50.25(a)(2)
   {{risks}}

3. BENEFITS THAT MAY REASONABLY BE EXPECTED - 50.25(a)(3)
   {{benefits}}

4. APPROPRIATE ALTERNATIVE PROCEDURES OR TREATMENTS - 50.25(a)(4)
   {{alternatives}}

5. CONFIDENTIALITY OF RECORDS - 50.25(a)(5)
   {{confidentiality_statement}} Records may be inspected by the FDA.

6. COMPENSATION AND MEDICAL TREATMENT FOR INJURY - 50.25(a)(6)
   If you believe you have been injured as a result of this research,
   contact {{injury_contact_name}} at {{injury_contact_phone}}.

7. WHOM TO CONTACT - 50.25(a)(7)
   Questions about the research: {{research_contact}}.
   Questions about your rights as a research subject: {{irb_name}},
   {{irb_phone}}.

8. VOLUNTARY PARTICIPATION - 50.25(a)(8)
   Participation is voluntary. Refusal to participate involves no
   penalty or loss of benefits to which you are otherwise entitled, and
   you may discontinue participation at any time without penalty.

SIGNATURE OF SUBJECT: ______________________  DATE: ____________
PERSON OBTAINING CONSENT: __________________  DATE: ____________
   [NON-DELEGABLE HUMAN ACT - gate: informed-consent. This engine
    drafts the form; consent itself is obtained by a qualified human.]
""",
}

# For each built-in template: field -> (dotted source path into the raw
# study record, governing citation for the span).
FIELD_SOURCES: Dict[str, Dict[str, Tuple[str, str]]] = {
    "form-fda-1571-ind-cover": {
        "sponsor_name": ("investigator.name", "Form FDA 1571 item 1; 21 CFR 312.3(b) (sponsor-investigator holds both roles)"),
        "sponsor_address": ("investigator.address", "Form FDA 1571 item 2"),
        "ind_number": ("ind_number", "Form FDA 1571 item 4"),
        "serial_number": ("ind_serial_number", "Form FDA 1571 item 5"),
        "drug_name": ("drug.name", "Form FDA 1571 item 6; 21 CFR 312.23(a)(1)(vii)"),
        "phase": ("phase", "Form FDA 1571 item 8"),
        "protocol_number": ("protocol_number", "Form FDA 1571 item 10; 21 CFR 312.23(a)(6)"),
        "protocol_title": ("title", "Form FDA 1571 item 10"),
        "contact_name": ("contacts.monitor_name", "Form FDA 1571 item 14; 21 CFR 312.53(d)"),
        "contact_phone": ("contacts.monitor_phone", "Form FDA 1571 item 14"),
    },
    "form-fda-1572-statement-of-investigator": {
        "investigator_name": ("investigator.name", "Form FDA 1572 item 1; 21 CFR 312.53(c)(1)(i)"),
        "investigator_address": ("investigator.address", "Form FDA 1572 item 1"),
        "education_degrees": ("investigator.degrees", "Form FDA 1572 item 2; 21 CFR 312.53(c)(2)"),
        "site_name": ("site.name", "Form FDA 1572 item 3; 21 CFR 312.53(c)(1)(ii)"),
        "site_address": ("site.address", "Form FDA 1572 item 3"),
        "clinical_lab_name": ("site.clinical_lab.name", "Form FDA 1572 item 4; 21 CFR 312.53(c)(1)(iii)"),
        "clinical_lab_address": ("site.clinical_lab.address", "Form FDA 1572 item 4"),
        "irb_name": ("irb.name", "Form FDA 1572 item 5; 21 CFR 312.53(c)(1)(iv)"),
        "irb_address": ("irb.address", "Form FDA 1572 item 5"),
        "subinvestigators": ("subinvestigators", "Form FDA 1572 item 6; 21 CFR 312.53(c)(1)(v)"),
        "protocol_number": ("protocol_number", "Form FDA 1572 item 7; 21 CFR 312.53(c)(1)(vi)"),
        "protocol_title": ("title", "Form FDA 1572 item 7"),
        "phase": ("phase", "Form FDA 1572 item 8; 21 CFR 312.53(c)(1)(vii)"),
        "ind_number": ("ind_number", "Form FDA 1572 item 8"),
    },
    "delegation-of-authority-log": {
        "protocol_number": ("protocol_number", "ICH E6(R3) 2.7"),
        "protocol_version": ("protocol_version", "ICH E6(R3) 2.7"),
        "protocol_title": ("title", "ICH E6(R3) 2.7"),
        "ind_number": ("ind_number", "ICH E6(R3) 2.7"),
        "site_name": ("site.name", "ICH E6(R3) 2.7"),
        "investigator_name": ("investigator.name", "ICH E6(R3) 2.7; 21 CFR 312.60"),
        "effective_date": ("delegation.effective_date", "ICH E6(R3) 2.7"),
    },
    "informed-consent-form-part50": {
        "protocol_title": ("title", "21 CFR 50.20"),
        "protocol_number": ("protocol_number", "21 CFR 50.20"),
        "protocol_version": ("protocol_version", "21 CFR 50.20"),
        "investigator_name": ("investigator.name", "21 CFR 50.25(a)(7)"),
        "site_name": ("site.name", "21 CFR 50.20"),
        "purpose": ("consent.purpose", "21 CFR 50.25(a)(1)"),
        "duration": ("consent.duration", "21 CFR 50.25(a)(1)"),
        "procedures": ("consent.procedures", "21 CFR 50.25(a)(1)"),
        "risks": ("consent.risks", "21 CFR 50.25(a)(2)"),
        "benefits": ("consent.benefits", "21 CFR 50.25(a)(3)"),
        "alternatives": ("consent.alternatives", "21 CFR 50.25(a)(4)"),
        "confidentiality_statement": ("consent.confidentiality_statement", "21 CFR 50.25(a)(5)"),
        "injury_contact_name": ("contacts.injury_contact_name", "21 CFR 50.25(a)(6)"),
        "injury_contact_phone": ("contacts.injury_contact_phone", "21 CFR 50.25(a)(6)"),
        "research_contact": ("contacts.research_contact", "21 CFR 50.25(a)(7)"),
        "irb_name": ("irb.name", "21 CFR 50.25(a)(7)"),
        "irb_phone": ("irb.phone", "21 CFR 50.25(a)(7)"),
    },
}

# ---------------------------------------------------------------------------
# Verbatim-locked template spans: doc_id -> span_id -> (canonical text, citation).
#
# These are fixed template prose, present BY CONSTRUCTION of generation.
# When a registered span renders, generation stamps a ProvenanceRecord for
# it, so provenance-strategy rules (ossicro.rules) verify the span's
# presence and byte-identity (SHA-256 registered in registry/rules.json)
# instead of substring-hunting for proxy words in the prose.
# ---------------------------------------------------------------------------

VERBATIM_SPANS: Dict[str, Dict[str, Tuple[str, str]]] = {
    "form-fda-1571-ind-cover": {
        "commitment-30-day-wait": (
            "COMMITMENTS: I agree not to begin clinical investigations until 30 days\n"
            "after FDA's receipt of the IND unless I receive earlier notification by\n"
            "FDA that the studies may begin (21 CFR 312.40(b)(1)).",
            "21 CFR 312.40(b)(1)",
        ),
    },
    "informed-consent-form-part50": {
        "icf-element-1": (
            "1. RESEARCH STATEMENT, PURPOSE, DURATION, PROCEDURES - 50.25(a)(1)",
            "21 CFR 50.25(a)(1)",
        ),
        "icf-element-2": (
            "2. REASONABLY FORESEEABLE RISKS OR DISCOMFORTS - 50.25(a)(2)",
            "21 CFR 50.25(a)(2)",
        ),
        "icf-element-3": (
            "3. BENEFITS THAT MAY REASONABLY BE EXPECTED - 50.25(a)(3)",
            "21 CFR 50.25(a)(3)",
        ),
        "icf-element-4": (
            "4. APPROPRIATE ALTERNATIVE PROCEDURES OR TREATMENTS - 50.25(a)(4)",
            "21 CFR 50.25(a)(4)",
        ),
        "icf-element-5": (
            "5. CONFIDENTIALITY OF RECORDS - 50.25(a)(5)",
            "21 CFR 50.25(a)(5)",
        ),
        "icf-element-6": (
            "6. COMPENSATION AND MEDICAL TREATMENT FOR INJURY - 50.25(a)(6)",
            "21 CFR 50.25(a)(6)",
        ),
        "icf-element-7": (
            "7. WHOM TO CONTACT - 50.25(a)(7)",
            "21 CFR 50.25(a)(7)",
        ),
        "icf-element-8": (
            "8. VOLUNTARY PARTICIPATION - 50.25(a)(8)",
            "21 CFR 50.25(a)(8)",
        ),
    },
}

MISSING_MARKER = "[[MISSING: %s]]"


def generate_document(study: Study, doc_id: str, doc_registry: Dict[str, dict]) -> Document:
    """Instantiate the built-in template ``doc_id`` from ``study``.

    Every filled field carries a ProvenanceRecord. Missing source data is
    rendered as an explicit marker and omitted from Document.fields so
    the completeness ledger can flag it red with a resolving question.
    """
    if doc_id not in TEMPLATES:
        raise KeyError(
            "No built-in template for %r (available: %s)"
            % (doc_id, ", ".join(sorted(TEMPLATES)))
        )
    entry = doc_registry.get(doc_id, {})
    template = TEMPLATES[doc_id]
    sources = FIELD_SOURCES[doc_id]

    fields: Dict[str, str] = {}
    provenance: List[ProvenanceRecord] = []

    def substitute(match: "re.Match[str]") -> str:
        name = match.group(1)
        if name not in sources:
            return MISSING_MARKER % name
        path, citation = sources[name]
        value = study.resolve(path)
        if value is None:
            return MISSING_MARKER % name
        if name not in fields:
            fields[name] = value
            provenance.append(
                ProvenanceRecord(
                    span=name,
                    source="%s = %r" % (path, value),
                    citation=citation,
                )
            )
        return value

    rendered = _PLACEHOLDER.sub(substitute, template)

    # Stamp provenance for verbatim-locked template spans that rendered.
    # The span is present by construction; the record is what lets a
    # provenance-strategy rule verify it without inspecting prose meaning.
    for span_id, (span_text, span_citation) in VERBATIM_SPANS.get(doc_id, {}).items():
        if span_text in rendered:
            provenance.append(
                ProvenanceRecord(
                    span=span_id,
                    source="template:%s#%s" % (doc_id, span_id),
                    citation=span_citation,
                )
            )

    return Document(
        doc_id=doc_id,
        title=entry.get("title", doc_id),
        state="draft",
        fields=fields,
        provenance=provenance,
        rendered=rendered,
        gate_id=entry.get("gate"),
    )


def generate_builtin_documents(study: Study, doc_registry: Dict[str, dict]) -> Dict[str, Document]:
    """Generate every built-in template that the study requires."""
    docs: Dict[str, Document] = {}
    for doc_id in TEMPLATES:
        if doc_id in study.required_documents:
            docs[doc_id] = generate_document(study, doc_id, doc_registry)
    return docs


def import_existing_documents(study: Study, doc_registry: Dict[str, dict]) -> Dict[str, Document]:
    """Wrap pre-existing documents from the fixture as Document objects.

    These represent collected/imported artifacts (e.g., a protocol drafted
    before OSSICRO). Their field values carry provenance pointing at the
    imported artifact, not at the study record -- which is exactly what
    lets the consistency check catch drift between them.
    """
    docs: Dict[str, Document] = {}
    for item in study.raw.get("existing_documents", []):
        doc_id = item["doc_id"]
        entry = doc_registry.get(doc_id, {})
        fields = {k: str(v) for k, v in item.get("fields", {}).items() if str(v).strip()}
        provenance = [
            ProvenanceRecord(
                span=k,
                source="imported document %r field %r = %r" % (doc_id, k, v),
                citation="; ".join(entry.get("governing_citations", [])) or "imported",
            )
            for k, v in fields.items()
        ]
        docs[doc_id] = Document(
            doc_id=doc_id,
            title=entry.get("title", doc_id),
            state=item.get("state", "draft"),
            fields=fields,
            provenance=provenance,
            rendered=item.get("rendered", "(imported artifact - source file held in TMF)"),
            gate_id=entry.get("gate"),
        )
    return docs
