#define hall_analog A0 //A0
int16_t signal {};
bool flag {};

#define RPWM_Output 6
#define LPWM_Output 5

int max_pwm = 85;

String serial;

void setup() {
  // pinMode(A7, OUTPUT);
  // digitalWrite(A7, HIGH);
  pinMode(RPWM_Output, OUTPUT);
  pinMode(LPWM_Output, OUTPUT);
  pinMode(hall_analog, INPUT);
  
  Serial.setTimeout(100);
  Serial.begin(9600);
}

void loop() {
  signal = analogRead(hall_analog); //187 to 873, for most potentiometer configs varies b/w 200 to 800
  serial = Serial.readString();
  if (serial == "d" && !flag) { //take signal<600 for (+) polarity, signal>400 for (-)
    Serial.println("DOWN");
    analogWrite(LPWM_Output, 0);
    analogWrite(RPWM_Output, max_pwm);
    flag = 1;
    }
    
  else if (serial == "u" && !flag) {
    Serial.println("UP");
    analogWrite(LPWM_Output, max_pwm);
    analogWrite(RPWM_Output, 0);
    flag = 1;
    } 
  
  else if (serial == "s" || signal > 600) {
    Serial.println("STOP");
    analogWrite(LPWM_Output, 0);
    analogWrite(RPWM_Output, 0);
    flag = 0;
    }
  //Serial.println(signal);
}

