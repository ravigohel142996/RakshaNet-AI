// Smart Safety Pole Controller Prototype Firmware (stub)
// Purpose: receive LoRa SOS and trigger siren/strobe immediately.

const int SIREN_PIN = 5;
const int STROBE_PIN = 6;

void setup() {
  pinMode(SIREN_PIN, OUTPUT);
  pinMode(STROBE_PIN, OUTPUT);
  // TODO: initialize LoRa receiver, GSM module, optional camera module
}

void triggerAlarm() {
  digitalWrite(SIREN_PIN, HIGH);
  digitalWrite(STROBE_PIN, HIGH);
  delay(10000);
  digitalWrite(SIREN_PIN, LOW);
  digitalWrite(STROBE_PIN, LOW);
}

void loop() {
  // TODO: if LoRa SOS packet received -> triggerAlarm() and escalate over GSM
  delay(100);
}
