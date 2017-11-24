//motor driver
#define enA 9
#define in1 4
#define in2 5
#define enB 10
#define in3 6
#define in4 7

//ultrasonic distance
#define trig 11
#define echo 3

int motorPwmA = 255;
int motorPwmB = -200;

long duration;
int distance;

bool newSpeed = true;//starts stopped
bool ultrasonic = false;//if the ultrasonic distance sensor is enabled or not

void setup() {
//motor driver
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

//ultrasonic distance
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  
//USB connection
  Serial.begin(9600);
}


void loop() {

  if(Serial.available() > 0) {
    char data = Serial.read();
    char str[2];
    str[0] = data;
    str[1] = '\0';
    Serial.println(str);
  }
  
  if (newSpeed = true){
    
    if (motorPwmA > 0) {
       digitalWrite(in1, HIGH);//ajust this for direction (swap high and low)
       digitalWrite(in2, LOW);//
    } else if (motorPwmA < 0) {//negative PWM means that the motors go backwords
      digitalWrite(in2, LOW);
      digitalWrite(in2, HIGH);
    }

    if (motorPwmB > 0) {
      digitalWrite(in3, HIGH);//ajust this for direction (swap high and low)
      digitalWrite(in4, LOW);
    } else if (motorPwmB < 0) {//negative PWM means that the motors go backwords
      digitalWrite(in4, LOW);
      digitalWrite(in4, HIGH);
    }

    newSpeed = true;//change to false after testing
  }
  //This needs to run every time to  keep PWM
  analogWrite(enA, abs(motorPwmA)); // Send PWM signal to motor A
  analogWrite(enB, abs(motorPwmB)); // Send PWM signal to motor B


  if (ultrasonic == true)
    digitalWrite(trig, LOW);
    delayMicroseconds(2);
    
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW);

    duration = pulseIn(echo, HIGH);//distance in time to an object
    
    distance = duration*0.034/2;//converts to distance in cm

    Serial.println(distance);
    
  analogWrite(enA, abs(motorPwmA)); // Send PWM signal to motor A
  analogWrite(enB, abs(motorPwmB)); // Send PWM signal to motor B

}











