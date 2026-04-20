# Backend Prototype

## Purpose
Alert orchestration service for SOS events.

## Features
- Accept SOS events
- Persist in-memory incident timeline
- Recommend nearest helper
- Provide incident list endpoint

## Run
```bash
cd /home/runner/work/RakshaNet-AI/RakshaNet-AI/backend
python3 -m unittest discover -s tests -p 'test_*.py'
python3 src/server.py
```
