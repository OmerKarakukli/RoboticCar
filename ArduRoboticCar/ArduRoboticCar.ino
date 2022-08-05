#define ledPin 13

#define RightMotPwm 7
#define LeftMotPwm 6
#define RightMotDir1 4
#define RightMotDir2 5
#define LeftMotDir1 2
#define LeftMotDir2 3

String serverIn = "";
bool stringComplete = false;

char output_buffer[128];

class HRC {
private:
  uint8_t _trig_pin{};
  uint8_t _echo_pin{};
  uint32_t _cur_dist{};
public:
  HRC(uint8_t trig_pin, uint8_t echo_pin)
  : _trig_pin(trig_pin)
  , _echo_pin(echo_pin)
  {

  }
  
  void init() {
    pinMode(_trig_pin, OUTPUT);
    digitalWrite(_trig_pin, LOW);
    pinMode(_echo_pin, INPUT);    
  }
  
  uint8_t get_trig_pin() { return _trig_pin; }
  uint8_t get_echo_pin() { return _echo_pin; }
  uint32_t get_cur_dist() { return _cur_dist; }

  void updateDist() {
    digitalWrite(_trig_pin, LOW);
    delayMicroseconds(5);
    digitalWrite(_trig_pin, HIGH);
    delayMicroseconds(10);
    digitalWrite(_trig_pin, LOW);
    uint32_t duration = pulseIn(_echo_pin, HIGH, 3500); //250000
    if (duration != 0) {
      _cur_dist = duration / 5.831;
    
    } else {
      _cur_dist = 600;
    }
  }

};

HRC FL{52, 53};
HRC FR{50, 51};
HRC L{48, 49};
HRC R{46, 47};

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
  FL.init();
  FR.init();
  L.init();
  R.init();
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
      L.updateDist();
      FL.updateDist();
      FR.updateDist();
      R.updateDist();
      sprintf_P(output_buffer, "%d,%d,%d,%d\n", L.get_cur_dist(), FL.get_cur_dist(), FR.get_cur_dist(), R.get_cur_dist());
      Serial.write(output_buffer);
    }
    else {
      Serial.println("Unknown command");
    }
    serverIn = "";
    stringComplete = false;
  }
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
