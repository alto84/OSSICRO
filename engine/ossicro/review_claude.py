"""Model-backed concept reviewer (Claude adapter for the ConceptReviewer port).

This is the production stand-in for DeterministicStubReviewer: it judges a
document's prose against the cited writing principles using a model, running
Anthropic's critique step. It deliberately holds NO authority beyond flagging:
it does not import ossicro.gates, has no path to a sign-off, cannot clear a
gate, and cannot edit a locked span. Escalation coupling lives in
ossicro.pipeline; the defensive locked-span guard is ossicro.review_port.
validate_report, applied downstream.

Design for testability and safety:
- The model client is INJECTED (``ClaudeConceptReviewer(client, model)``), so
  tests run offline with a fake client and no key.
- ``from_anthropic(...)`` lazily imports the SDK and reads ANTHROPIC_API_KEY;
  it raises a clear, actionable error when either is absent rather than
  degrading silently.
- Temperature 0 and a pinned model id, for reproducibility.
- A malformed model response fails LOUDLY (ConceptReviewError) — a reviewer
  that cannot be parsed must not pass silently.

Selecting this reviewer is EGRESS (B1): rendered document text leaves the
machine for the Anthropic API. The app selects it only when
OSSICRO_LIVE_CONCEPT_REVIEW is affirmatively set — a deployment decision with
documented preconditions (BAA / zero retention / a named human on the log);
see docs/deployment/AI-REVIEW-PRECONDITIONS.md. Every live review writes one
``ai_review`` audit record (HC5) via the app, attributed with
``model_id``/``model_version`` below.
"""

from __future__ import annotations

import json
import os
import re
from typing import List, Optional

from .review_port import (
    ADVISORY_SEVERITY,
    HARD_SEVERITY,
    ConceptFinding,
    ConceptReviewer,
    Principle,
    ReviewReport,
    load_writing_principles,
)

DEFAULT_MODEL = "claude-sonnet-5"   # pinned; override per call site
_MAX_TOKENS = 2000

_SYSTEM = (
    "You are a senior regulatory-writing reviewer for clinical-trial submissions. "
    "You judge a DOCUMENT against a set of cited PRINCIPLES stated as text, using "
    "professional judgment — not a banned-word list. Return only defects a careful "
    "physician-signer would not adopt as their own work product.\n\n"
    "Rules you must obey:\n"
    "- Quote the exact offending text verbatim in `span`; never paraphrase evidence, "
    "and never cite text that is not present in the document.\n"
    "- Do not flag legitimate regulatory register (formal passives, 'shall', defined-term "
    "repetition, required boilerplate). Those are correct, not defects.\n"
    "- severity 'deficient' = a real defect that should block adoption; 'advisory' = a "
    "minor improvement. If the document is clean, return an empty list.\n"
    "- You judge and flag only. You never rewrite the document, never approve anything, "
    "and never make a regulatory determination.\n"
    "Respond with ONLY a JSON array of objects "
    '{"principle_id","severity","span","message","suggestion"} and nothing else.'
)


class ConceptReviewError(RuntimeError):
    """Raised when the model response cannot be parsed into findings."""


class ClaudeConceptReviewer(ConceptReviewer):
    """A ConceptReviewer backed by a Claude Messages client.

    ``client`` must expose ``messages.create(model=, max_tokens=, temperature=,
    system=, messages=[...])`` returning an object whose ``.content[0].text`` is
    the model's text (the Anthropic SDK shape). Inject a fake in tests.
    """

    def __init__(self, client, model: str = DEFAULT_MODEL, max_tokens: int = _MAX_TOKENS,
                 model_version: str = ""):
        self._client = client
        self.model = model
        # B1 full remediation (Overhaul P3 / HC5): the per-review ai_review
        # audit record names exactly which model saw the document text.
        # ``model_id`` is the pinned API model identifier; ``model_version``
        # defaults to that same pin (Anthropic model ids are themselves the
        # version pin) unless the deployment knows a finer-grained snapshot.
        # Never blank — the audit record always carries both.
        self.model_id = model
        self.model_version = model_version or model
        self._max_tokens = max_tokens

    @classmethod
    def from_anthropic(cls, model: str = DEFAULT_MODEL, api_key: Optional[str] = None):
        """Construct with a live Anthropic client. Lazy import; loud on absence."""
        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError(
                "ClaudeConceptReviewer.from_anthropic requires ANTHROPIC_API_KEY. "
                "Set it, pass api_key=, or use DeterministicStubReviewer for offline runs."
            )
        try:
            import anthropic  # noqa: WPS433 (lazy by design)
        except ImportError as exc:  # pragma: no cover - environment dependent
            raise RuntimeError(
                "The 'anthropic' package is not installed. `pip install anthropic`, "
                "or use DeterministicStubReviewer for offline runs."
            ) from exc
        return cls(anthropic.Anthropic(api_key=key), model=model)

    def _build_user_message(self, text: str, principles: List[Principle]) -> str:
        rubric = "\n".join("- [%s] %s (%s)" % (p.id, p.text, p.source) for p in principles)
        return "PRINCIPLES:\n%s\n\nDOCUMENT:\n<<<\n%s\n>>>" % (rubric, text)

    def _call(self, text: str, principles: List[Principle]) -> str:
        resp = self._client.messages.create(
            model=self.model, max_tokens=self._max_tokens, temperature=0,
            system=_SYSTEM,
            messages=[{"role": "user", "content": self._build_user_message(text, principles)}],
        )
        # Anthropic Messages shape: resp.content is a list of blocks with .text
        try:
            return "".join(getattr(b, "text", "") for b in resp.content)
        except Exception as exc:  # pragma: no cover
            raise ConceptReviewError("Unexpected model response shape: %r" % (resp,)) from exc

    @staticmethod
    def _parse(raw: str) -> List[dict]:
        raw = (raw or "").strip()
        # tolerate a code fence or leading prose; extract the first JSON array
        m = re.search(r"\[.*\]", raw, re.DOTALL)
        if not m:
            if raw in ("", "[]"):
                return []
            raise ConceptReviewError("No JSON array in model response: %r" % raw[:200])
        try:
            data = json.loads(m.group(0))
        except json.JSONDecodeError as exc:
            raise ConceptReviewError("Malformed JSON in model response: %s" % exc) from exc
        if not isinstance(data, list):
            raise ConceptReviewError("Model response was not a JSON array")
        return data

    def review(self, text: str, doc, principles: List[Principle]) -> ReviewReport:
        principles = principles or load_writing_principles()
        report = ReviewReport(model=self.model)
        for item in self._parse(self._call(text, principles)):
            sev = item.get("severity", ADVISORY_SEVERITY)
            if sev not in (HARD_SEVERITY, ADVISORY_SEVERITY):
                sev = ADVISORY_SEVERITY
            report.findings.append(
                ConceptFinding(
                    principle_id=str(item.get("principle_id", "")),
                    severity=sev,
                    span=str(item.get("span", "")),
                    message=str(item.get("message", "")),
                    suggestion=str(item.get("suggestion", "")),
                )
            )
        return report
