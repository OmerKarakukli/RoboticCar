#define ledPin 13

#define RightMotPwm 7
#define LeftMotPwm 6
#define RightMotDir1 4
#define RightMotDir2 5
#define LeftMotDir1 2
#define LeftMotDir2 3


String serverIn = "";
bool stringComplete = false;

typedef struct HRC {
  byte trig;
  byte echo;
  uint32_t dist;
} HRC;

HRC FL{52, 53, 0};
HRC FR{50, 51, 0};
HRC L{48, 49, 0};
HRC R{46, 47, 0};
HRC sensors[4] = {L, FL, FR, R};

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
  for (byte i = 0; i < 4; i++) {
    pinMode(sensors[i].trig, OUTPUT);
    digitalWrite(sensors[i].trig, LOW);
    pinMode(sensors[i].echo, INPUT);
  }
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
    else if ((serverIn == "Dist") || (serverIn == "dist")) {
      //updateFrontDist();
      //Serial.println(frontDist);
      updateDist(&L);
      updateDist(&FL);
      updateDist(&FR);
      updateDist(&R);
      Serial.print(L.dist); Serial.print(','); Serial.print(FL.dist); Serial.print(','); Serial.print(FR.dist); Serial.print(','); Serial.println(R.dist);
    }
    else {
      Serial.println("Unknown command");
    }
    serverIn = "";
    stringComplete = false;
  }
  //updateDist(&L);
  //updateDist(&FL);
  //updateDist(&FR);
  //updateDist(&R);
  //Serial.print(L.dist); Serial.print(','); Serial.print(FL.dist); Serial.print(','); Serial.print(FR.dist); Serial.print(','); Serial.println(R.dist);
  //updateFrontDist();
  //Serial.println(frontDist);
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      serverIn += inChar;
    }
    //delay(5);
  }
}



void updateDist(HRC *sen) {
  digitalWrite(sen->trig, LOW);
  delayMicroseconds(5);
  digitalWrite(sen->trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(sen->trig, LOW);
  uint32_t duration = pulseIn(sen->echo, HIGH, 3500); //250000
  if (duration != 0) {
    sen->dist = duration / 5.831;
  } else {
    sen->dist = 600;
  }
}



/*void updateFrontDist() {
  digitalWrite(trig, LOW);
  delayMicroseconds(5);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  uint32_t duration = pulseIn(echo, HIGH, 250000);
  if (duration != 0) {
    frontDist = duration / 5.831;
  }
  }*/
