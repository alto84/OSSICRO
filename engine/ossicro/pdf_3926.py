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
from typing import Dict, List, Optional, Tuple

__all__ = [
    "WATERMARK_TEXT",
    "FOOTER_TEXT",
    "FDF_3926_FIELD_MAP",
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
# TODO(HUMAN-VERIFY) — FDF field-name map.
#
# Left-hand side: OSSICRO intake field ids (the route schema in
# engine/registry/routes.json — the SAME ids gen_form_3926 consumes).
# Right-hand side: the FDA Form 3926 AcroForm field names the FDF targets.
#
# The right-hand names are UNVERIFIED PLACEHOLDERS written in a plain
# readable style. The official fillable Form FDA 3926 (OMB 0910-0814) was
# deliberately NOT fetched (pilot rule: no external fetches); before any
# real import, a human must open the official form in a forms inspector
# (e.g. pdftk dump_data_fields) and correct each right-hand name in this one
# dict. Until that verification pass, the FDF is synthetic-only.
# ---------------------------------------------------------------------------
FDF_3926_FIELD_MAP: Dict[str, str] = {
    # Item 2 — type of submission
    "submission.initial_or_followup": "3926_02_initial_or_followup",  # TODO(HUMAN-VERIFY)
    "submission.emergency":           "3926_02_emergency",            # TODO(HUMAN-VERIFY)
    "submission.ind_number":          "3926_02_ind_number",           # TODO(HUMAN-VERIFY)
    # Item 3 — patient information and clinical presentation
    "patient.coded_id":               "3926_03_patient_identifier",   # TODO(HUMAN-VERIFY)
    "patient.age":                    "3926_03_age",                  # TODO(HUMAN-VERIFY)
    "patient.sex":                    "3926_03_sex",                  # TODO(HUMAN-VERIFY)
    "patient.diagnosis":              "3926_03_diagnosis",            # TODO(HUMAN-VERIFY)
    "patient.prior_therapies":        "3926_03_prior_therapies",      # TODO(HUMAN-VERIFY)
    "request.clinical_rationale":     "3926_03_clinical_rationale",   # TODO(HUMAN-VERIFY)
    # Item 4 — investigational drug
    "drug.name":                      "3926_04_drug_name",            # TODO(HUMAN-VERIFY)
    "manufacturer.name":              "3926_04_manufacturer",         # TODO(HUMAN-VERIFY)
    # Item 5 — treatment plan
    "treatment.benefit_risk":         "3926_05_treatment_plan_summary",  # TODO(HUMAN-VERIFY)
    "drug.dose":                      "3926_05_dose",                 # TODO(HUMAN-VERIFY)
    "drug.route":                     "3926_05_route",                # TODO(HUMAN-VERIFY)
    "drug.duration":                  "3926_05_duration",             # TODO(HUMAN-VERIFY)
    "treatment.monitoring_plan":      "3926_05_monitoring",           # TODO(HUMAN-VERIFY)
    # Item 6 — letter of authorization
    "manufacturer.ind_dmf_reference": "3926_06_loa_reference",        # TODO(HUMAN-VERIFY)
    # Item 7 — physician qualification statement
    "investigator.license_number":    "3926_07_license_number",       # TODO(HUMAN-VERIFY)
    "investigator.license_state":     "3926_07_license_state",        # TODO(HUMAN-VERIFY)
    "investigator.risk_determination": "3926_07_risk_determination",  # TODO(HUMAN-VERIFY)
    # Item 8 — IRB
    "irb.name":                       "3926_08_irb_name",             # TODO(HUMAN-VERIFY)
    # Item 10 — waivers (physician attestations, passed through verbatim)
    "waiver_10a":                     "3926_10a_waiver_312_10",       # TODO(HUMAN-VERIFY)
    "waiver_10b":                     "3926_10b_waiver_56_105",       # TODO(HUMAN-VERIFY)
    # Item 11 — physician (requestor / sponsor-investigator)
    "investigator.name":              "3926_11_physician_name",       # TODO(HUMAN-VERIFY)
    "investigator.degrees":           "3926_11_degrees",              # TODO(HUMAN-VERIFY)
    "investigator.address":           "3926_11_address",              # TODO(HUMAN-VERIFY)
    "investigator.phone":             "3926_11_phone",                # TODO(HUMAN-VERIFY)
    "investigator.email":             "3926_11_email",                # TODO(HUMAN-VERIFY)
}

# The print layout: (section heading, [(label, intake field id), ...]) in the
# 3926's own item order. Same ids as FDF_3926_FIELD_MAP / gen_form_3926.
_PDF_LAYOUT: List[Tuple[str, List[Tuple[str, str]]]] = [
    ("2. TYPE OF SUBMISSION", [
        ("Initial or follow-up", "submission.initial_or_followup"),
        ("Emergency request", "submission.emergency"),
        ("IND number (if existing)", "submission.ind_number"),
    ]),
    ("3. PATIENT INFORMATION AND CLINICAL PRESENTATION", [
        ("Patient identifier (coded - no direct identifiers)", "patient.coded_id"),
        ("Age", "patient.age"),
        ("Sex", "patient.sex"),
        ("Diagnosis / condition", "patient.diagnosis"),
        ("Prior therapies and outcomes", "patient.prior_therapies"),
        ("Clinical rationale (21 CFR 312.305(a))", "request.clinical_rationale"),
    ]),
    ("4. INVESTIGATIONAL DRUG", [
        ("Name", "drug.name"),
        ("Manufacturer / source", "manufacturer.name"),
    ]),
    ("5. TREATMENT PLAN (summary; full plan attached)", [
        ("Summary", "treatment.benefit_risk"),
        ("Dose", "drug.dose"),
        ("Route", "drug.route"),
        ("Planned duration", "drug.duration"),
        ("Monitoring", "treatment.monitoring_plan"),
    ]),
    ("6. LETTER OF AUTHORIZATION", [
        ("LOA cross-references application", "manufacturer.ind_dmf_reference"),
    ]),
    ("7. PHYSICIAN QUALIFICATION STATEMENT", [
        ("Physician", "investigator.name"),
        ("Degrees", "investigator.degrees"),
        ("License number", "investigator.license_number"),
        ("License state", "investigator.license_state"),
        ("312.310(a) determination (risk drug <= risk disease)",
         "investigator.risk_determination"),
    ]),
    ("8. INSTITUTIONAL REVIEW BOARD", [
        ("IRB of record", "irb.name"),
    ]),
    ("10. WAIVERS (physician attestations)", [
        ("10.a Waiver (312.10 - waive 1571/1572 requirements)", "waiver_10a"),
        ("10.b Waiver (56.105 - chair concurrence)", "waiver_10b"),
    ]),
    ("11. PHYSICIAN (REQUESTOR / SPONSOR-INVESTIGATOR)", [
        ("Name", "investigator.name"),
        ("Address", "investigator.address"),
        ("Phone", "investigator.phone"),
        ("Email", "investigator.email"),
    ]),
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
    # and indent. Pagination happens after.
    lines: List[Tuple[str, str]] = [
        ("title", "FORM FDA 3926 — INDIVIDUAL PATIENT EXPANDED ACCESS IND"),
        ("meta", "Authority: 21 CFR 312.310; Form FDA 3926 (OMB 0910-0814)"),
        ("meta", "DRAFT — for qualified human review; not for submission."),
        ("blank", ""),
    ]
    for heading, fields in _PDF_LAYOUT:
        lines.append(("head", heading))
        for label, field_id in fields:
            value = _resolve(study_or_intake, field_id)
            value_lines = _wrap_value(value)
            # Short values inline with the label; long/multi-line below it.
            if len(value_lines) == 1 and len(label) + len(value_lines[0]) <= _WRAP_COLS:
                lines.append(("field", "%s: %s" % (label, value_lines[0])))
            else:
                lines.append(("field", "%s:" % label))
                for vl in value_lines:
                    lines.append(("value", vl))
        if heading.startswith("10."):
            lines.append(("note", _ATTESTATION_NOTE))
        lines.append(("blank", ""))
    lines.append(("blank", ""))
    for wrapped in textwrap.wrap(_SIGNATURE_NOTICE, _WRAP_COLS):
        lines.append(("note", wrapped))

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
        page += _text_op(_MARGIN, _FOOTER_Y, 7.5,
                         "%s   Page %d of %d" % (FOOTER_TEXT, i, n), gray=0.25)
    return _build_pdf([bytes(p) for p in pages])


# ---------------------------------------------------------------------------
# fdf_3926
# ---------------------------------------------------------------------------

def fdf_3926(intake: Dict[str, object]) -> bytes:
    """A standard FDF that fills the official Form 3926 AcroForm.

    Keyed by ``FDF_3926_FIELD_MAP`` (UNVERIFIED right-hand names — see the
    TODO(HUMAN-VERIFY) block above). Only mapped schema fields with present
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
    # imports this FDF shows the draft notice in the marker field.
    entries.append(b"<< /T (ossicro_draft_notice) /V ("
                   + _pdf_escape(WATERMARK_TEXT + " — draft for qualified "
                                 "human review; field-name map unverified "
                                 "(TODO HUMAN-VERIFY).") + b") >>")

    buf = bytearray()
    buf += b"%FDF-1.2\n"
    buf += b"% " + _pdf_escape(WATERMARK_TEXT) + b"\n"
    buf += (b"% DRAFT export from OSSICRO. Field names in this file are "
            b"UNVERIFIED placeholders (TODO HUMAN-VERIFY against the official "
            b"Form FDA 3926 AcroForm). Synthetic-only through the pilot.\n")
    buf += b"1 0 obj\n<< /FDF << /Fields [\n"
    for entry in entries:
        buf += entry + b"\n"
    buf += b"] >> >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF\n"
    return bytes(buf)
