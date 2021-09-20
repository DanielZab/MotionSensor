#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

int ledPin = 2;                // choose the pin for the LED
int inputPin = 6;               // choose the input pin (for PIR sensor)
int pirState = LOW;             // we start, assuming no motion detected
int val = 0;                    // variable for reading the pin status
RF24 radio(7, 8); // CE, CSN
const byte address[6] = "27412";
void setup() {
  pinMode(ledPin, OUTPUT);      // declare LED as output
  pinMode(inputPin, INPUT);     // declare sensor as input
 
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
}
 
void loop(){
  val = digitalRead(inputPin);  // read input value
  
  if (val == HIGH)  // check if the input is HIGH
  {            
    digitalWrite(ledPin, HIGH);  // turn LED ON
  
    if (pirState == LOW) 
  {
      const char text[] = "Motion Detected";
      radio.write(&text, sizeof(text));// print on output change
      pirState = HIGH;
    }
  } 
  else 
  {
    digitalWrite(ledPin, LOW); // turn LED OFF
  
    if (pirState == HIGH)
  {
      const char text[] = "Motion Ended";
      radio.write(&text, sizeof(text));  // print on output change
      pirState = LOW;
    }
  }
}
