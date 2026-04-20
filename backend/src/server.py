import json
import math
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

INCIDENTS = {}
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
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            return self._send_json(200, {"status": "ok"})

        if parsed.path == "/api/v1/incidents":
            incidents = sorted(INCIDENTS.values(), key=lambda x: x["created_at"], reverse=True)
            return self._send_json(200, {"incidents": incidents})

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
        return self._send_json(201, incident)


def run():
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print("RakshaNet backend running on http://0.0.0.0:8080")
    server.serve_forever()


if __name__ == "__main__":
    run()
