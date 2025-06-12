float temp;
int tempPin = 3;

void setup () {
  Serial.begin (9600);
}
void loop () {
 
  temp = analogRead (tempPin); // read analog volt from sensor and save to variable temp
  temp = temp * 0.048828125; //convert sensor reading to Celsius
  Serial.print(temp); // display temperature value
  Serial.println();
  delay(1000); // update sensor reading each one second
  
}