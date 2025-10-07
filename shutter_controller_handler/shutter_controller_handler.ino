int receivedByte;
int shutterStatus;
int ttlPin = 10;

void writeShutter(int value){
    digitalWrite(ttlPin, value);
    digitalWrite(13, value);
}

void setup() {
  Serial.begin(9600);
  pinMode(ttlPin, OUTPUT);
  pinMode(13, OUTPUT);
}

void loop() {
  if(Serial.available()>0){
    receivedByte = Serial.read();
    
    if(receivedByte == 49){
      writeShutter(1);
      Serial.println("Shutter on");
      shutterStatus = 1;
    } else if(receivedByte == 48){
      writeShutter(0);
      Serial.println("Shutter off");
      shutterStatus = 0;
    } else if(receivedByte == 63){
      Serial.println(shutterStatus);
    };
    
  };
}
