#include <PID_v1.h>

#define M1            8
#define M2            9  // motor's PWM outputs
#define M3            11
#define M4            10 // motor's PWM outputs
#define M5            13
#define M6            12  // motor's PWM outputs
#define M7            46
#define M8            44 // motor's PWM outputs



//double kp=93.9606732001279 ,ki=136.891460277931,kd=1.24430533532324, N=36.6125637209499; 

//double kp=101.760676251617 ,ki=186.855469671902,kd=0.874940976211089, N=42.1307433461873;
double kp=22.2707628694451 ,ki=59.2428963251724/3.0,kd=1.0*0.539873470177468, N=17.4572555042356; 
double input=0, output=0, setpoint=0, lastinput=0;
PID myPID(&input, &output, &setpoint,kp,ki,kd, DIRECT);
volatile long encoder0Pos = 0;
long previousMillis = 0;// will store last time LED was updated


double kp2=kp ,ki2=ki,kd2=kd, N2=N; 
double input2=0, output2=0, setpoint2=0, lastinput2=0;
PID myPID2(&input2, &output2, &setpoint2,kp2,ki2,kd2, DIRECT);
volatile long encoder0Pos2 = 0;
long previousMillis2 = 0;        // will store last time LED was updated

//double kp3=22.2707628694451 ,ki3=59.2428963251724,kd3=0.539873470177468, N3=17.4572555042356; 
double kp3=kp ,ki3=ki,kd3=kd, N3=N; 
double input3=0, output3=0, setpoint3=0, lastinput3=0;
PID myPID3(&input3, &output3, &setpoint3,kp3,ki3,kd3, DIRECT);
volatile long encoder0Pos3 = 0;
long previousMillis3 = 0;// will store last time LED was updated


double kp4=kp ,ki4=ki,kd4=kd, N4=N; 
double input4=0, output4=0, setpoint4=0, lastinput4=0;
PID myPID4(&input4, &output4, &setpoint4,kp4,ki4,kd4, DIRECT);
volatile long encoder0Pos4 = 0;
long previousMillis4 = 0;  


// and for the encoder:
#define ENC_A_A 2 // pin connected to external interrupt
#define ENC_A_B 4 // pin connected to normal pin
#define ENC_B_A 3 // pin connected to external interrupt
#define ENC_B_B 5 // pin connected to normal pin
#define ENC_C_A 18 // pin connected to external interrupt
#define ENC_C_B 6 // pin connected to normal pin
#define ENC_D_A 19 // pin connected to external interrupt
#define ENC_D_B 7 // pin connected to normal pin

// variables
float position_A = 0; // controller variables as globals
float position_B = 0; // controller variables as globals
float position_C = 0; // controller variables as globals
float position_D = 0; // controller variables as globals
// timing:
unsigned long loopTime, printTime; // timing
unsigned long loopTime2, printTime2; // timing
unsigned long loopTime3, printTime3; // timing
unsigned long loopTime4, printTime4; // timing
volatile long encodercount_A; 
volatile long encodercount_B; 
volatile long encodercount_C; 
volatile long encodercount_D; 
volatile unsigned long lasttime_A, transitiontime_A;
volatile unsigned long lasttime_B, transitiontime_B;
volatile unsigned long lasttime_C, transitiontime_C;
volatile unsigned long lasttime_D, transitiontime_D;


int magPin = 52;
void setup() { 
  // motor
  myPID.SetMode(AUTOMATIC);
  myPID.SetOutputLimits(-255,255);
  myPID.SetSampleTime(20);
  // motor2
  myPID2.SetMode(AUTOMATIC);
  myPID2.SetOutputLimits(-255,255);
  myPID2.SetSampleTime(20);
  // motor3
  myPID3.SetMode(AUTOMATIC);
  myPID3.SetOutputLimits(-255,255);
  myPID3.SetSampleTime(20);
  // motor4
  myPID4.SetMode(AUTOMATIC);
  myPID4.SetOutputLimits(-255,255);
  myPID4.SetSampleTime(20);
  //encoder
  pinMode(ENC_A_A, INPUT_PULLUP); // encoder A
  pinMode(ENC_A_B, INPUT_PULLUP);
  pinMode(ENC_B_A, INPUT_PULLUP); // encoder B
  pinMode(ENC_B_B, INPUT_PULLUP);
  pinMode(ENC_C_A, INPUT_PULLUP); // encoder C
  pinMode(ENC_C_B, INPUT_PULLUP);
  pinMode(ENC_D_A, INPUT_PULLUP); // encoder D
  pinMode(ENC_D_B, INPUT_PULLUP);
  
  Serial.begin (115200);
  Serial.setTimeout(1);
  attachInterrupt(0, encoder_A, RISING);
  attachInterrupt(1, encoder_B, RISING);
  attachInterrupt(5, encoder_C, RISING);
  attachInterrupt(4, encoder_D, RISING);
  setpoint = 0;
  setpoint2 = 0;
  setpoint3 = 0;
  setpoint4 = 0;
    

  // magnet
  pinMode(magPin, OUTPUT);
  digitalWrite(magPin, HIGH);
} 


float angle;
String msg;
int x;
int y ;
char data;
double magnet = 0;
bool test = true;
double  setpoints[4] = {0,0,0,0};

void loop(){
  // Updates the previous state of the outputA with the current state
  //position_A =  (float) encodercount_A*(360.0/(514.8*(80/22)*(80/22)));
  // Convertion from degrees to length
  // back up : 209, with tick rope
  input =  +(float) encodercount_A*(10.0/240.0)*10.0;
  input2 =  -(float) encodercount_B*(10.0/240.0)*10.0;
  input3 =  -(float) encodercount_C*(10.0/240.0)*10.0;
  input4 =  +(float) encodercount_D*(10.0/240.0)*10.0;
  /*
  Serial.print(input );
  Serial.print(" : ");
  Serial.print(input2 );
  Serial.print(" : ");
  Serial.print(input3 );
  Serial.print(" : ");
  Serial.print(input4 );
  Serial.println(" : ");
  */
  
  
  if(Serial.available()>0){
  
    String returnString = readStringM();
    double FirstJoin = getValue(returnString, ':', 3).toDouble();
    double SecondJoin = getValue(returnString, ':', 4).toDouble();
    double ThirthJoin = getValue(returnString, ':', 1).toDouble();
    double FourthJoin = getValue(returnString, ':', 2).toDouble();
    magnet = getValue(returnString, ':', 5).toDouble();
    
    
    if (magnet == 0){
      digitalWrite(magPin, HIGH);
    }else if (magnet == 1){
      digitalWrite(magPin, LOW);
    }
    //Serial.println( String(encoder0Pos) + " ::: " + String(encoder0Pos2) + " ::: " + String(encoder0Pos3) + " ::: " + String(encoder0Pos4) + " ::: " + String(magnet));
    Serial.println( String(ThirthJoin) + " ::: " + String(FourthJoin) + " ::: " + String(FirstJoin) + " ::: " + String(SecondJoin) + " ::: " + String(magnet));
    
    setpoint = FirstJoin;
    setpoint2 = SecondJoin;
    setpoint3= ThirthJoin;
    setpoint4 = FourthJoin;
  }
  /*
  Serial.print(setpoint );
  Serial.print(" : ");
  Serial.print(setpoint2 );
  Serial.print(" : ");
  Serial.print(setpoint3 );
  Serial.print(" : ");
  Serial.print(setpoint4 );
  Serial.println(" : ");
  */
  
  // Compute PID
  myPID.Compute(N, input-lastinput);
  // Send power to motors
  if(abs(input-setpoint) == 0.0 ){
    pwmOut(0);output = 0; }
  else pwmOut(output); 
  
  myPID2.Compute(N2, input2-lastinput2); 
  if(abs(input2-setpoint2) == 0.0){
    pwmOut2(0);output2 = 0; }
  else pwmOut2(output2);
  
  myPID3.Compute(N3, input3-lastinput3);
  if(abs(input3-setpoint3) == 0.0){
    pwmOut3(0);output3 = 0; }
  else pwmOut3(output3); 
  
  myPID4.Compute(N4, input4-lastinput4);
  if(abs(input4-setpoint4) == 0.0){
    pwmOut4(0);output4 = 0; }
  else pwmOut4(output4);

  /*
  Serial.print(output );
  Serial.print(" : ");
  Serial.print(output2 );
  Serial.print(" : ");
  Serial.print(output3 );
  Serial.print(" : ");
  Serial.print(output4 );
  Serial.println(" : ");
  */
  lastinput =  input;
  lastinput2 =  input2;
  lastinput3 =  input3;
  lastinput4 =  input4;
    
}

void pwmOut(int out) {
   if(out<0) {
    analogWrite(M1,0);
    analogWrite(M2,abs(out)); }
   else {
   analogWrite(M2,0);
   analogWrite(M1,abs(out)); }
  }
void pwmOut2(int out2) {
   if(out2<0){
    analogWrite(M3,0);
    analogWrite(M4,abs(out2));
    }
   else {
    analogWrite(M4,0);
    analogWrite(M3,abs(out2));
    }
  }
 void pwmOut3(int out3) {
   if(out3<0) {
    analogWrite(M5,0);
    analogWrite(M6,abs(out3)); }
   else {
   analogWrite(M6,0);
   analogWrite(M5,abs(out3)); }
  }
void pwmOut4(int out4) {
   if(out4<0){
    analogWrite(M7,0);
    analogWrite(M8,abs(out4));
    }
   else {
    analogWrite(M8,0);
    analogWrite(M7,abs(out4));
    }
  }


void encoder_A() {
  transitiontime_A = micros() - lasttime_A; // this bit for sensing pulse duration
  if (digitalRead(ENC_A_B))
    encodercount_A++;                   // counting the pulses (position)
  else
    encodercount_A--;
  lasttime_A = micros();
}

void encoder_B() {
  transitiontime_B = micros() - lasttime_B; // this bit for sensing pulse duration
  if (digitalRead(ENC_B_B))
    encodercount_B++;                   // counting the pulses (position)
  else
    encodercount_B--;
  lasttime_B = micros();
}

void encoder_C() {
  transitiontime_C = micros() - lasttime_C; // this bit for sensing pulse duration
  if (digitalRead(ENC_C_B))
    encodercount_C++;                   // counting the pulses (position)
  else
    encodercount_C--;
  lasttime_C = micros();
}

void encoder_D() {
  transitiontime_D = micros() - lasttime_D; // this bit for sensing pulse duration
  if (digitalRead(ENC_D_B))
    encodercount_D++;                   // counting the pulses (position)
  else
    encodercount_D--;
  lasttime_D = micros();
}
String getValue(String data, char separator, int index)
{
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
String getSetpoints(String data, char separator, int index)
{
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

bool reading = false;

void readMsg(double returnArray[]){
  String msg;
  char x = Serial.read();
  if (x == '#' || reading){
    while (true){
      char y = Serial.read();
      if (y == '#'){
        returnArray[0] = getValue(msg, ":", 0).toDouble();
        returnArray[1] = getValue(msg, ":", 1).toDouble();
        reading = true;
          break;
      }
      msg = msg + y;
    }
  }
  
}

String readStringM(){
  String msg;
  char x = Serial.read();
  if (x == '#' || reading){
    while (true){
      char y = Serial.read();
      if (y == '#'){
        reading = true;
        return msg;
      }
      msg = msg + y;
    }
  }
  
}

double stringToDouble(String & str)   //<-- notice the "&"
{
  return atof( str.c_str() );
}
