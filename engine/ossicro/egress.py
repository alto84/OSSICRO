"""INV-4: the de-identified egress gateway (BUILD-PLAN Wave 2, feature B).

THE single sanctioned outbound constructor for registry queries. This module
is the ONLY engine module besides ``review_claude.py`` permitted to import an
outbound HTTP client (``urllib.request``) — ``TestEngineEgressBoundary``
enforces that boundary. It must NEVER import the FHIR ingestion module or any
other chart-bearing path: the gateway sees only the closed
``DeidentifiedPredicates`` struct, never a chart, never an intake value.

WHAT MAY LEAVE THE MACHINE (the closed field set, nothing else):

    condition_codes   coded diagnoses (SNOMED CT / ICD-10-CM codes ONLY —
                      the codes are validated code-shaped; free text is
                      structurally unrepresentable)
    drug_name         a single drug-name token (no spaces -> no sentences)
    drug_rxnorm       an RxNorm concept id (digits only)
    age_band          a 5-year band ("55-59") with a "90+" top bucket per
                      45 CFR 164.514(b)(2)(i)(C) — never a raw age or DOB
    sex               male / female / other
    route_code        a SNOMED route-of-administration code (digits only)

No names, no dates, no geography, no identifiers, no free text. Construction
of the struct REJECTS any other field (frozen dataclass — an unknown keyword
is a TypeError) and rejects date-shaped or free-text-shaped values inside the
allowed fields (ValueError).

AGAINST INFERENCE EGRESS (Fable review SERIOUS 4) — identifiers are not the
only way to re-identify. Expanded access skews rare-disease, where a specific
condition code + age band + sex can be NATIONALLY UNIQUE. Two mitigations:

1. QUERY DECOMPOSITION (``decompose_query``): the outbound query carries the
   condition (and drug) ALONE. Age band, sex, and route are NEVER sent — they
   are filtered LOCALLY against the returned candidates' structured
   eligibility. A registry operator observing our queries learns a condition
   of interest, never a (condition, age, sex) triple.
2. RARE-CODE ROLL-UP (``roll_up_condition_codes``): ICD-10-CM extension codes
   are rolled up to their 3-character category before egress (C22.1 -> C22),
   so a maximally-specific rare subtype code does not leave the machine.

RESIDUAL RE-IDENTIFICATION RISK, stated honestly: the residual is real and
not fully closable at this layer. (a) SNOMED CT codes are sent as-is — we
have no local terminology server to roll them up a hierarchy, and a rare
SNOMED concept can itself be near-unique. (b) Even a rolled-up condition
category, combined with the query's source network address and timing,
tells the registry operator that SOMEONE at this clinic is preparing an
expanded-access request for that condition family — in a small community
that can be identifying. (c) Repeated queries across sessions are linkable
by the operator. These are accepted, documented residuals of querying any
external registry at all; the alternative (no query) is the only zero-risk
posture, and the mitigation for (b)/(c) is operational (query volume,
shared egress), not structural.

LIVE EGRESS IS DISABLED. Every call routes to a caller-supplied MOCK adapter
(``live=False``, the default). ``live=True`` raises ``EgressDisabled`` unless
the module-level greenlight flag is flipped — which it is not, and must not
be without Alton's explicit greenlight (HC2 adjacency). Every call — mock or
live — writes an ``egress_query`` audit record via ``ossicro.audit.append``.
"""

from __future__ import annotations

import re
import urllib.request  # noqa: F401 — THE sanctioned outbound import (unused until greenlight)
from dataclasses import dataclass, fields as dataclass_fields
from typing import Dict, List, Optional, Tuple

from . import audit as audit_mod

__all__ = [
    "ALLOWED_DESTINATIONS",
    "EgressDisabled",
    "DeidentifiedPredicates",
    "age_band_from_age",
    "roll_up_condition_codes",
    "decompose_query",
    "egress_query",
    "lint_free_text_identifiers",
]

# The ONLY hosts an outbound registry query may ever address (BUILD-PLAN
# Wave 2). Anything else is refused before any other work happens.
ALLOWED_DESTINATIONS = frozenset({
    "clinicaltrials.gov",
    "eutils.ncbi.nlm.nih.gov",   # NCBI E-utilities
    "api.fda.gov",               # openFDA
})

# GREENLIGHT FLAG — live egress stays OFF. Flipping this to True is the
# explicit human greenlight act for real external queries (HC2 adjacency);
# it must never be flipped by code, config, or a test. When greenlit, the
# live branch in ``egress_query`` below is where the urllib client goes.
_LIVE_EGRESS_ENABLED = False


class EgressDisabled(Exception):
    """Raised when a live external query is requested without the greenlight."""


# ---------------------------------------------------------------------------
# Value validation — the closed struct's walls
# ---------------------------------------------------------------------------

# A clinical code is EITHER SNOMED CT (6-18 digits) OR ICD-10-CM shaped
# (a letter, two digits, optional .extension). Nothing else — an all-alpha
# token ("Rivera"), a coded patient id ("PT3926.014"), and an 8-digit date
# ("19680314") all fail these shapes, so a name/identifier/date cannot pose
# as a condition code (review MAJOR-1). The two-shape check replaces the old
# permissive one-regex wall.
_SNOMED_RE = re.compile(r"^\d{6,18}$")
_ICD10_RE = re.compile(r"^[A-Za-z]\d{2}(?:\.[A-Za-z0-9]{1,4})?$")
# Date shapes we refuse anywhere (ISO, US-written, EU-written, and compact
# YYYYMMDD which would otherwise pass the SNOMED digit shape): a birth date
# smuggled into a "code" field must fail construction, not egress.
_DATE_RES = (
    re.compile(r"\d{4}-\d{1,2}-\d{1,2}"),
    re.compile(r"\d{1,2}/\d{1,2}/\d{2,4}"),
    re.compile(r"\d{1,2}\.\d{1,2}\.\d{4}"),
    re.compile(r"^(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])$"),  # YYYYMMDD
)
# A drug name: ONE token, letters/digits/hyphens. No spaces means no
# sentences, no "pt Jane Doe", no dosing narrative.
_DRUG_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9\-]{0,63}$")
_RXNORM_RE = re.compile(r"^\d{1,8}$")
_ROUTE_CODE_RE = re.compile(r"^\d{1,18}$")
_AGE_BAND_RE = re.compile(r"^(\d{1,2})-(\d{1,2})$")
_SEXES = ("male", "female", "other")


def _looks_like_date(value: str) -> bool:
    return any(rx.search(value) for rx in _DATE_RES)


def _check_code(code: object) -> str:
    ok = (isinstance(code, str)
          and not _looks_like_date(code)
          and (_SNOMED_RE.match(code) or _ICD10_RE.match(code)))
    if not ok:
        raise ValueError(
            "condition_codes accepts clinical codes only (SNOMED CT = 6-18 "
            "digits, or ICD-10-CM = letter+2 digits+optional .extension); got "
            "a value that is not code-shaped — free text, names, dates, and "
            "identifiers are structurally refused (INV-4)")
    return code


@dataclass(frozen=True)
class DeidentifiedPredicates:
    """The CLOSED set of facts allowed to leave the machine (INV-4).

    Frozen dataclass: an unknown keyword (patient_name=..., dob=..., any
    identifier) is a TypeError at construction — the struct has no place to
    put it. Values inside the allowed fields are shape-validated in
    ``__post_init__``: a date, a multi-word string, or a non-code-shaped
    "code" raises ValueError. Fail closed at construction, not at egress.
    """

    condition_codes: Tuple[str, ...] = ()
    drug_name: Optional[str] = None
    drug_rxnorm: Optional[str] = None
    age_band: Optional[str] = None
    sex: Optional[str] = None
    route_code: Optional[str] = None

    def __post_init__(self):
        codes = self.condition_codes
        if isinstance(codes, str) or not isinstance(codes, (list, tuple)):
            raise ValueError("condition_codes must be a list/tuple of codes")
        object.__setattr__(self, "condition_codes",
                           tuple(_check_code(c) for c in codes))
        if self.drug_name is not None and not _DRUG_NAME_RE.match(str(self.drug_name)):
            raise ValueError(
                "drug_name must be a single drug-name token (letters/digits/"
                "hyphens, no spaces) — free text is refused (INV-4)")
        if self.drug_rxnorm is not None and not _RXNORM_RE.match(str(self.drug_rxnorm)):
            raise ValueError("drug_rxnorm must be an RxNorm concept id (digits)")
        if self.age_band is not None:
            band = str(self.age_band)
            if band != "90+":
                m = _AGE_BAND_RE.match(band)
                if not m or int(m.group(1)) % 5 != 0 \
                        or int(m.group(2)) != int(m.group(1)) + 4 \
                        or int(m.group(1)) > 85:
                    raise ValueError(
                        "age_band must be a 5-year band ('55-59') or '90+' "
                        "(45 CFR 164.514) — never a raw age or date of birth")
        if self.sex is not None and self.sex not in _SEXES:
            raise ValueError("sex must be one of %s or None" % (_SEXES,))
        if self.route_code is not None and not _ROUTE_CODE_RE.match(str(self.route_code)):
            raise ValueError("route_code must be a SNOMED CT route code (digits)")

    # -- builder ----------------------------------------------------------

    @classmethod
    def from_profile(cls, committed_intake: Dict[str, object]) -> "DeidentifiedPredicates":
        """Derive predicates from a COMMITTED intake snapshot — and ONLY the
        closed field set. Everything else in the intake (names, addresses,
        narratives, dates, contact details) is structurally ignored: this
        builder reads exactly five intake keys and emits only validated,
        closed-vocabulary values.

        - ``patient.age`` -> a 5-year band with a "90+" top (never the raw age)
        - ``patient.sex`` -> normalized male/female/other, else absent
        - ``patient.diagnosis`` -> condition CODES from the closed local
          term->code table below; the diagnosis TEXT itself never leaves.
          An unrecognized diagnosis yields NO codes — honest absence, never
          a guess (INV-6).
        - ``drug.name`` -> a canonical token from the closed drug table ONLY;
          an investigational/unrecognized agent yields None (the raw drug
          text never leaves — review MAJOR-2)
        - ``drug.route`` -> a SNOMED route code from the closed local table,
          else absent
        """
        intake = committed_intake or {}
        return cls(
            condition_codes=_condition_codes_from_text(
                str(intake.get("patient.diagnosis", "") or "")),
            # Drug is derived through a CLOSED table, exactly like conditions —
            # raw drug.name text NEVER egresses (review MAJOR-2). An
            # investigational or unrecognized agent yields None (honest
            # absence); matching then proceeds on the condition axis. Growing
            # the table is how a drug becomes matchable — never by sending text.
            drug_name=_drug_from_text(str(intake.get("drug.name", "") or "")),
            drug_rxnorm=None,   # intake carries no RxNorm coding today
            age_band=age_band_from_age(intake.get("patient.age")),
            sex=_normalize_sex(str(intake.get("patient.sex", "") or "")),
            route_code=_route_code_from_text(
                str(intake.get("drug.route", "") or "")),
        )

    def as_dict(self) -> Dict[str, object]:
        """JSON-friendly view (tuples -> lists). Contract key for the drug
        name is ``drug`` per the shared /match contract."""
        return {
            "condition_codes": list(self.condition_codes),
            "drug": self.drug_name,
            "drug_rxnorm": self.drug_rxnorm,
            "age_band": self.age_band,
            "sex": self.sex,
            "route_code": self.route_code,
        }


# ---------------------------------------------------------------------------
# Local derivation tables — CLOSED vocabularies. Only values that appear
# below can ever be emitted; free intake text cannot pass through them.
# ---------------------------------------------------------------------------

# term (lowercased substring of the diagnosis narrative) -> clinical codes.
# The table is the wall: an unrecognized diagnosis emits NOTHING. Growing
# this table is how new conditions become matchable — never by sending text.
_CONDITION_TERM_CODES: Dict[str, Tuple[str, ...]] = {
    "cholangiocarcinoma": ("70179006", "C22.1"),
    "biliary tract cancer": ("70179006", "C22.1"),
    "amyotrophic lateral sclerosis": ("86044005", "G12.21"),
    "pancreatic adenocarcinoma": ("700423003", "C25.9"),
    "glioblastoma": ("393563007", "C71.9"),
}

# route text token -> SNOMED CT route-of-administration code.
_ROUTE_CODES: Dict[str, str] = {
    "oral": "26643006",
    "po": "26643006",
    "intravenous": "47625008",
    "iv": "47625008",
    "subcutaneous": "34206005",
    "intramuscular": "78421000",
    "topical": "6064005",
    "intrathecal": "72607000",
}


def _condition_codes_from_text(diagnosis: str) -> Tuple[str, ...]:
    text = " ".join(diagnosis.lower().split())
    out: List[str] = []
    for term, codes in sorted(_CONDITION_TERM_CODES.items()):
        if term in text:
            for code in codes:
                if code not in out:
                    out.append(code)
    return tuple(out)


# Known-agent name -> canonical token. A CLOSED vocabulary: an investigational
# or unrecognized drug name resolves to None so raw intake text can never leave
# (review MAJOR-2). Seeded with common oncology comparators; grow deliberately.
_DRUG_TERM_TOKENS: Dict[str, str] = {
    "gemcitabine": "gemcitabine", "cisplatin": "cisplatin",
    "oxaliplatin": "oxaliplatin", "fluorouracil": "fluorouracil",
    "pembrolizumab": "pembrolizumab", "nivolumab": "nivolumab",
    "durvalumab": "durvalumab",
}


def _drug_from_text(name: str) -> Optional[str]:
    text = " ".join(name.lower().split())
    for term, token in sorted(_DRUG_TERM_TOKENS.items()):
        if term in text:
            return token
    return None   # investigational / unrecognized -> honest absence, no text egress


def _normalize_sex(value: str) -> Optional[str]:
    v = value.strip().lower()
    if v in _SEXES:
        return v
    return {"f": "female", "m": "male"}.get(v)


def _route_code_from_text(route: str) -> Optional[str]:
    for token in re.sub(r"[^a-z0-9]+", " ", route.lower()).split():
        if token in _ROUTE_CODES:
            return _ROUTE_CODES[token]
    return None


def age_band_from_age(age: object) -> Optional[str]:
    """5-year band per 45 CFR 164.514: 58 -> '55-59'; >=90 -> '90+' (the
    safe-harbor top bucket). A missing / unparseable age yields None — never
    a guess."""
    try:
        years = int(str(age).strip())
    except (TypeError, ValueError):
        return None
    if years < 0:
        return None
    if years >= 90:
        return "90+"
    lo = (years // 5) * 5
    return "%d-%d" % (lo, lo + 4)


# ---------------------------------------------------------------------------
# Inference-egress mitigations
# ---------------------------------------------------------------------------

_ICD10_EXTENSION_RE = re.compile(r"^([A-Za-z]\d{2})\.")


def roll_up_condition_codes(codes) -> List[str]:
    """Roll ICD-10-CM extension codes up to their 3-character category
    (C22.1 -> C22) before egress — a maximally-specific rare-subtype code
    never leaves the machine. SNOMED CT codes pass through unchanged (no
    local hierarchy to climb; see the module docstring's residual-risk
    statement). Order-preserving, de-duplicated."""
    out: List[str] = []
    for code in codes:
        m = _ICD10_EXTENSION_RE.match(str(code))
        rolled = m.group(1) if m else str(code)
        if rolled not in out:
            out.append(rolled)
    return out


def decompose_query(predicates: "DeidentifiedPredicates"):
    """Split the predicates into (outbound, local_filters).

    ``outbound``: rolled-up condition codes + drug identity — the ONLY
    facts the wire ever carries. ``local_filters``: the field names whose
    values are withheld and applied locally against returned candidates
    (age band, sex, route). Querying the condition alone keeps the
    (condition, age, sex) triple — the rare-disease uniqueness vector —
    off the wire entirely.
    """
    outbound = {
        "condition_codes": roll_up_condition_codes(predicates.condition_codes),
        "drug_name": predicates.drug_name,
        "drug_rxnorm": predicates.drug_rxnorm,
    }
    local = [name for name, value in (("age_band", predicates.age_band),
                                      ("sex", predicates.sex),
                                      ("route_code", predicates.route_code))
             if value is not None]
    return outbound, local


# ---------------------------------------------------------------------------
# m20 (Overhaul P9): naive deterministic identifier lint over free text.
#
# Deliberately NAIVE — a handful of fixed patterns, no NLP, no judgment. It
# runs at release and egress time over the intake's FREE-TEXT fields (the
# caller selects them; typed date fields legitimately hold dates). It is
# ESCALATE-ONLY by construction: a warning names the FIELD and the pattern
# KIND — never the matched text (the warning itself must not re-leak the
# identifier), never a block, never a rewrite. A human decides what to do.
# ---------------------------------------------------------------------------

_LINT_NAME_ADJACENT_RE = re.compile(
    r"[Nn]ame\s*[:=]\s*[A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+")
_LINT_DOB_LABEL_RE = re.compile(
    r"(?i)\b(?:dob|date\s+of\s+birth|birth\s*date|born\s+on)\b")
_LINT_SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

# (kind, matcher(text) -> bool, human-readable description of the KIND).
_IDENTIFIER_LINTS = (
    ("ssn", lambda t: bool(_LINT_SSN_RE.search(t)),
     "a Social-Security-number-shaped value"),
    ("date-like", lambda t: _looks_like_date(t),
     "a date-shaped value (a DOB or treatment date in free text can identify)"),
    ("dob-label", lambda t: bool(_LINT_DOB_LABEL_RE.search(t)),
     "a date-of-birth label"),
    ("name-label", lambda t: bool(_LINT_NAME_ADJACENT_RE.search(t)),
     "a 'name:'-labeled capitalized name pair"),
)


def lint_free_text_identifiers(fields: Dict[str, object]) -> List[dict]:
    """Naive deterministic identifier lint (m20) over free-text fields.

    ``fields`` maps field_id -> value; non-string values are ignored. Returns
    one warning dict per (field, pattern-kind) hit:

        {"field_id": ..., "kind": ..., "message": ...}

    The message names the field and the pattern kind ONLY — never the matched
    text. Escalate-only: the caller surfaces the warnings; nothing is ever
    blocked or rewritten on their account.
    """
    warnings: List[dict] = []
    for field_id in sorted(fields):
        value = fields[field_id]
        if not isinstance(value, str) or not value.strip():
            continue
        for kind, hits, description in _IDENTIFIER_LINTS:
            if hits(value):
                warnings.append({
                    "field_id": field_id,
                    "kind": kind,
                    "message": (
                        "Possible direct identifier in free text: field "
                        "'%s' contains %s. Review and remove direct "
                        "identifiers (coded identifiers only) before any "
                        "real use — OSSICRO flags this; it never blocks or "
                        "rewrites your text." % (field_id, description)),
                })
    return warnings


# ---------------------------------------------------------------------------
# THE sanctioned outbound constructor
# ---------------------------------------------------------------------------

def egress_query(predicates: "DeidentifiedPredicates", destination: str, *,
                 adapter, trail: List[dict], actor: str = "",
                 live: bool = False) -> List[dict]:
    """The single sanctioned registry query (INV-4). Returns candidate dicts.

    Order of the walls, fail closed at each:
      1. only a ``DeidentifiedPredicates`` instance may pass (no raw dicts);
      2. ``destination`` must be on the allow-list;
      3. ``live=True`` raises ``EgressDisabled`` while the greenlight flag is
         off (it is off);
      4. the query is DECOMPOSED — rolled-up condition codes + drug only;
         age/sex/route never leave (they are the caller's local filters);
      5. one ``egress_query`` audit record is written (destination + the
         exact outbound facts + which fields were withheld) — for mock and
         live alike;
      6. the query goes to the MOCK adapter (live path disabled).
    """
    if not isinstance(predicates, DeidentifiedPredicates):
        raise TypeError(
            "egress_query accepts only a DeidentifiedPredicates struct — "
            "raw dicts cannot cross the egress boundary (INV-4)")
    if destination not in ALLOWED_DESTINATIONS:
        raise ValueError(
            "destination %r is not on the egress allow-list %s (INV-4)"
            % (destination, sorted(ALLOWED_DESTINATIONS)))
    if live and not _LIVE_EGRESS_ENABLED:
        raise EgressDisabled("egress disabled — requires greenlight")

    outbound, local_filters = decompose_query(predicates)

    audit_mod.append(
        trail, actor=actor, action="egress_query", target=destination,
        detail={
            "destination": destination,
            "condition_codes": list(outbound["condition_codes"]),
            "drug_name": outbound["drug_name"] or "",
            "drug_rxnorm": outbound["drug_rxnorm"] or "",
            "withheld_local_filters": local_filters,
            "decomposed": True,
            "live": bool(live),
        })

    if live:
        # GREENLIGHT MARKER: when _LIVE_EGRESS_ENABLED is flipped by an
        # explicit human greenlight, the real urllib.request client for the
        # allow-listed registry APIs is built HERE — and nowhere else in the
        # engine. Until then this branch is unreachable (the flag check
        # above raises first).
        raise EgressDisabled(
            "live egress is greenlit but no live registry client is "
            "implemented yet — build it at the GREENLIGHT MARKER")

    if adapter is None:
        raise ValueError("egress_query requires a registry adapter when live=False")
    return adapter.search(destination,
                          condition_codes=list(outbound["condition_codes"]),
                          drug_name=outbound["drug_name"],
                          drug_rxnorm=outbound["drug_rxnorm"])


# Guard: the dataclass field set IS the closed contract. If a future edit
# adds a field here without a design review, this trips immediately at import.
_EXPECTED_FIELDS = ("condition_codes", "drug_name", "drug_rxnorm",
                    "age_band", "sex", "route_code")
assert tuple(f.name for f in dataclass_fields(DeidentifiedPredicates)) == _EXPECTED_FIELDS
