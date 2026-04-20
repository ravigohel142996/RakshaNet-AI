# RakshaNet-AI
Offline Emergency Safety Network for Rural India

## What this repository now includes
- MVP scope and architecture documents
- Safety-critical response flow definitions
- Prototype firmware stubs (wearable + pole)
- Python backend starter for SOS orchestration
- Lightweight operations dashboard (incident timeline/status)
- Grant, pitch, and pilot business planning artifacts

## Repository structure
- `/docs` — planning, grant proof, pitch and business model artifacts
- `/firmware` — wearable and pole device firmware stubs
- `/backend` — alert orchestration service prototype
- `/dashboard` — basic web dashboard for incidents

## Quick start (backend)
```bash
cd /home/runner/work/RakshaNet-AI/RakshaNet-AI/backend
python3 -m unittest discover -s tests -p 'test_*.py'
python3 src/server.py
```

Service runs at `http://localhost:8080`.
