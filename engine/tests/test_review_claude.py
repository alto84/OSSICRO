"""Claude concept-reviewer tests (offline; fake client). No network, no key.
Run: `cd engine && python -m unittest tests.test_review_claude -v`."""

import inspect
import unittest

from ossicro import review_claude
from ossicro.review_claude import ClaudeConceptReviewer, ConceptReviewError
from ossicro.review_port import load_writing_principles, validate_report
from ossicro.models import Document


class _Block:
    def __init__(self, text):
        self.text = text


class _Resp:
    def __init__(self, text):
        self.content = [_Block(text)]


class _FakeClient:
    """Records the call and returns a canned Messages response."""
    def __init__(self, text):
        self._text = text
        self.last_kwargs = None
        self.messages = self

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        return _Resp(self._text)


PRINCIPLES = load_writing_principles()


class ParsingTests(unittest.TestCase):
    def test_parses_findings(self):
        client = _FakeClient('[{"principle_id":"P2","severity":"deficient",'
                             '"span":"cutting-edge","message":"promotional","suggestion":"delete"}]')
        r = ClaudeConceptReviewer(client).review("We offer a cutting-edge platform.", None, PRINCIPLES)
        self.assertEqual(len(r.findings), 1)
        self.assertEqual(r.findings[0].principle_id, "P2")
        self.assertTrue(r.findings[0].is_hard)
        self.assertEqual(r.model, review_claude.DEFAULT_MODEL)

    def test_empty_is_clean(self):
        r = ClaudeConceptReviewer(_FakeClient("[]")).review("The sponsor shall report.", None, PRINCIPLES)
        self.assertEqual(r.findings, [])

    def test_tolerates_code_fence_and_prose(self):
        client = _FakeClient('Here are the findings:\n```json\n[{"principle_id":"P4","severity":"advisory",'
                             '"span":"It is important to note","message":"metacommentary"}]\n```')
        r = ClaudeConceptReviewer(client).review("It is important to note X.", None, PRINCIPLES)
        self.assertEqual(len(r.findings), 1)

    def test_malformed_fails_loudly(self):
        with self.assertRaises(ConceptReviewError):
            ClaudeConceptReviewer(_FakeClient("not json at all {")).review("x", None, PRINCIPLES)

    def test_call_uses_temperature_zero(self):
        client = _FakeClient("[]")
        ClaudeConceptReviewer(client, model="claude-sonnet-5").review("x", None, PRINCIPLES)
        self.assertEqual(client.last_kwargs["temperature"], 0)
        self.assertEqual(client.last_kwargs["model"], "claude-sonnet-5")


class SafetyTests(unittest.TestCase):
    def test_no_gate_access_in_module(self):
        # Acceptance criterion: the adapter must not import gates or touch sign-offs.
        src = inspect.getsource(review_claude)
        self.assertNotIn("import.*gates", src)
        self.assertNotIn("signoff", src.lower())
        self.assertNotIn("finalize", src.lower())

    def test_findings_still_pass_locked_span_guard(self):
        # A finding quoting present, non-locked text survives validate_report.
        doc = Document(doc_id="x", title="X", rendered="We offer a cutting-edge platform.")
        client = _FakeClient('[{"principle_id":"P2","severity":"deficient","span":"cutting-edge","message":"m"}]')
        r = ClaudeConceptReviewer(client).review(doc.rendered, doc, PRINCIPLES)
        self.assertEqual(len(validate_report(r, doc).findings), 1)

    def test_from_anthropic_loud_without_key(self):
        import os
        saved = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            with self.assertRaises(RuntimeError):
                ClaudeConceptReviewer.from_anthropic()
        finally:
            if saved is not None:
                os.environ["ANTHROPIC_API_KEY"] = saved


if __name__ == "__main__":
    unittest.main(verbosity=2)
