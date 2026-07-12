"""OSSICRO end-to-end smoke test — proves the whole dashboard flow works.

Run the server first, then this script:

    python app/server.py            # terminal 1  (serves http://127.0.0.1:8765)
    python tools/smoke_e2e.py       # terminal 2

It creates a fresh synthetic case and drives every persona path the dashboard
uses: intake -> commit -> generate -> ledger -> package -> Form-3926 PDF ->
registry match -> release -> manufacturer inbox -> patient link/view ->
export -> enrollment promote -> coordinator board -> IRB gate sign-off. Each
step prints PASS/FAIL; the process exits non-zero if any step fails.

Pure standard library, same as the server. No real PHI: the sample case is the
synthetic epilepsy fixture the tests use. Uses the public HTTP API only.
"""
import json
import sys
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8765"
_passed = 0
_failed = 0


def call(method, path, body=None, raw=False):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        BASE + path, data=data,
        headers={"Content-Type": "application/json"}, method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            payload = r.read()
            if raw:
                return r.status, payload
            try:
                return r.status, json.loads(payload.decode())
            except ValueError:
                return r.status, payload.decode(errors="replace")[:200]
    except urllib.error.HTTPError as e:
        payload = e.read()
        try:
            return e.code, json.loads(payload.decode())
        except ValueError:
            return e.code, payload.decode(errors="replace")[:300]
    except urllib.error.URLError as e:
        print(f"\nCannot reach {BASE} — is the server running? ({e})")
        sys.exit(2)


def step(name, cond, detail=""):
    global _passed, _failed
    if cond:
        _passed += 1
        print(f"[PASS] {name}  {detail}")
    else:
        _failed += 1
        print(f"[FAIL] {name}  {detail}")


def main():
    actor = "Dr. Jordan Rivera"

    s, schema = call("GET", "/api/route/3926/schema")
    nfields = len(schema.get("fields", [])) if isinstance(schema, dict) else 0
    step("GET route schema", s == 200 and nfields > 0, f"http {s}, {nfields} fields")

    s, sample = call("GET", "/api/route/3926/sample")
    values = sample.get("values", sample) if isinstance(sample, dict) else {}
    step("GET sample intake", s == 200 and bool(values), f"http {s}")

    s, case = call("POST", "/api/case", {})
    cid = (case.get("case_id") or case.get("id")) if isinstance(case, dict) else None
    step("POST create case", s == 200 and bool(cid), f"http {s}, id={cid}")
    if not cid:
        _finish()

    s, r = call("POST", f"/api/case/{cid}/intake", {"values": values})
    if s != 200:
        s, r = call("POST", f"/api/case/{cid}/intake", values)
    step("POST intake", s == 200, f"http {s}")

    s, r = call("POST", f"/api/case/{cid}/profile/commit", {"actor": actor})
    committed = r.get("committed", {}) if isinstance(r, dict) else {}
    step("POST profile/commit", s == 200, f"http {s}, state={committed.get('state')}")

    s, gen = call("POST", f"/api/case/{cid}/generate", {"route_id": "3926"})
    ndocs = len(gen.get("documents", {})) if isinstance(gen, dict) else 0
    step("POST generate documents", s == 200 and ndocs > 0, f"http {s}, {ndocs} docs")

    s, chk = call("GET", f"/api/case/{cid}/check")
    step("GET completeness ledger", s == 200 and isinstance(chk, dict),
         f"http {s}, totals={chk.get('totals') if isinstance(chk, dict) else '?'}")

    s, pkg = call("GET", f"/api/case/{cid}/package")
    step("GET package manifest", s == 200 and isinstance(pkg, dict) and "package_sha256" in pkg,
         f"http {s}")

    s, pdf = call("GET", f"/api/case/{cid}/form3926.pdf", raw=True)
    is_pdf = isinstance(pdf, (bytes, bytearray)) and pdf[:4] == b"%PDF"
    step("GET Form-3926 PDF", s == 200 and is_pdf,
         f"http {s}, {len(pdf) if isinstance(pdf, (bytes, bytearray)) else '?'} bytes")

    s, m = call("POST", f"/api/case/{cid}/match", {})
    step("POST registry match", s == 200 and isinstance(m, dict),
         f"http {s}, {len(m.get('candidates', [])) if isinstance(m, dict) else '?'} candidates")

    s, _ = call("POST", f"/api/case/{cid}/release", {"actor": actor, "to": "manufacturer"})
    step("POST release to manufacturer", s == 200, f"http {s}")

    s, inbox = call("GET", "/api/manufacturer/inbox")
    step("GET manufacturer inbox", s == 200, f"http {s}")

    s, pl = call("POST", f"/api/case/{cid}/patient-link", {"actor": actor})
    token = pl.get("patient_token") if isinstance(pl, dict) else None
    step("POST mint patient link", s == 200 and bool(token), f"http {s}")
    if token:
        s, pv = call("GET", f"/api/patient/{token}")
        step("GET patient status view", s == 200 and isinstance(pv, dict),
             f"http {s}, stage={pv.get('stage') if isinstance(pv, dict) else '?'}")
        s, _ = call("GET", "/api/patient/deadbeefdeadbeef")
        step("GET unknown patient token -> 404", s == 404, f"http {s}")

    s, _ = call("POST", f"/api/case/{cid}/export", {"actor": actor, "format": "pdf"})
    step("POST audited export", s == 200, f"http {s}")

    ack = ("I acknowledge informed-consent and IRB concurrence are not yet signed; "
           "I am recording enrollment for tracking and will not treat until both complete.")
    s, pr = call("POST", f"/api/case/{cid}/promote",
                 {"actor": actor, "legal_basis": "waiver-164.512",
                  "acknowledge_unsigned_gates": ack})
    step("POST promote to enrollment", s == 200, f"http {s}")

    s, board = call("GET", "/api/cro/board")
    step("GET coordinator board", s == 200, f"http {s}")

    # IRB gate sign-off: role/gate/doc must all match — the governance check.
    _, chk2 = call("GET", f"/api/case/{cid}/check")
    irb_doc = next((g.get("doc_id") for g in chk2.get("gate_packet", [])
                    if g.get("gate_id") == "irb-approval"), "")
    s, _ = call("POST", f"/api/case/{cid}/signoff",
                {"gate_id": "irb-approval", "doc_id": irb_doc, "role": "irb",
                 "signer_name": actor, "date": "2026-07-14",
                 "statement": "IRB (Advarra) granted concurrence for this "
                              "single-patient expanded-access treatment; letter on file.",
                 "evidence": {"type": "irb-letter", "reference": "Advarra concurrence"}})
    step("POST role-checked gate sign-off", s == 200, f"http {s}")

    # Micro-CRO: obligations menu, a draft TORO, and the non-delegable refusal
    s, menu = call("GET", "/api/toro/obligations")
    step("GET TORO obligations menu", s == 200 and isinstance(menu, dict)
         and len(menu.get("transferable", [])) == 12, f"http {s}")
    s, tor = call("POST", "/api/toro",
                  {"scope": "enumerated",
                   "transferred_ids": ["select-monitors", "annual-reports"]})
    step("POST build draft TORO", s == 200 and isinstance(tor, dict)
         and bool(tor.get("rendered")), f"http {s}")
    s, _ = call("POST", "/api/toro",
                {"scope": "enumerated", "transferred_ids": ["informed-consent"]})
    step("POST TORO refuses non-delegable -> 400", s == 400, f"http {s}")

    _finish()


def _finish():
    print(f"\n==== SMOKE RESULT: {_passed} passed, {_failed} failed ====")
    sys.exit(1 if _failed else 0)


if __name__ == "__main__":
    main()
