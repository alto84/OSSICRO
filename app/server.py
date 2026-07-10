"""OSSICRO MVP backend — Route-3926 single-patient expanded access.

Pure Python 3 stdlib (http.server). Starts with:

    python app/server.py

and listens on 127.0.0.1:8765. In-memory case store (no real PHI). Serves the
frontend at ``/`` and the SHARED API CONTRACT:

    GET  /api/route/3926/schema
    POST /api/case
    POST /api/case/{id}/intake
    POST /api/case/{id}/generate
    GET  /api/case/{id}/check
    GET  /api/case/{id}/package

The backend imports the engine (models / generate / pipeline / gates / routes /
ea_generators / assemble). It drafts, checks, and assembles; it never performs a
non-delegable act — the gates fail closed in the engine (GateViolation).
"""

from __future__ import annotations

import json
import os
import re
import sys
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# --- wire in the engine -----------------------------------------------------
APP_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(APP_DIR)
ENGINE_DIR = os.path.join(REPO_ROOT, "engine")
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

from ossicro import routes as routes_mod                     # noqa: E402
from ossicro.assemble import assemble_submission             # noqa: E402
from ossicro.ea_generators import build_study, generate_route_documents  # noqa: E402
from ossicro.pipeline import run_check                       # noqa: E402
from ossicro.registry import load_documents, load_gates      # noqa: E402

STATIC_DIR = os.path.join(APP_DIR, "static")
HOST, PORT = "127.0.0.1", 8765

# In-memory case store (MVP; no real PHI).
CASES: dict = {}

# Registries loaded once.
DOC_REGISTRY = load_documents()
GATE_REGISTRY = load_gates()


# ---------------------------------------------------------------------------
# Engine wiring per case
# ---------------------------------------------------------------------------

def _route_for(case: dict) -> dict:
    emergency = str(case["intake"].get("submission.emergency", "")).strip().lower() in ("true", "1", "yes")
    return routes_mod.route_for_emergency(emergency)


def _study_and_docs(case: dict):
    route = _route_for(case)
    study = build_study(case["intake"], route)
    documents = generate_route_documents(study, route, DOC_REGISTRY)
    return route, study, documents


def _schema_payload() -> dict:
    return {"fields": routes_mod.intake_fields()}


def _generate_payload(case: dict) -> dict:
    route, study, documents = _study_and_docs(case)
    case["route_id"] = route["route_id"]
    ordered = [d for d in route["documents"] if d in documents]
    return {
        "route_id": route["route_id"],
        "documents": [
            {"doc_id": d, "title": documents[d].title, "rendered": documents[d].rendered}
            for d in ordered
        ],
    }


def _check_payload(case: dict) -> dict:
    route, study, documents = _study_and_docs(case)
    result = run_check(study, documents, DOC_REGISTRY, GATE_REGISTRY)
    totals = {"green": 0, "amber": 0, "red": 0}
    ledger = []
    for item in result.ledger:
        totals[item.status] = totals.get(item.status, 0) + 1
        ledger.append({
            "doc_id": item.doc_id,
            "title": item.title,
            "status": item.status,
            "gate_id": item.gate_id,
            "questions": item.questions,
            "notes": item.notes,
        })
    consistency = [
        {
            "field_name": f.field_name,
            "reference_value": f.reference_value,
            "observed": f.observed,
            "question": f.question,
        }
        for f in result.inconsistencies
    ]
    gate_packet = []
    for pg in result.gate_packet:
        doc_ids = pg.doc_ids or [None]
        for doc_id in doc_ids:
            gate_packet.append({
                "gate_id": pg.gate_id,
                "name": pg.name,
                "responsible_role": pg.responsible_role,
                "citation": pg.citation,
                "doc_id": doc_id,
                "questions": pg.questions,
            })
    return {"ledger": ledger, "totals": totals, "consistency": consistency, "gate_packet": gate_packet}


def _package_payload(case: dict) -> dict:
    route, study, documents = _study_and_docs(case)
    return assemble_submission(study, documents, route, DOC_REGISTRY, GATE_REGISTRY)


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------

_CASE_INTAKE = re.compile(r"^/api/case/([^/]+)/intake$")
_CASE_GENERATE = re.compile(r"^/api/case/([^/]+)/generate$")
_CASE_CHECK = re.compile(r"^/api/case/([^/]+)/check$")
_CASE_PACKAGE = re.compile(r"^/api/case/([^/]+)/package$")


class Handler(BaseHTTPRequestHandler):
    server_version = "OSSICRO/0.1"

    # -- helpers -------------------------------------------------------------
    def _send_json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, text, status=200, content_type="text/html; charset=utf-8"):
        body = text.encode("utf-8") if isinstance(text, str) else text
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return None

    def _case(self, case_id):
        return CASES.get(case_id)

    def log_message(self, fmt, *args):  # quieter console
        sys.stderr.write("[ossicro] " + (fmt % args) + "\n")

    # -- GET -----------------------------------------------------------------
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/" or path == "/index.html":
            return self._serve_static("index.html")
        if path == "/api/route/3926/schema":
            return self._send_json(_schema_payload())

        m = _CASE_CHECK.match(path)
        if m:
            case = self._case(m.group(1))
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            try:
                return self._send_json(_check_payload(case))
            except Exception as exc:  # surfaces GateViolation etc. honestly
                return self._send_json({"error": type(exc).__name__, "detail": str(exc)}, 500)

        m = _CASE_PACKAGE.match(path)
        if m:
            case = self._case(m.group(1))
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            try:
                return self._send_json(_package_payload(case))
            except Exception as exc:
                return self._send_json({"error": type(exc).__name__, "detail": str(exc)}, 500)

        return self._send_json({"error": "not found", "path": path}, 404)

    # -- POST ----------------------------------------------------------------
    def do_POST(self):
        path = self.path.split("?", 1)[0]

        if path == "/api/case":
            case_id = uuid.uuid4().hex[:12]
            CASES[case_id] = {"intake": {}, "route_id": "route-3926"}
            return self._send_json({"case_id": case_id})

        m = _CASE_INTAKE.match(path)
        if m:
            case = self._case(m.group(1))
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            payload = self._read_json()
            if payload is None or not isinstance(payload.get("fields"), dict):
                return self._send_json({"error": "expected {fields:{...}}"}, 400)
            # Store only non-empty values; blanks stay honestly absent.
            for key, value in payload["fields"].items():
                if value is None or (isinstance(value, str) and value.strip() == ""):
                    case["intake"].pop(key, None)
                else:
                    case["intake"][key] = value
            return self._send_json({"ok": True})

        m = _CASE_GENERATE.match(path)
        if m:
            case = self._case(m.group(1))
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            try:
                return self._send_json(_generate_payload(case))
            except Exception as exc:
                return self._send_json({"error": type(exc).__name__, "detail": str(exc)}, 500)

        return self._send_json({"error": "not found", "path": path}, 404)

    # -- static --------------------------------------------------------------
    def _serve_static(self, name):
        safe = os.path.normpath(name).lstrip("/\\")
        full = os.path.join(STATIC_DIR, safe)
        if not full.startswith(STATIC_DIR) or not os.path.isfile(full):
            return self._send_text("Not found", 404, "text/plain; charset=utf-8")
        ctype = "text/html; charset=utf-8" if full.endswith(".html") else "application/octet-stream"
        with open(full, "rb") as f:
            return self._send_text(f.read(), 200, ctype)


def main():
    os.makedirs(STATIC_DIR, exist_ok=True)
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    sys.stderr.write("OSSICRO backend on http://%s:%d  (Route-3926 MVP)\n" % (HOST, PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.stderr.write("\nshutting down\n")
        httpd.shutdown()


if __name__ == "__main__":
    main()
