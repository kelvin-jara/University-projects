//butt
//#define TRIGGER 22
//#define ECHO 24
//front
//#define TRIGGER 28
//#define ECHO 30

float distanceWall = 25;

#include <UltrasonicSensor.h>

UltrasonicSensor ultrasonicButt (22, 24);
UltrasonicSensor ultrasonicFront (28, 30);

// pin definitions for the motorshield
#define BRAKE_B 8 // 9 for output A
#define BRAKE_A 9 // 9 for output A
#define PWM_A 3  // 3 for output A
#define PWM_B 11  // 3 for output A
#define DIR_A 12  // 12 for output A
#define DIR_B 13  // 12 for output A
// and for the encoder:
#define ENC_A_A 2 // pin connected to external interrupt
#define ENC_A_B 4 // pin connected to normal pin
#define ENC_B_A 19 // pin for PCINT because pin 3 is in use
#define ENC_B_B 6 // pin connected to normal pin
// for the current:
#define CURRENT_A A0
#define CURRENT_B A1

// variables
float position_A, setpoint_A, error_A, velocity_A; // controller variables as globals
float position_B, setpoint_B, error_B, velocity_B; // controller variables as globals
// variables for PID control
float previousError_A, errorRate_A, sumError_A;
float previousError_B, errorRate_B, sumError_B;
// timing:
unsigned long loopTime, printTime; // timing
unsigned long loopTime2;
volatile long encodercount_A; // encoder: global accessed from Interrupt: volatile
volatile long encodercount_B; // encoder: global accessed from Interrupt: volatile
int mode; // mode 0: direct PWM, mode 1: P control
volatile unsigned long lasttime_A, transitiontime_A;
volatile unsigned long lasttime_B, transitiontime_B; 
float Kp = 6;//6.0;
float Kd = 0.0003;//5.0;
float Ki= 0.00;
float antiWindup = 200;
int loopDelay = 50;
int mvalue;

void setup() {
  //distance sensor
   int temperature = 22;//idk why this but well
  ultrasonicButt.setTemperature(temperature);
  ultrasonicFront.setTemperature(temperature);




  //controlles
  pinMode(BRAKE_A, OUTPUT);     // brake
  pinMode(BRAKE_B, OUTPUT);       // brake
  pinMode(PWM_A, OUTPUT);         // PWM
  pinMode(DIR_A, OUTPUT);         // dir
  pinMode(ENC_A_A, INPUT_PULLUP); // encoder A
  pinMode(ENC_A_B, INPUT_PULLUP);
  pinMode(PWM_B, OUTPUT);         // PWM
  pinMode(DIR_B, OUTPUT);         // dir
  pinMode(ENC_B_A, INPUT_PULLUP); // encoder B
  pinMode(ENC_B_B, INPUT_PULLUP);
  Serial.begin(115200);
  attachInterrupt(0, encoder_A, RISING); // std. external interrupt
  attachInterrupt(4, encoder_B, RISING); // std. external interrupt
  //attachPinChangeInterrupt(); // different style interrupt for encoder B
  setpoint_B = 0; // remove this: just for testing!!
  setpoint_A = 0;
  mode = 1; // also, your choice, 
 // mvalue=1;
}


int n;

int lastn;
volatile unsigned long   stepf=200;
int laststepf;
int stepr=270;//300
int laststepr;
int diff;
int counter;
 int xx[30];
void loop() {
  if (millis() > loopTime + 49) { // 20 Hz output
    loopTime = millis();      // reset looptimer
// distance sensing
  int distanceButt = ultrasonicButt.distanceInCentimeters();
  int distanceFront = ultrasonicFront.distanceInCentimeters();

  if (distanceFront<0) distanceFront=00;
  if (distanceButt<0) distanceButt=00;
  
  if (distanceFront > distanceWall&&distanceButt<=distanceWall) {
     // Serial.println("go straight");
      n=1;
  }
  
  if (distanceButt <= distanceWall&&distanceFront <= distanceWall) {
      //Serial.println("turn right");
      n=3;
  }

  if (distanceButt>distanceWall){
   // Serial.println("turn left");
      n=2;
  }

  // else n=0;
diff=abs(lastn-n);

//diff=lastn-n;
mvalue=n;

if(diff>1){
  counter ++; 
    xx[counter]=n;
  }

  if(counter>30){
    mvalue=n ;
    counter=0;
  }
  
  if(counter>0&&counter<30)mvalue=xx[1];
  //if(position_A)
  // */
  
if(diff=1&&counter>10){
 mvalue=1;
}  
  if(mvalue==0)nomove();
  if(mvalue==1){
    forward(-stepf);
    stepf=stepf+30;
    if (distanceFront<=10){
      
      rotate_R(stepr);
      stepf=0;
      position_A=0;
      position_B=0;
      setpoint_A=0;
      setpoint_B=0;
      //delay(100);
    }

  }
 // if(mvalue==2)rotate_L(stepr);
  if(mvalue==2)forward(-stepf); 
  if(mvalue==3)rotate_R(stepr);
  if(mvalue==4)back(stepf);


//mvalue=n; 



    
// sample point
    // this bit for measuring velocity through pulse transition time:
    if (transitiontime_B > 0) velocity_B = 2094.40 / transitiontime_B; // in [rad/sec] so 2*pi / (30*100ppr*transitiontime)/1000.000[s] = 6283000/(3000*transitiontime) = 2094.40/transitiontime
    else velocity_B = 0;
    if (transitiontime_A > 0) velocity_A = 2094.40 / transitiontime_A; // in [rad/sec] so 2*pi / (30*100ppr*transitiontime)/1000.000[s] = 6283000/(3000*transitiontime) = 2094.40/transitiontime
    else velocity_A = 0;
    // wheel position in degrees
    position_B = (360 * (float) encodercount_B) / (100 * 30); // degrees: 100 PPR, 1:30 gear, 360 deg/rev. in [rad] it would be 2*pi*(float)encodercount/(100*30)
    position_A = (360 * (float) encodercount_A) / (100 * 30); // degrees: 100 PPR, 1:30 gear, 360 deg/rev. in [rad] it would be 2*pi*(float)encodercount/(100*30)
// control 
    // simple feedback control -- This is where the control magic happens:
    error_B = setpoint_B - position_B;  // error signal
    error_A = setpoint_A - position_A;  // error signal
    errorRate_A = 50*(previousError_A - error_A)/loopDelay;
    errorRate_B = 50*(previousError_B - error_B)/loopDelay;    
    
    if (mode == 1) {
      setMotor_B(Kp * error_B-Kd * errorRate_B);// + 50*(Ki * sumError_B)/loopDelay); // Proportional control
      setMotor_A(Kp * error_A-Kd * errorRate_A);// + 50*(Ki * sumError_A)/loopDelay); // Proportional control
    }
    
    // direct PWM (for testing, step response, etc)
    if (mode == 0) {
      setMotor_B(setpoint_B); // direct PWM
      setMotor_A(setpoint_A); // direct PWM
    }
    previousError_A = error_A;  // differential
    previousError_B = error_B;  // differential
    sumError_A = constrain(sumError_A + error_A, -antiWindup, antiWindup);  // integral
    sumError_B = constrain(sumError_B + error_B, -antiWindup, antiWindup);  // integral
//error less than a threshol
// find points to move


/*
  if (previousError_A <= 7 ){
mvalue=n;
}
  if (previousError_A > 7 ){
mvalue=lastmvalue;
}
*/

/*
if (previousError_A <= 0.1*setpoint_B && mvalue==1){
  setpoint_B=0;
  position_B=0;
  setpoint_A=0;
  position_A=0;
}
if (previousError_A <= 0.1*setpoint_B && mvalue==4){
  setpoint_B=0;
  position_B=0;
  setpoint_A=0;
  position_A=0;
}

*/

// serial monitor output
/*
    Serial.print(millis());
    Serial.print("\t");     // tab
    Serial.print(setpoint_A);
    Serial.print("\t");
    Serial.print((int)position_A);
    Serial.print("\t");     // tab
    Serial.print(setpoint_B);
    Serial.print("\t");
    Serial.print((int)position_B);*/
    Serial.print(n);
    Serial.print('\t');
    Serial.print(counter);
    Serial.print('\t');
    Serial.print(diff);
    Serial.print('\t');
    Serial.print(mvalue);
    Serial.print('\t');    
    Serial.print(distanceButt);
    Serial.print('\t');
    Serial.println(distanceFront);
  }
}



/// go forward
// len must be  in meters
void nomove(){
  Serial.print("not moving");
  Serial.print('\t');
  setpoint_A=0;
  setpoint_B=0;
}
void forward(int len){
  Serial.print("going forward");
  Serial.print('\t');
  
  setpoint_A=-len;
  setpoint_B=+len;
  
}
void back(int len){
  Serial.print("going backwards");
  Serial.print('\t');
  // len=300;
  setpoint_A=+len;
  setpoint_B=-len;
}
/// rotate
void rotate_L(int deg){
  Serial.print("rotating left"); 
  Serial.print('\t');
  //int deg=300;
  setpoint_A = -deg; 
  setpoint_B = -deg;
}
void rotate_R(int deg){
  Serial.print("rotating rigth");
  Serial.print('\t');
  //int deg=300;
  setpoint_A = deg; 
  setpoint_B = deg;
}










////// ===== DON'T start messing with the code below this line ====////
// encoder interrupt routine
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
// Set motor, use brake when 0 is sent
void setMotor_A(int value) {
  if (value > 0) {
    digitalWrite(DIR_A, HIGH);
    digitalWrite(BRAKE_A, LOW);
    analogWrite(PWM_A, min(value, 255));
  }
  else if (value < 0) {
    digitalWrite(DIR_A, LOW);
    digitalWrite(BRAKE_A, LOW);
    analogWrite(PWM_A, min(abs(value), 255));
  }
  else {
    digitalWrite(DIR_A, LOW);
    digitalWrite(BRAKE_A, HIGH);
    analogWrite(PWM_A, 0);
  }
}

// Set motor, use brake when 0 is sent
void setMotor_B(int value) {
  if (value > 0) {
    digitalWrite(DIR_B, HIGH);
    digitalWrite(BRAKE_B, LOW);
    analogWrite(PWM_B, min(value, 255));
  }
  else if (value < 0) {
    digitalWrite(DIR_B, LOW);
    digitalWrite(BRAKE_B, LOW);
    analogWrite(PWM_B, min(abs(value), 255));
  }
  else {
    digitalWrite(DIR_B, LOW);
    digitalWrite(BRAKE_B, HIGH);
    analogWrite(PWM_B, 0);
  }
}
