#define ledPin 13

#define RightMotPwm 7
#define LeftMotPwm 6
#define RightMotDir1 5
#define RightMotDir2 4
#define LeftMotDir1 3
#define LeftMotDir2 2

#define trig 52
#define echo 53

String serverIn = "";
bool stringComplete = false;

uint32_t frontDist;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  serverIn.reserve(1024);
  pinMode(RightMotPwm, OUTPUT);
  pinMode(LeftMotPwm, OUTPUT);
  pinMode(RightMotDir1, OUTPUT);
  pinMode(RightMotDir2, OUTPUT);
  pinMode(LeftMotDir1, OUTPUT);
  pinMode(LeftMotDir2, OUTPUT);
  pinMode(ledPin, OUTPUT);
  analogWrite(RightMotPwm, 0);
  analogWrite(LeftMotPwm, 0);
  pinMode(trig, OUTPUT);
  digitalWrite(trig, LOW);
  pinMode(echo, INPUT);
  frontDist = 0;
}

void loop() {
  // put your main code here, to run repeatedly:
  if (stringComplete) {
    if ((serverIn == "ON") || (serverIn == "on") || (serverIn == "On") ) {
      Serial.println("Turn On");
      digitalWrite(ledPin, HIGH);
    }
    else if ((serverIn == "OFF") || (serverIn == "off") || (serverIn == "Off")) {
      Serial.println("Turn Off");
      digitalWrite(ledPin, LOW);
    }
    else if ((serverIn == "W") || (serverIn == "w")) {
      Serial.println("Go Forward");
      digitalWrite(RightMotDir1, LOW);
      digitalWrite(RightMotDir2, HIGH);
      digitalWrite(LeftMotDir1, LOW);
      digitalWrite(LeftMotDir2, HIGH);
      analogWrite(RightMotPwm, 255);
      analogWrite(LeftMotPwm, 255);
    }
    else if ((serverIn == "X") || (serverIn == "x")) {
      Serial.println("Go Backward");
      digitalWrite(RightMotDir1, HIGH);
      digitalWrite(RightMotDir2, LOW);
      digitalWrite(LeftMotDir1, HIGH);
      digitalWrite(LeftMotDir2, LOW);
      analogWrite(RightMotPwm, 255);
      analogWrite(LeftMotPwm, 255);
    }
    else if ((serverIn == "D") || (serverIn == "d")) {
      Serial.println("Tuen Right");
      digitalWrite(RightMotDir1, HIGH);
      digitalWrite(RightMotDir2, LOW);
      digitalWrite(LeftMotDir1, LOW);
      digitalWrite(LeftMotDir2, HIGH);
      analogWrite(RightMotPwm, 255);
      analogWrite(LeftMotPwm, 255);
    }
    else if ((serverIn == "A") || (serverIn == "a")) {
      Serial.println("Turn Left");
      digitalWrite(RightMotDir1, LOW);
      digitalWrite(RightMotDir2, HIGH);
      digitalWrite(LeftMotDir1, HIGH);
      digitalWrite(LeftMotDir2, LOW);
      analogWrite(RightMotPwm, 255);
      analogWrite(LeftMotPwm, 255);
    }
    else if ((serverIn == "S") || (serverIn == "s")) {
      Serial.println("Stop");
      analogWrite(RightMotPwm, 0);
      analogWrite(LeftMotPwm, 0);
    }
    else if ((serverIn == "S") || (serverIn == "s")) {
      Serial.println("Stop");
      analogWrite(RightMotPwm, 0);
      analogWrite(LeftMotPwm, 0);
    }
    else if (serverIn == "frontDist") {
      Serial.println(frontDist);
    }
    else {
      Serial.println("Unknown command");
    }
    serverIn = "";
    stringComplete = false;
  }

  updateFrontDist();

}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      serverIn += inChar;
    }
    delay(5);
  }
}

void updateFrontDist() {
  digitalWrite(trig, LOW);
  delayMicroseconds(5);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  uint32_t duration = pulseIn(echo, HIGH, 250000);
  if (duration != 0) {
    frontDist = duration / 5.831;
  }
}
