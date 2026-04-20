// Wearable SOS Band Prototype Firmware (stub)
// Purpose: detect SOS button press and transmit LoRa emergency packet.

const int SOS_BUTTON_PIN = 2;
const int LED_PIN = 13;

void setup() {
  pinMode(SOS_BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  // TODO: initialize LoRa radio and GPS (if available)
}

void loop() {
  if (digitalRead(SOS_BUTTON_PIN) == LOW) {
    digitalWrite(LED_PIN, HIGH);
    // TODO: build and send SOS payload: band_id, timestamp, gps, battery
    delay(500);
    digitalWrite(LED_PIN, LOW);
  }
  delay(50);
}
