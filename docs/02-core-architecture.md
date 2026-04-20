# Core Architecture Freeze

## Data/Signal Path
1. Wearable device sends SOS packet over LoRa.
2. Nearest pole receives SOS and triggers local actuator stack (siren + strobe).
3. Pole forwards incident payload to backend over GSM (fallback first principle).
4. Backend sends outbound notifications and stores incident record.
5. Cloud AI computes nearest helper and fastest route when internet is available.

## Design Principles
- Local-first response: no cloud dependency for immediate life-safety actions.
- Multi-channel resilience: LoRa for local trigger, GSM for outbound reach.
- Degraded-but-safe mode: if internet/cloud fails, local and GSM paths still operate.

## Components
- Wearable firmware node
- Pole edge controller
- Alert orchestration API
- Ops dashboard
- Optional cloud optimization service
