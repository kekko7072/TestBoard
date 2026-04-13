#define lockPin 2
String inputString = "";         // A string to hold incoming data
String cmd;
int ledPins[] = {3, 5, 6, 9, 10, 11}; // Your array of pins
int pinCount = 6;               // Number of LEDs

void setup() {
  Serial.begin(9600);            // Must match the Baud Rate in Python
  pinMode(ledPin, OUTPUT);           //  LED
  pinMode(lockPin, OUTPUT);          // lock system
  for (int i = 0; i < pinCount; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop() {
  // 1. Check if data is available
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    
    // 2. Build the string until we hit a newline (\n)
    if (inChar == '\n') {
      executeCommand(inputString);
      inputString = ""; // Clear for next time
    } else {
      inputString += inChar;
    }
  }
}

void executeCommand(String cmd) {
  cmd.trim(); // Remove any hidden spaces
  
  if (cmd == "LED_ON") {
    // Turning them all HIGH at once
  for (int i = 0; i < pinCount; i++) {
    analogWrite(ledPin, 138);
  }
  } 
  else if (cmd == "LED_OFF") {
   // Turning them all LOW at once
  for (int i = 0; i < pinCount; i++) {
    digitalWrite(ledPins[i], LOW);
  }
  } 

  if (cmd == "Lock_ON") {
    digitalWrite(lockPin, HIGH);
  } 
  else if (cmd == "Lock_OFF") {
    digitalWrite(lockPin, LOW);
  } 
  else if (cmd == "GET_STATUS") {
    // This sends data BACK to the Python GUI
    Serial.println("SYSTEM_OK");
  }
}
