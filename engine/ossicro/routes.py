"""Route loading: routes.json (the submission-route registry).

A ROUTE is a named submission workflow (Route-3926 single-patient expanded
access, emergency and non-emergency variants). It declares, as data:

- the ordered document set the route generates,
- the FDA-facing subset that is assembled into the reviewer's package,
- the eCTD module map,
- the statutory clocks the route arms (with working-day vs calendar-day
  calendars), and
- the code-enforced gates it touches (defined in gates.json).

The intake field schema is shared across routes and lives at the top level of
routes.json. Paths resolve relative to the engine root so the loader works from
any current working directory (mirrors ossicro.registry).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

ENGINE_ROOT = Path(__file__).resolve().parent.parent
ROUTES_PATH = ENGINE_ROOT / "registry" / "routes.json"


class RouteError(KeyError):
    """Raised when an unknown route id is requested."""


def _load() -> Dict[str, Any]:
    with open(ROUTES_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_routes() -> Dict[str, Dict[str, Any]]:
    """Return every route keyed by route id."""
    return _load().get("routes", {})


def get_route(route_id: str) -> Dict[str, Any]:
    """Return one route by id, or raise RouteError."""
    routes = load_routes()
    if route_id not in routes:
        raise RouteError(
            "Unknown route %r (available: %s)" % (route_id, ", ".join(sorted(routes)))
        )
    return routes[route_id]


def intake_fields() -> List[Dict[str, Any]]:
    """Return the shared physician-intake field schema (§8 of the spec)."""
    return _load().get("intake_fields", [])


def route_for_emergency(emergency: bool) -> Dict[str, Any]:
    """Select the emergency or non-emergency Route-3926 variant."""
    return get_route("route-3926-emergency" if emergency else "route-3926")
