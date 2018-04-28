//motor driver
#define enA 9
#define in1 4
#define in2 5
#define enB 10
#define in3 6
#define in4 7

//ultrasonic distance (not used in the final version due to time)
#define trig 11
#define echo 3

int debugCounter = 0;
bool varDebuger = false;

const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];

// variables to hold the parsed data
char messageFromPC[numChars] = {0};
int serialPwmA = 0;
int serialPwmB = 0;

boolean newData = false;

bool newSpeed = false;//starts stopped --- change to true if you want it to go without the Raspberry Pi
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
  Serial.println("Enter data in this style <Text, 12, 24.7>  ");
}

void loop() {
  
  recvWithStartEndMarkers();
  if (newData == true) {
    strcpy(tempChars, receivedChars);
    // because strtok() used in parseData() replaces the commas with \0
    parseData();
    //showParsedData();
    newData = false;
    newSpeed = true;    
    Serial.println(serialPwmA);
    Serial.println(serialPwmB);
  }

  if (newSpeed == true){
    
    if (serialPwmA > 0) {
       digitalWrite(in1, HIGH);//ajust this for direction (swap high and low)
       digitalWrite(in2, LOW);
    } else if (serialPwmA < 0) {//negative PWM means that the motors go backwords
      digitalWrite(in2, LOW);
      digitalWrite(in2, HIGH);
    }

    if (serialPwmB > 0) {
      digitalWrite(in3, HIGH);//ajust this for direction (swap high and low)
      digitalWrite(in4, LOW);
    } else if (serialPwmB < 0) {//negative PWM means that the motors go backwords
      digitalWrite(in4, LOW);
      digitalWrite(in4, HIGH);
    }

    newSpeed = false;//change to false after testing
  }
  //This needs to run every time to  keep PWM
  analogWrite(enA, abs(serialPwmA));// Send PWM signal to motor A
  analogWrite(enB, abs(serialPwmB));// Send PWM signal to motor B


  //if (ultrasonic == true)
    //add the updated sensor code here
    
  if (varDebuger == true){
    debugCounter++;
    if (debugCounter == 500){
        debugCounter = 0;
    }
    Serial.println(debugCounter);
  }

}

//functions moded from Robin2 on the arduino forums
//https://forum.arduino.cc/index.php?topic=288234.0
void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0';// terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}


void parseData() {// split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");// get the first part - the string
    strcpy(messageFromPC, strtokIndx);// copy it to messageFromPC
 
    strtokIndx = strtok(NULL, ",");// this continues where the previous call left off
    serialPwmA = atoi(strtokIndx);// convert this part to an integer

    strtokIndx = strtok(NULL, ",");
    serialPwmB = atoi(strtokIndx);// convert this part to an intager (was float)

} 
