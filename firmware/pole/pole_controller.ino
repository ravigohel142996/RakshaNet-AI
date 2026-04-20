// Smart Safety Pole Controller Prototype Firmware (stub)
// Purpose: receive LoRa SOS and trigger siren/strobe immediately.

const int SIREN_PIN = 5;
const int STROBE_PIN = 6;
const unsigned long ALARM_DURATION_MS = 10000;

bool alarmActive = false;
unsigned long alarmStart = 0;

void setup() {
  pinMode(SIREN_PIN, OUTPUT);
  pinMode(STROBE_PIN, OUTPUT);
  // TODO: initialize LoRa receiver, GSM module, optional camera module
}

void triggerAlarm() {
  alarmActive = true;
  alarmStart = millis();
  digitalWrite(SIREN_PIN, HIGH);
  digitalWrite(STROBE_PIN, HIGH);
}

void updateAlarm() {
  if (alarmActive && millis() - alarmStart >= ALARM_DURATION_MS) {
    alarmActive = false;
    digitalWrite(SIREN_PIN, LOW);
    digitalWrite(STROBE_PIN, LOW);
  }
}

void loop() {
  // TODO: if LoRa SOS packet received -> triggerAlarm() and escalate over GSM
  updateAlarm();
  delay(100);
}
