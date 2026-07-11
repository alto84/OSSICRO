"""Form FDA 3926 PDF / FDF export — hand-written PDF bytes, pure stdlib.

BUILD-PLAN Wave 3 item D. No pip dependencies (no reportlab / PyPDF): the PDF
file structure (objects, xref, trailer) and the FDF are assembled by hand.
No I/O, no network — this module extends the ``TestEngineEgressBoundary``
surface.

Two exports:

``render_3926_pdf(study_or_intake) -> bytes``
    A print-ready, letter-size PDF laying out the Form-3926 items with the
    case's intake values filled. Every page carries a diagonal
    "DRAFT — NOT FOR SUBMISSION" watermark and a footer stating the document
    is a draft for qualified human review. The watermark is part of each
    page's content stream — it stays until the gates clear because the ONLY
    render this module offers is the watermarked one (there is no flag to
    remove it; removing it is a code change, reviewed as such).

``fdf_3926(intake) -> bytes``
    A standard FDF (Forms Data Format) file that fills a real Form FDA 3926
    AcroForm when imported into it, keyed by ``FDF_3926_FIELD_MAP`` below.
    The FDF opens with DRAFT comment lines and fills the draft-marker field
    so the import itself carries the draft notice.

Both are value-faithful to intake: a missing field renders BLANK (PDF) or is
omitted (FDF) — nothing is fabricated, defaulted, or guessed (HC2). Nothing
here performs a non-delegable act: the signature blocks render as explicit
"physician signs by hand" notices, never as a filled signature (HC1).
"""

from __future__ import annotations

import textwrap
from typing import Dict, List, NamedTuple, Optional, Tuple

__all__ = [
    "WATERMARK_TEXT",
    "FOOTER_TEXT",
    "PENDING_NUMBERING_NOTE",
    "FORM_3926_MAP_VERIFIED_BY",
    "ITEM_BEST_KNOWN",
    "ITEM_LOCALLY_CONFIRMED",
    "ITEM_UNRESOLVED",
    "FormItem",
    "FORM_3926_ITEMS",
    "FDF_3926_FIELD_MAP",
    "pending_item_numbering_note",
    "item_citation",
    "render_3926_pdf",
    "fdf_3926",
]

# The watermark every page carries until the gates clear (BUILD-PLAN Wave 3:
# "DRAFT watermark retained until the gates clear — a filled 3926 is one
# email from a submission").
WATERMARK_TEXT = "DRAFT — NOT FOR SUBMISSION"

FOOTER_TEXT = ("DRAFT for qualified human review — OSSICRO drafts; it never "
               "signs, submits, or files (21 CFR 312.310; Constitution HC1).")

_SIGNATURE_NOTICE = ("SIGNATURE: __________________________________  DATE: __________  "
                     "[NON-DELEGABLE HUMAN ACT — gate: submission-to-fda. The "
                     "sponsor-investigator signs by hand; software cannot be a "
                     "sponsor (21 CFR 312.52).]")

_ATTESTATION_NOTE = ("[Fields 10.a / 10.b are physician attestations; OSSICRO "
                     "never defaults or auto-checks them.]")


# ---------------------------------------------------------------------------
# FORM_3926_ITEMS — the ONE item-number map (Overhaul P8, closes M6).
#
# Every 3926 render surface consumes this table: the text template's section
# order (ea_generators._FORM_3926_TEMPLATE headings), the print layout
# (_PDF_LAYOUT), and the FDF field-name map (FDF_3926_FIELD_MAP) are all
# DERIVED from it, so the three renders cannot disagree again.
# docs/route-3926-submission-spec.md §1.1 cites this table.
#
# PENDING-HUMAN-VERIFICATION — reconciliation provenance (P8):
#
#   Reconciled 2026-07-11 against the LOCAL
#   sources/fda-guidance/FDA_Expanded-Access-Form-3926-Instructions.pdf
#   (the June 2016 / updated October 2017 guidance "Individual Patient
#   Expanded Access Applications: Form FDA 3926", OMB 0910-0814). That
#   guidance CONFIRMS: the existence and waiver semantics of Fields 10.a
#   (§ 312.10 waiver of the additional part 312 / Form 1571+1572
#   requirements) and 10.b (§ 56.105 waiver of the § 56.108(c) convened-IRB
#   requirement, physician-signed), the OMB control number, and the
#   follow-up submission types (312.32(c), 312.32(d), 312.33, 312.310(c)(2),
#   312.30, 312.41, 312.42(e)). It does NOT enumerate items 1-9/11, so
#   those numbers/labels are the BEST-KNOWN target assembled from the wiki
#   corpus (wiki/03-documents/form-fda-3926-expanded-access.md) and the
#   route spec. The pre-P8 surfaces disagreed (template/PDF: LOA=6,
#   qualification=7, IRB=8, no item 9; spec §1.1: qualification=6,
#   rationale=9); they are reconciled HERE to: 3 = patient clinical
#   information (incl. rationale), 4 = treatment information, 5 = LOA,
#   6 = physician qualification statement, 7 = physician (requestor)
#   information, 8 = IRB, 9 = UNRESOLVED, 10 = waivers, 11 = signature.
#
# HUMAN CHECKLIST (blocks marker removal, nothing else):
#   1. Open the official fillable Form FDA 3926 (OMB 0910-0814) in a forms
#      inspector (e.g. `pdftk form3926.pdf dump_data_fields`).
#   2. Verify/correct every AcroForm name in this table (each field triple's
#      third element — they are UNVERIFIED PLACEHOLDERS; the official form
#      was deliberately not fetched: pilot rule, no external fetches).
#   3. Verify every item number and label — including whatever the real
#      item 9 is (UNRESOLVED below).
#   4. Initial the map: set FORM_3926_MAP_VERIFIED_BY = "Name, YYYY-MM-DD".
#      That single edit removes the pending-numbering marker from every
#      rendered surface. It never touches the DRAFT watermark — drafts stay
#      drafts until the gates clear (HC1).
# ---------------------------------------------------------------------------

# Set ONLY by a qualified human after completing the checklist above.
# None => every rendered surface carries PENDING_NUMBERING_NOTE.
FORM_3926_MAP_VERIFIED_BY: Optional[str] = None

# The visible P8 HITL marker (same style as citations.PENDING_FOOTER).
PENDING_NUMBERING_NOTE = (
    "[PENDING-HUMAN-VERIFICATION] Item numbering pending verification "
    "against the official Form FDA 3926 (OMB 0910-0814).")

# Item-map row statuses (what the LOCAL corpus supports, honestly).
ITEM_BEST_KNOWN = "BEST-KNOWN"              # assembled from wiki corpus + spec
ITEM_LOCALLY_CONFIRMED = "LOCALLY-CONFIRMED"  # named verbatim by the local guidance PDF
ITEM_UNRESOLVED = "UNRESOLVED"              # not derivable from the local corpus


class FormItem(NamedTuple):
    """One numbered item of the Form 3926 draft layout.

    ``fields``: (display label, intake field id, FDF AcroForm name or None).
    A None FDF name means the field renders in the layouts but is not an
    FDF fill target under this item (e.g. a display-only repeat).
    """
    number: str                                        # "1" .. "11"
    label: str
    fields: Tuple[Tuple[str, str, Optional[str]], ...]
    status: str                                        # ITEM_* above
    note: str = ""


FORM_3926_ITEMS: Tuple[FormItem, ...] = (
    FormItem("1", "DATE OF SUBMISSION", (), ITEM_BEST_KNOWN,
             "Filled from the physician-entered anchor date (submission.date) "
             "at generate time; never the wall clock."),
    FormItem("2", "NATURE OF SUBMISSION", (
        ("Initial or follow-up", "submission.initial_or_followup",
         "3926_02_initial_or_followup"),
        ("Emergency request", "submission.emergency", "3926_02_emergency"),
        ("IND number (if follow-up to an existing IND)",
         "submission.ind_number", "3926_02_ind_number"),
    ), ITEM_BEST_KNOWN,
             "The local guidance confirms the follow-up submission types "
             "(312.32(c)/(d), 312.33, 312.310(c)(2), 312.30, 312.41, "
             "312.42(e)) but not the item number."),
    FormItem("3", "PATIENT'S CLINICAL INFORMATION", (
        ("Patient identifier (coded - no direct identifiers)",
         "patient.coded_id", "3926_03_patient_identifier"),
        ("Age", "patient.age", "3926_03_age"),
        ("Sex", "patient.sex", "3926_03_sex"),
        ("Diagnosis / condition", "patient.diagnosis", "3926_03_diagnosis"),
        ("Prior therapies and outcomes", "patient.prior_therapies",
         "3926_03_prior_therapies"),
        ("Clinical rationale (21 CFR 312.305(a))",
         "request.clinical_rationale", "3926_03_clinical_rationale"),
    ), ITEM_BEST_KNOWN,
             "Diagnosis, history/current status, prior therapies, and the "
             "rationale for the treatment request (the spec previously "
             "placed the rationale at Field 9 — reconciled here to item 3)."),
    FormItem("4", "TREATMENT INFORMATION", (
        ("Investigational drug name", "drug.name", "3926_04_drug_name"),
        ("Manufacturer / source", "manufacturer.name", "3926_04_manufacturer"),
        ("Treatment plan summary (full plan attached)",
         "treatment.benefit_risk", "3926_04_treatment_plan_summary"),
        ("Dose", "drug.dose", "3926_04_dose"),
        ("Route", "drug.route", "3926_04_route"),
        ("Planned duration", "drug.duration", "3926_04_duration"),
        ("Monitoring", "treatment.monitoring_plan", "3926_04_monitoring"),
    ), ITEM_BEST_KNOWN,
             "Drug + treatment plan merged under one item (pre-P8 the "
             "template split them across items 4 and 5)."),
    FormItem("5", "LETTER OF AUTHORIZATION (LOA)", (
        ("LOA cross-references application",
         "manufacturer.ind_dmf_reference", "3926_05_loa_reference"),
    ), ITEM_BEST_KNOWN, "Pre-P8 the template numbered the LOA as item 6."),
    FormItem("6", "PHYSICIAN'S QUALIFICATION STATEMENT", (
        ("Physician", "investigator.name", None),
        ("Degrees", "investigator.degrees", "3926_06_degrees"),
        ("License number", "investigator.license_number",
         "3926_06_license_number"),
        ("License state", "investigator.license_state",
         "3926_06_license_state"),
        ("312.310(a) determination (risk drug <= risk disease)",
         "investigator.risk_determination", "3926_06_risk_determination"),
    ), ITEM_BEST_KNOWN,
             "Matches the route spec (qualification = Field 6); pre-P8 the "
             "template numbered it 7."),
    FormItem("7", "PHYSICIAN INFORMATION (REQUESTOR / SPONSOR-INVESTIGATOR)", (
        ("Name", "investigator.name", "3926_07_physician_name"),
        ("Address", "investigator.address", "3926_07_address"),
        ("Phone", "investigator.phone", "3926_07_phone"),
        ("Email", "investigator.email", "3926_07_email"),
    ), ITEM_BEST_KNOWN,
             "Pre-P8 the template numbered the requestor block 11 while its "
             "provenance citations said field 10 — reconciled to item 7."),
    FormItem("8", "INSTITUTIONAL REVIEW BOARD (IRB) INFORMATION", (
        ("IRB of record", "irb.name", "3926_08_irb_name"),
    ), ITEM_BEST_KNOWN, ""),
    FormItem("9", "[UNRESOLVED - TRANSCRIBE FROM THE OFFICIAL FORM AT THE "
                  "HUMAN PASS]", (), ITEM_UNRESOLVED,
             "The local instructions/guidance PDF never enumerates item 9 "
             "and the corpus does not resolve it. Rendered as an explicit "
             "unresolved slot — honestly absent, never guessed (HC2)."),
    FormItem("10", "REQUEST FOR AUTHORIZATION (WAIVERS - PHYSICIAN "
                   "ATTESTATIONS)", (
        ("10.a Waiver (312.10 - waive 1571/1572 requirements)", "waiver_10a",
         "3926_10a_waiver_312_10"),
        ("10.b Waiver (56.105 - chair concurrence)", "waiver_10b",
         "3926_10b_waiver_56_105"),
    ), ITEM_LOCALLY_CONFIRMED,
             "Field numbers 10.a/10.b and their waiver semantics are named "
             "verbatim by the local guidance PDF (sections III-IV). The "
             "AcroForm names remain unverified placeholders."),
    FormItem("11", "PHYSICIAN SIGNATURE AND DATE", (), ITEM_BEST_KNOWN,
             "Non-delegable human act (gate: submission-to-fda); renders as "
             "a sign-by-hand notice, never a filled signature (HC1)."),
)


def pending_item_numbering_note() -> str:
    """The P8 HITL marker line, or '' once a human has initialed the map.

    Reads FORM_3926_MAP_VERIFIED_BY at call time: the marker disappears from
    rendered surfaces ONLY via the human edit of that constant.
    """
    return "" if FORM_3926_MAP_VERIFIED_BY else PENDING_NUMBERING_NOTE


def item_citation(number: str) -> str:
    """A provenance citation for a Form 3926 item reference, honest about
    the verification state of the item map."""
    base = "Form FDA 3926 item %s (OMB 0910-0814)" % number
    if FORM_3926_MAP_VERIFIED_BY:
        return base
    return base + " [item numbering PENDING-HUMAN-VERIFICATION]"


# The FDF field-name map, DERIVED from FORM_3926_ITEMS: OSSICRO intake field
# ids (routes.json schema — the same ids gen_form_3926 consumes) -> the FDA
# Form 3926 AcroForm names the FDF targets. The right-hand names are
# UNVERIFIED PLACEHOLDERS (TODO HUMAN-VERIFY — see the checklist above);
# until the human pass, the FDF is synthetic-only.
FDF_3926_FIELD_MAP: Dict[str, str] = {
    intake_id: fdf_name
    for item in FORM_3926_ITEMS
    for (_label, intake_id, fdf_name) in item.fields
    if fdf_name
}

# The print layout, DERIVED from FORM_3926_ITEMS: (numbered heading,
# [(label, intake field id), ...]) in the table's item order.
_PDF_LAYOUT: List[Tuple[str, List[Tuple[str, str]]]] = [
    ("%s. %s" % (item.number, item.label),
     [(label, intake_id) for (label, intake_id, _fdf) in item.fields])
    for item in FORM_3926_ITEMS
]

# --- page geometry (US Letter, points) --------------------------------------
_PAGE_W, _PAGE_H = 612, 792
_MARGIN = 54
_BODY_SIZE = 9
_LABEL_SIZE = 9
_HEAD_SIZE = 10
_TITLE_SIZE = 12
_LEADING = 12
_WRAP_COLS = 96          # conservative for 9pt Helvetica in a 504pt column
_FOOTER_Y = 30


# ---------------------------------------------------------------------------
# Value resolution — value-faithful, missing renders blank
# ---------------------------------------------------------------------------

def _resolve(source, field_id: str) -> str:
    """The intake value as text, or "" when honestly absent.

    ``source`` is either a flat dotted-key intake dict or a Study (anything
    with a ``resolve`` method). No defaults, no fabrication: None / blank
    stays blank.
    """
    if hasattr(source, "resolve"):
        value = source.resolve(field_id)
    elif isinstance(source, dict):
        value = source.get(field_id)
    else:
        raise TypeError("render_3926_pdf expects a Study or a flat intake dict")
    if value is None:
        return ""
    text = str(value)
    return "" if text.strip() == "" else text


# ---------------------------------------------------------------------------
# PDF primitives
# ---------------------------------------------------------------------------

def _pdf_escape(text: str) -> bytes:
    """A PDF literal-string body: cp1252 (WinAnsi) bytes, specials escaped.

    ASCII passes through untouched (so filled values stay byte-searchable in
    the output); non-WinAnsi characters degrade to '?' rather than corrupting
    the file; bytes outside the printable range are octal-escaped.
    """
    data = str(text).encode("cp1252", "replace")
    out = bytearray()
    for b in data:
        if b in (0x28, 0x29, 0x5C):          # ( ) backslash
            out += b"\\" + bytes([b])
        elif 32 <= b <= 126:
            out.append(b)
        else:
            out += ("\\%03o" % b).encode("ascii")
    return bytes(out)


def _text_op(x: float, y: float, size: float, text: str,
             font: bytes = b"/F1", gray: float = 0.0) -> bytes:
    return (b"BT " + font + (" %g Tf %g g 1 0 0 1 %g %g Tm (" % (size, gray, x, y))
            .encode("ascii") + _pdf_escape(text) + b") Tj ET\n")


def _watermark_op() -> bytes:
    """The diagonal DRAFT watermark, drawn under the body text of every page."""
    # 45-degree rotation matrix (cos/sin = 0.7071), light gray, large type.
    return (b"q BT /F2 42 Tf 0.82 g 0.7071 0.7071 -0.7071 0.7071 96 150 Tm ("
            + _pdf_escape(WATERMARK_TEXT) + b") Tj ET Q\n")


def _wrap_value(text: str, cols: int = _WRAP_COLS) -> List[str]:
    lines: List[str] = []
    for raw in (str(text).splitlines() or [""]):
        wrapped = textwrap.wrap(raw, cols) if raw.strip() else [""]
        lines.extend(wrapped or [""])
    return lines or [""]


def _build_pdf(page_streams: List[bytes]) -> bytes:
    """Assemble a complete PDF: catalog, page tree, two fonts, N pages."""
    # Object numbering: 1 catalog, 2 pages, 3 F1 (Helvetica), 4 F2 (bold),
    # then per page i: page object (5 + 2i) and its content stream (6 + 2i).
    n_pages = len(page_streams)
    objects: List[bytes] = []
    kids = b" ".join(("%d 0 R" % (5 + 2 * i)).encode("ascii") for i in range(n_pages))
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")                       # 1
    objects.append(b"<< /Type /Pages /Kids [" + kids +
                   (b"] /Count %d >>" % n_pages))                              # 2
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica"
                   b" /Encoding /WinAnsiEncoding >>")                          # 3
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold"
                   b" /Encoding /WinAnsiEncoding >>")                          # 4
    for i, stream in enumerate(page_streams):
        objects.append((
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] "
            "/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> "
            "/Contents %d 0 R >>" % (_PAGE_W, _PAGE_H, 6 + 2 * i)
        ).encode("ascii"))
        objects.append((b"<< /Length %d >>\nstream\n" % len(stream))
                       + stream + b"\nendstream")

    buf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]  # object 0 is the free head
    for num, body in enumerate(objects, start=1):
        offsets.append(len(buf))
        buf += (b"%d 0 obj\n" % num) + body + b"\nendobj\n"
    xref_at = len(buf)
    buf += ("xref\n0 %d\n" % (len(objects) + 1)).encode("ascii")
    buf += b"0000000000 65535 f \n"
    for off in offsets[1:]:
        buf += ("%010d 00000 n \n" % off).encode("ascii")
    buf += ("trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n"
            % (len(objects) + 1, xref_at)).encode("ascii")
    buf += b"%%EOF\n"
    return bytes(buf)


# ---------------------------------------------------------------------------
# render_3926_pdf
# ---------------------------------------------------------------------------

def render_3926_pdf(study_or_intake) -> bytes:
    """A print-ready, DRAFT-watermarked PDF of the filled Form 3926 layout.

    ``study_or_intake`` is a Study or the flat dotted-key intake dict. Values
    are laid out verbatim under the form's item headings; a missing field
    renders as a blank value line — honestly absent, never fabricated.
    """
    # Build the logical line list first: (kind, text) where kind selects font
    # and indent. Pagination happens after. Section order/numbering comes
    # from the ONE item map (FORM_3926_ITEMS) — heading softened to a draft
    # layout, never presented as the official form (P8).
    lines: List[Tuple[str, str]] = [
        ("title", "FORM FDA 3926 (DRAFT LAYOUT) — INDIVIDUAL PATIENT EXPANDED ACCESS IND"),
        ("meta", "Authority: 21 CFR 312.310; Form FDA 3926 (OMB 0910-0814)"),
        ("meta", "DRAFT — for qualified human review; not for submission."),
    ]
    numbering_note = pending_item_numbering_note()
    if numbering_note:
        lines.append(("meta", numbering_note))
    lines.append(("blank", ""))
    for item in FORM_3926_ITEMS:
        lines.append(("head", "%s. %s" % (item.number, item.label)))
        for label, field_id, _fdf in item.fields:
            value = _resolve(study_or_intake, field_id)
            value_lines = _wrap_value(value)
            # Short values inline with the label; long/multi-line below it.
            if len(value_lines) == 1 and len(label) + len(value_lines[0]) <= _WRAP_COLS:
                lines.append(("field", "%s: %s" % (label, value_lines[0])))
            else:
                lines.append(("field", "%s:" % label))
                for vl in value_lines:
                    lines.append(("value", vl))
        if item.status == ITEM_UNRESOLVED:
            for wrapped in textwrap.wrap(
                    "[UNRESOLVED - the local Form-3926 instructions/guidance "
                    "does not enumerate this item; the human pass transcribes "
                    "it from the official fillable form.]", _WRAP_COLS):
                lines.append(("note", wrapped))
        if item.number == "10":
            lines.append(("note", _ATTESTATION_NOTE))
        if item.number == "11":
            for wrapped in textwrap.wrap(_SIGNATURE_NOTICE, _WRAP_COLS):
                lines.append(("note", wrapped))
        lines.append(("blank", ""))

    # Paginate and emit content streams.
    styles = {
        "title": (b"/F2", _TITLE_SIZE, 0.0, _MARGIN),
        "meta":  (b"/F1", _BODY_SIZE, 0.35, _MARGIN),
        "head":  (b"/F2", _HEAD_SIZE, 0.0, _MARGIN),
        "field": (b"/F1", _LABEL_SIZE, 0.0, _MARGIN),
        "value": (b"/F1", _BODY_SIZE, 0.0, _MARGIN + 14),
        "note":  (b"/F1", _BODY_SIZE, 0.3, _MARGIN),
        "blank": (b"/F1", _BODY_SIZE, 0.0, _MARGIN),
    }
    top_y = _PAGE_H - _MARGIN
    bottom_y = _FOOTER_Y + 2 * _LEADING
    pages: List[bytearray] = []
    stream = bytearray(_watermark_op())
    y = top_y
    for kind, text in lines:
        if y < bottom_y:
            pages.append(stream)
            stream = bytearray(_watermark_op())
            y = top_y
        if kind == "blank":
            y -= _LEADING // 2
            continue
        font, size, gray, x = styles[kind]
        stream += _text_op(x, y, size, text, font=font, gray=gray)
        y -= _LEADING if kind != "title" else _LEADING + 4
    pages.append(stream)

    n = len(pages)
    for i, page in enumerate(pages, start=1):
        if numbering_note:
            # P8 HITL marker: every page's footer says the item numbering is
            # pending until a human initials FORM_3926_MAP_VERIFIED_BY.
            page += _text_op(_MARGIN, _FOOTER_Y + _LEADING, 7.5,
                             numbering_note, gray=0.25)
        page += _text_op(_MARGIN, _FOOTER_Y, 7.5,
                         "%s   Page %d of %d" % (FOOTER_TEXT, i, n), gray=0.25)
    return _build_pdf([bytes(p) for p in pages])


# ---------------------------------------------------------------------------
# fdf_3926
# ---------------------------------------------------------------------------

def fdf_3926(intake: Dict[str, object]) -> bytes:
    """A standard FDF that fills the official Form 3926 AcroForm.

    Keyed by ``FDF_3926_FIELD_MAP``, derived from ``FORM_3926_ITEMS``
    (UNVERIFIED right-hand names until the P8 human checklist above is
    completed). Only mapped schema fields with present
    values are emitted; an absent value is omitted, never fabricated. The
    file opens with DRAFT comment lines and carries a draft-marker field so
    the import itself announces its draft status.
    """
    if hasattr(intake, "resolve"):
        source = intake
    elif isinstance(intake, dict):
        source = dict(intake)
    else:
        raise TypeError("fdf_3926 expects a flat intake dict (or a Study)")

    entries: List[bytes] = []
    for intake_id in sorted(FDF_3926_FIELD_MAP):
        value = _resolve(source, intake_id)
        if value == "":
            continue  # honestly absent — the form field stays empty
        entries.append(b"<< /T (" + _pdf_escape(FDF_3926_FIELD_MAP[intake_id])
                       + b") /V (" + _pdf_escape(value) + b") >>")
    # Draft marker travels IN the data, not only in comments: any viewer that
    # imports this FDF shows the draft notice in the marker field. The
    # verification clause is honest about the item map's state (P8).
    if FORM_3926_MAP_VERIFIED_BY:
        map_state = ("field-name map verified by %s."
                     % FORM_3926_MAP_VERIFIED_BY)
    else:
        map_state = ("field-name map and item numbering unverified "
                     "(TODO HUMAN-VERIFY; PENDING-HUMAN-VERIFICATION "
                     "against the official Form FDA 3926, OMB 0910-0814).")
    entries.append(b"<< /T (ossicro_draft_notice) /V ("
                   + _pdf_escape(WATERMARK_TEXT + " — draft for qualified "
                                 "human review; " + map_state) + b") >>")

    buf = bytearray()
    buf += b"%FDF-1.2\n"
    buf += b"% " + _pdf_escape(WATERMARK_TEXT) + b"\n"
    if FORM_3926_MAP_VERIFIED_BY:
        buf += (b"% DRAFT export from OSSICRO. Field-name/item map verified by "
                + _pdf_escape(FORM_3926_MAP_VERIFIED_BY)
                + b" (see pdf_3926.FORM_3926_ITEMS).\n")
    else:
        buf += (b"% DRAFT export from OSSICRO. Field names in this file are "
                b"UNVERIFIED placeholders (TODO HUMAN-VERIFY against the official "
                b"Form FDA 3926 AcroForm). Synthetic-only through the pilot.\n")
        buf += b"% " + _pdf_escape(PENDING_NUMBERING_NOTE) + b"\n"
    buf += b"1 0 obj\n<< /FDF << /Fields [\n"
    for entry in entries:
        buf += entry + b"\n"
    buf += b"] >> >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF\n"
    return bytes(buf)
