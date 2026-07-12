"""TORO generator tests. Run: `cd engine && python -m unittest tests.test_toro -v`.

The load-bearing test is that a non-delegable obligation can NEVER be drafted as
transferred (HC1): build_toro fails closed before it renders anything.
"""

import unittest

from ossicro import toro


class RegistryTests(unittest.TestCase):
    def test_menu_shape(self):
        reg = toro.load_sponsor_obligations()
        self.assertEqual(len(reg["transferable"]), 12)
        self.assertEqual(len(reg["non_transferable"]), 6)
        for o in reg["transferable"]:
            self.assertTrue(o["id"] and o["description"] and o["citations"])
            self.assertEqual(o["default_owner"], "sponsor")
        for o in reg["non_transferable"]:
            self.assertTrue(o["holder"] and o["reason"] and o["citations"])

    def test_non_delegable_set(self):
        nt = {o["id"] for o in toro.load_sponsor_obligations()["non_transferable"]}
        for expected in ("informed-consent", "irb-judgment", "investigator-conduct",
                         "si-attestations", "dsmb-deliberation", "supply-decision"):
            self.assertIn(expected, nt)


class BuildTests(unittest.TestCase):
    PARTIES = {"sponsor": {"legal_name": "Dr. Jordan Rivera (sponsor-investigator)",
                           "address": "Montclair, NJ"},
               "cro": {"legal_name": "Thin Accountable Layer LLC", "address": "NJ"}}
    PROTOCOL = {"number": "XYZ101-EPIL-002", "title": "n-of-1 EA study",
                "ind_number": "IND 176432"}

    def test_enumerated_transfer(self):
        r = toro.build_toro(
            scope="enumerated",
            transferred_ids=["select-monitors", "annual-reports"],
            parties=self.PARTIES, protocol=self.PROTOCOL, effective_date="2026-07-15")
        self.assertEqual(r["transferred"], ["annual-reports", "select-monitors"])
        by_id = {row["id"]: row for row in r["obligation_table"]}
        self.assertEqual(by_id["select-monitors"]["status"], "Transferred")
        self.assertEqual(by_id["annual-reports"]["status"], "Transferred")
        self.assertEqual(by_id["fda-inspection"]["status"], "Retained")
        # owner map: transferred -> CRO, retained -> sponsor
        owners = {e["obligation"]: e["holder"] for e in r["owner_map"]}
        self.assertEqual(owners["select-monitors"], "CRO")
        self.assertEqual(owners["fda-inspection"], "sponsor")
        self.assertIn("fda-inspection", r["retained"])

    def test_transfer_all(self):
        r = toro.build_toro(scope="all", parties=self.PARTIES, protocol=self.PROTOCOL)
        self.assertEqual(len(r["transferred"]), 12)
        self.assertEqual(r["retained"], [])
        self.assertTrue(all(row["status"] == "Transferred"
                            for row in r["obligation_table"]))

    def test_refuses_non_delegable(self):
        with self.assertRaises(toro.TransferError) as cm:
            toro.build_toro(scope="enumerated",
                            transferred_ids=["select-monitors", "informed-consent"])
        msg = str(cm.exception)
        self.assertIn("informed-consent", msg)
        self.assertIn("non-delegable", msg)
        self.assertIn("312.52", msg)

    def test_refuses_each_non_delegable(self):
        nt = {o["id"] for o in toro.load_sponsor_obligations()["non_transferable"]}
        for oid in nt:
            with self.assertRaises(toro.TransferError):
                toro.build_toro(scope="enumerated", transferred_ids=[oid])

    def test_refuses_unknown_id(self):
        with self.assertRaises(toro.TransferError):
            toro.build_toro(scope="enumerated", transferred_ids=["not-a-real-obligation"])

    def test_invalid_scope(self):
        with self.assertRaises(toro.TransferError):
            toro.build_toro(scope="some", transferred_ids=[])

    def test_safety_review_qualified_human_warning(self):
        r = toro.build_toro(scope="enumerated", transferred_ids=["safety-review"])
        self.assertTrue(any("safety-review" in w and "physician" in w.lower()
                            for w in r["warnings"]))

    def test_non_delegable_always_in_owner_map(self):
        # even a minimal transfer names what it cannot move
        r = toro.build_toro(scope="enumerated", transferred_ids=[])
        nt_in_map = {e["obligation"] for e in r["owner_map"] if not e["transferable"]}
        self.assertEqual(len(nt_in_map), 6)

    def test_rendered_document(self):
        r = toro.build_toro(scope="enumerated",
                            transferred_ids=["annual-reports"],
                            parties=self.PARTIES, protocol=self.PROTOCOL,
                            effective_date="2026-07-15")
        doc = r["rendered"]
        self.assertIn("21 CFR 312.52", doc)
        self.assertIn("DRAFT", doc)
        self.assertIn("Field 16", doc)                       # 1571 documentation
        self.assertIn("Thin Accountable Layer LLC", doc)     # CRO party
        self.assertIn("deemed NOT transferred", doc)
        self.assertIn("informed consent", doc.lower())       # non-delegable section


if __name__ == "__main__":
    unittest.main()
