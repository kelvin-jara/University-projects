#include <PID_v1.h>

#define M1            8
#define M2            9  // motor's PWM outputs
#define M3            11
#define M4            10 // motor's PWM outputs



//double kp=81.4688630740179 ,ki=86.6017195153668,kd=1.8397203026128, N=38.6820754878712;
double kp=101.760676251617 ,ki=186.855469671902,kd=0.874940976211089, N=42.1307433461873; 
double input=0, output=0, setpoint=0, lastinput=0;
PID myPID(&input, &output, &setpoint,kp,ki,kd, DIRECT);
volatile long encoder0Pos = 0;
long previousMillis = 0;// will store last time LED was updated

//double kp2=1.42,ki2=1.270,kd2=0.3500;

//better
//double kp2=1.0, ki2=1.0 ,kd2=0.0, N2 = 0.0; // goof but not enough
double kp2=10.4531321202476, ki2=16.843621605007,kd2=1.19069171337777, N2 = 18.3848501275142; // goof but not enough
double input2=0, output2=0, setpoint2=0, lastinput2=0;
PID myPID2(&input2, &output2, &setpoint2,kp2,ki2,kd2, DIRECT);
volatile long encoder0Pos2 = 0;
long previousMillis2 = 0;        // will store last time LED was updated


// and for the encoder:
#define ENC_A_A 2 // pin connected to external interrupt
#define ENC_A_B 4 // pin connected to normal pin
#define ENC_B_A 3 // pin connected to external interrupt
#define ENC_B_B 5 // pin connected to normal pin
// variables
float position_A; // controller variables as globals
float position_B; // controller variables as globals
// timing:
unsigned long loopTime, printTime; // timing
unsigned long loopTime2, printTime2; // timing
volatile long encodercount_A; 
volatile long encodercount_B; 
volatile unsigned long lasttime_A, transitiontime_A;
volatile unsigned long lasttime_B, transitiontime_B;



void setup() { 
  // motor
  myPID.SetMode(AUTOMATIC);
  myPID.SetOutputLimits(-255,255);
  // motor2
  myPID2.SetMode(AUTOMATIC);
  myPID2.SetOutputLimits(-255,255);
  //encoder
  pinMode(ENC_A_A, INPUT_PULLUP); // encoder A
  pinMode(ENC_A_B, INPUT_PULLUP);
  pinMode(ENC_B_A, INPUT_PULLUP); // encoder B
  pinMode(ENC_B_B, INPUT_PULLUP);
  Serial.begin (115200);
  attachInterrupt(0, encoder_A, RISING);
  attachInterrupt(1, encoder_B, RISING);
  setpoint = 0;
  setpoint2 = 0;  
} 


int i =0;
int now = 0;
long previousMillisForM = 0; 
long currentMillisForM = 0; 
volatile long Mencoder0Pos = 0;
volatile long Mencoder0Pos2 = 0;
void loop(){
     position_A =  +(float) encodercount_A*(10.0/209.0)*10.0;
     position_B =  -(float) encodercount_B*(10.0/209.0)*10.0;
     encoder0Pos = position_A;
     encoder0Pos2 = position_B;
     input = encoder0Pos;
     input2 = encoder0Pos2;
     if(Serial.available() > 0) {
      i = Serial.parseInt();
       if (i != 0){
        Serial.println(i);
        now = i;
        setpoint = 0;
        setpoint2 = i;
       } 
      
      //Serial.println(String(setpoint) + " : " + String(setpoint2));
      
    }
    myPID.Compute(N, input-lastinput);// wait till PID is actually computed in the mean time assert the endstop pins
    myPID2.Compute(N2, input2-lastinput2);
    if(input==setpoint){
      pwmOut(0);output = 0; }
    else pwmOut(output); 
    if(input2==setpoint2){
      pwmOut2(0);output2 = 0; }
    else pwmOut2(output2); 
    
  
}

void pwmOut(int out) {
   if(out<0){
    analogWrite(M1,0);
    analogWrite(M2,abs(out));
    }
   else {
    analogWrite(M2,0);
    analogWrite(M1,abs(out));
    }
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
  lastt
