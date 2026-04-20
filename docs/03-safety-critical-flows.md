# Safety-Critical Flow Definitions

## 1) SOS Trigger Flow
- User presses SOS on wearable.
- Band transmits SOS + device ID + timestamp + coarse GPS.
- Pole validates packet and starts siren/strobe immediately.
- Pole sends incident to backend for escalation.

## 2) No-Network Fallback Flow
- If cloud unavailable, pole still performs siren/strobe locally.
- Pole retries GSM escalation with exponential backoff.
- Incident remains queued locally until upload succeeds.

## 3) False-Trigger Cancel Window
- 10-second cancel window available after trigger.
- Cancel requires authenticated local action (band double-hold + pole confirmation).
- Cancel event is logged and preserved for audit.

## 4) Evidence Capture & Secure Storage
- Pole camera captures short clip on activation.
- File metadata linked to incident ID.
- Encrypted-at-rest storage and role-based retrieval.
