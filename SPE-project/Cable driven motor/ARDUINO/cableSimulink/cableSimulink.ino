  #include <PID_v1.h>

#define M1            10
#define M2            11  // motor's PWM outputs
#define M3            46
#define M4            44 // motor's PWM outputs

//double kp=65.4494536501632,ki=77.0781439031017,kd=0.0958821774106496, N =100; // good but not enough
//double kp=101.760676251617 ,ki=186.855469671902,kd=0.874940976211089, N=42.1307433461873;
double kp=22.2707628694451 ,ki=59.2428963251724/3.0,kd=2*0.539873470177468, N=17.4572555042356; 
double input=0, output=0, setpoint=0, lastinput=0;
PID myPID(&input, &output, &setpoint,kp,ki,kd, DIRECT);
volatile long encoder0Pos = 0;
long previousMillis = 0;// will store last time LED was updated


double kp2=kp ,ki2=ki,kd2=kd, N2=N; 
double input2=0, output2=0, setpoint2=0, lastinput2=0;
PID myPID2(&input2, &output2, &setpoint2,kp2,ki2,kd2, DIRECT);
volatile long encoder0Pos2 = 0;
long previousMillis2 = 0;        // will store last time LED was updated

// and for the encoder:
#define ENC_A_A 3 // pin connected to external interrupt
#define ENC_A_B 5 // pin connected to normal pin
#define ENC_B_A 19 // pin connected to external interrupt
#define ENC_B_B 7 // pin connected to normal pin
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

// Create a union to easily convert float to byte
typedef union{
  float number;
  double numberd;
  uint8_t bytes[4];
} FLOATUNION_t;


// Create the variable you want to send
FLOATUNION_t myValue;
FLOATUNION_t myValue2;
FLOATUNION_t myValue3;

//magnet
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
  //encoder
  pinMode(ENC_A_A, INPUT_PULLUP); // encoder A
  pinMode(ENC_A_B, INPUT_PULLUP);
  pinMode(ENC_B_A, INPUT_PULLUP); // encoder B
  pinMode(ENC_B_B, INPUT_PULLUP);
  // initialize serial, use the same boudrate in the Simulink Config block
  Serial.begin(115200);

  attachInterrupt(1, encoder_A, RISING);
  attachInterrupt(4, encoder_B, RISING);
  setpoint = 0;
  setpoint2 = 0; 

  //magnet
  pinMode(magPin, OUTPUT);
  digitalWrite(magPin, HIGH);
}

float angle;
String msg;
int x;
int y ;
char data;
unsigned long lastmill = 0 ;
unsigned long current = 0 ;
void loop(){
   position_A =  +(float) encodercount_A*(10.0/209.0)*10.0;
   position_B =  +(float) encodercount_B*(10.0/209.0)*10.0;
   /*
   Serial.print(position_A );
   Serial.print(" : ");
   Serial.print(position_B );
   Serial.println(" : ");
   */
   //position_B =  (float) encodercount_B*(360.0 /858);
   encoder0Pos = position_A;
   encoder0Pos2 = position_B;
   myValue2.number = position_A;
   myValue3.number = position_B;
   input = encoder0Pos;
   input2 = encoder0Pos2;
  
  
  // Print header: Important to avoid sync errors!
  current = millis();
  if(current-lastmill > 10){
    
    if(Serial.available() > 0){
        myValue.numberd = getFloat(); // IN reality this is a double
        setpoint = myValue.numberd;//myValue.number; 
        setpoint2 = myValue.numberd;//myValue.number; 
    }
    
    Serial.write('A'); 
    for (int i=0; i<4; i++){
      Serial.write(myValue2.bytes[i]); 
    }
    for (int i=0; i<4; i++){
      Serial.write(myValue3.bytes[i]); 
    }
    // Print terminator
    Serial.print('\n');
    lastmill = current;
  }
   
  myPID.Compute(N, lastinput-input);// wait till PID is actually computed in the mean time assert the endstop pins
  myPID2.Compute(N2, lastinput2-input2);// wait till PID is actually computed in the mean time assert the endstop pins
  
  if(abs(input-setpoint) == 0.0){
    pwmOut(0);output = 0; }
  else pwmOut(output); 
  
  if(abs(input2-setpoint2) == 0.0){
    pwmOut2(0);output2 = 0; }
  else pwmOut2(output2); 
  /*
  Serial.print(output );
  Serial.print(" : ");
  Serial.print(output2 );
  Serial.println(" : ");
  */
}


double getFloat(){
    int cont = 0;
    FLOATUNION_t f;
    while (cont < 4 ){
        f.bytes[cont] = Serial.read() ;
        cont = cont + 1;
    }
    return f.numberd;
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
