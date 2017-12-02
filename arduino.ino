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

int motorPwmA = 120;
int motorPwmB = 120;
int readPwmA;
int readPwmB;

int debugCounter = 0;
bool varDebuger = false;

String serialData;

bool newSpeed = false;//starts stopped
bool ultrasonic = false;//if the ultrasonic distance sensor is enabled or not

String getValue(String data, char separator, int index) {//Thanks to econjack on the Arduino forums
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}


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
    serialData = Serial.read();
    String valA = getValue(serialData, 'm', 0);
    String valB = getValue(serialData, 'm', 1);
    readPwmA = valA.toInt();
    readPwmB = valB.toInt();
    newSpeed = true;
  }
  
  if (newSpeed == true){
    
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


  //if (ultrasonic == true)
    //add the updated sensor code here
    
  if (varDebuger == true){
    debugCounter++;
    Serial.println(debugCounter);
  }
  

}
