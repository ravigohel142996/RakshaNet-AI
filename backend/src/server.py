import json
import math
import os
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

# Prototype-only in-memory incident storage.
# Replace with persistent storage (e.g., PostgreSQL) for production deployments.
INCIDENTS = {}
INCIDENT_ORDER = []
MIN_PAGE_LIMIT = 1
MAX_PAGE_LIMIT = 500
DEFAULT_PAGE_LIMIT = 50
DEFAULT_ALLOWED_ORIGIN = "http://localhost"
DEFAULT_BIND_HOST = "127.0.0.1"
DEFAULT_BIND_PORT = 8080
# Prototype helper catalog.
# For production, load responders from deployment-specific configuration/database.
HELPERS = [
    {"id": "helper-1", "name": "ASHA Worker 1", "lat": 23.0225, "lng": 72.5714},
    {"id": "helper-2", "name": "Police Post A", "lat": 23.0300, "lng": 72.5800},
    {"id": "helper-3", "name": "Community Volunteer", "lat": 23.0150, "lng": 72.5600},
]


def haversine_km(lat1, lon1, lat2, lon2):
    radius = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c


def nearest_helper(lat, lng):
    ranked = sorted(
        HELPERS,
        key=lambda helper: haversine_km(lat, lng, helper["lat"], helper["lng"]),
    )
    helper = ranked[0]
    return {
        "id": helper["id"],
        "name": helper["name"],
        "distance_km": round(haversine_km(lat, lng, helper["lat"], helper["lng"]), 2),
    }


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header(
            "Access-Control-Allow-Origin",
            os.getenv("RAKSHANET_ALLOWED_ORIGIN", DEFAULT_ALLOWED_ORIGIN),
        )
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send_json(200, {"status": "ok"})

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            return self._send_json(200, {"status": "ok"})

        if parsed.path == "/api/v1/incidents":
            query = parse_qs(parsed.query)
            try:
                limit = min(
                    max(int(query.get("limit", [str(DEFAULT_PAGE_LIMIT)])[0]), MIN_PAGE_LIMIT),
                    MAX_PAGE_LIMIT,
                )
                offset = max(int(query.get("offset", ["0"])[0]), 0)
            except ValueError:
                return self._send_json(400, {"error": "invalid_pagination"})
            incident_ids = INCIDENT_ORDER[offset : offset + limit]
            incidents = [INCIDENTS[incident_id] for incident_id in incident_ids]
            return self._send_json(
                200,
                {
                    "incidents": incidents,
                    "pagination": {"offset": offset, "limit": limit, "total": len(INCIDENT_ORDER)},
                },
            )

        if parsed.path.startswith("/api/v1/incidents/"):
            incident_id = parsed.path.split("/")[-1]
            incident = INCIDENTS.get(incident_id)
            if not incident:
                return self._send_json(404, {"error": "incident_not_found"})
            return self._send_json(200, incident)

        return self._send_json(404, {"error": "not_found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/v1/sos":
            return self._send_json(404, {"error": "not_found"})

        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            return self._send_json(400, {"error": "invalid_json"})

        required = ["band_id", "lat", "lng"]
        missing = [key for key in required if key not in payload]
        if missing:
            return self._send_json(400, {"error": "missing_fields", "fields": missing})

        incident_id = str(uuid.uuid4())
        helper = nearest_helper(float(payload["lat"]), float(payload["lng"]))

        incident = {
            "incident_id": incident_id,
            "band_id": payload["band_id"],
            "lat": payload["lat"],
            "lng": payload["lng"],
            "pole_id": payload.get("pole_id", "nearest-pole"),
            "status": "triggered",
            "actions": [
                "pole_alerted",
                "siren_on",
                "strobe_on",
                "gsm_escalation_to_3_contacts",
            ],
            "nearest_helper": helper,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        INCIDENTS[incident_id] = incident
        INCIDENT_ORDER.insert(0, incident_id)
        return self._send_json(201, incident)


def run():
    host = os.getenv("RAKSHANET_HOST", DEFAULT_BIND_HOST)
    port = int(os.getenv("RAKSHANET_PORT", str(DEFAULT_BIND_PORT)))
    server = HTTPServer((host, port), Handler)
    print(f"RakshaNet backend running on http://{host}:{port}")
    print(
        "Use RAKSHANET_HOST=0.0.0.0 and explicit RAKSHANET_ALLOWED_ORIGIN "
        "for controlled multi-device/network deployment."
    )
    server.serve_forever()


if __name__ == "__main__":
    run()
