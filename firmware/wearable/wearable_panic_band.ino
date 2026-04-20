// Wearable SOS Band Prototype Firmware (stub)
// Purpose: detect SOS button press and transmit LoRa emergency packet.

const int SOS_BUTTON_PIN = 2;
const int LED_PIN = 13;
const unsigned long BUTTON_DEBOUNCE_MS = 60;
bool lastRawState = HIGH;
bool stableButtonState = HIGH;
unsigned long lastDebounceAt = 0;
unsigned long ledOffAt = 0;

void setup() {
  pinMode(SOS_BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  // TODO: initialize LoRa radio and GPS (if available)
}

void triggerSOS() {
  digitalWrite(LED_PIN, HIGH);
  ledOffAt = millis() + 500;
  // TODO: build and send SOS payload: band_id, timestamp, gps, battery
}

void loop() {
  bool rawState = digitalRead(SOS_BUTTON_PIN);
  unsigned long now = millis();

  if (rawState != lastRawState) {
    lastRawState = rawState;
    lastDebounceAt = now;
  }

  if ((now - lastDebounceAt) >= BUTTON_DEBOUNCE_MS && stableButtonState != rawState) {
    stableButtonState = rawState;
    if (stableButtonState == LOW) triggerSOS();
  }

  if (ledOffAt > 0 && now >= ledOffAt) {
    digitalWrite(LED_PIN, LOW);
    ledOffAt = 0;
  }
}
