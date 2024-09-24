#include <Servo.h>
#include<SoftwareSerial.h>
SoftwareSerial mySerial(2,3);
Servo swivel;
Servo tilt;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  mySerial.begin(9600);
  mySerial.write(0x7C);
  mySerial.write(128+21);
  mySerial.write(157);
  mySerial.write(12);
  mySerial.write(17);
  swivel.attach(9);
  tilt.attach(10);
  pinMode(4, OUTPUT);
  swivel.write(0);
  tilt.write(90);
}

void loop() {
  if (Serial.available()) {
    // put your main code here, to run repeatedly:
    char var = Serial.read();  //input from RPI
    //Serial.println(var);
    switch (var) {
      case '1':  //bluecircle
        moveServo(33,60);
        mySerial.write(12);
        mySerial.write("Blue Circle");
        delay(2000);
        mySerial.write(12);
        Serial.println("1");
        break;
      case '2':  //greencircle
        moveServo(62,60);
        mySerial.write(12);
        mySerial.write("Green Circle");
        delay(2000);
        mySerial.write(12);
        Serial.println("2");
        break;
      case '3':  //bluecircle
        moveServo(91,60);
        mySerial.write(12);
        mySerial.write("Red Circle");
        delay(2000);
        mySerial.write(12);
        Serial.println("3");
        break;
      case '4':  //redtriangle
        moveServo(120,60);
        mySerial.write(12);
        mySerial.write("Blue Triangle");
        delay(2000);
        mySerial.write(12);
        Serial.println("4");
        break;
      case '5':  //greentriangle
        moveServo(148.5,60);
        mySerial.write(12);
        mySerial.write("Green Triangle");
        delay(2000);
        mySerial.write(12);
        Serial.println("5");
        break;
      case '6':  //bluetriangle
        moveServo(33,120);
        mySerial.write(12);
        mySerial.write("Red Triangle");
        delay(2000);
        mySerial.write(12);
        Serial.println("6");
        break;
      case '7':  //redsquare
        moveServo(62,120);
        mySerial.write(12);
        mySerial.write("Blue Square");
        delay(2000);
        mySerial.write(12);
        Serial.println("7");
        break;
      case '8':  //greensquare
        moveServo(91,120);
        mySerial.write(12);
        mySerial.write("Green Square");
        delay(2000);
        mySerial.write(12);
        Serial.println("8");
        break;
      case '9':  //bluesquare
        moveServo(120,120);
        mySerial.write(12);
        mySerial.write("Red Square");
        delay(2000);
        mySerial.write(12);
        Serial.println("9");
        break;
      case '0':  //undefined
        moveServo(148.5,120);
        mySerial.write(12);
        mySerial.write("Undefined");
        delay(2000);
        mySerial.write(12);
        Serial.println("10");
        
        break;
    }
    moveServo(0,90);
    delay(300);
  }
}

void moveServo(int angle1, int angle2) {
  //int i;
  for (int i = 0; i <= angle1; i++) {
    swivel.write(i);
    delay(50);
  }
  if (angle2 < 90) {
    for (int j = 90; j >= angle2; j--) {
      tilt.write(j);
      delay(50);
    }
    delay(2500);
    for (int j = angle2; j < 90; j++) {
      tilt.write(j);
      delay(50);
    }
  } else if (angle2 > 90) {
    for (int k = 90; k <= angle2; k++) {
      tilt.write(k);
      delay(50);
    }
    delay(2500);
    for (int k = angle2; k > 90; k--) {
      tilt.write(k);
      delay(50);
    }
  }
  for (int i = angle1; i >= 0; i--) {
    swivel.write(i);
    delay(50);
  }
}