#include <ESP8266WiFi.h>
#include "ESP8266SMTP.h"
#define fsrPin A0
int fsrReading;

const char* ssid = "DLS-Pro";            		// WIFI network name
const char* password = "Abcd@1234";        		// WIFI network password
uint8_t connection_state = 0;           // Connected to WIFI or not
uint16_t reconnect_interval = 10000;    // If not connected wait time to try again

uint8_t WiFiConnect(const char* ssID, const char* nPassword)
{
	static uint16_t attempt = 0;
	Serial.print("Connecting to ");
	Serial.println(ssID);
	WiFi.begin(ssID, nPassword);

	uint8_t i = 0;
	while(WiFi.status() != WL_CONNECTED && i++ < 50) {
		delay(200);
		Serial.print(".");
	}
	++attempt;
	Serial.println("");
	if(i == 51) {
		Serial.print(F("Connection: TIMEOUT on attempt: "));
		Serial.println(attempt);
		if(attempt % 2 == 0)
			Serial.println(F("Check if access point available or SSID and Password are correct\r\n"));
		return false;
	}
	Serial.println(F("Connection: ESTABLISHED"));
	Serial.print(F("Got IP address: "));
	Serial.println(WiFi.localIP());
	return true;
}

void Awaits(uint16_t interval)
{
	uint32_t ts = millis();
	while(!connection_state){
		delay(50);
		if(!connection_state && millis() > (ts + interval)){
			connection_state = WiFiConnect(ssid, password);
			ts = millis();
		}
	}
}

void setup()
{
	Serial.begin(115200);
	delay(2000);
	
	connection_state = WiFiConnect(ssid, password);

	if(!connection_state) {  				// if not connected to WIFI
		Awaits(reconnect_interval);         // constantly trying to connect
	}

	uint32_t startTime = millis();
	while(1){
	  fsrReading = analogRead(fsrPin);

  Serial.print("Analog reading = ");
  Serial.print(fsrReading);     // the raw analog reading

  if (fsrReading == 0) {
    Serial.println(" - No pressure");
  } else if (fsrReading < 10) {
    Serial.println(" - Light touch");
  } else if (fsrReading < 50) {
    Serial.println(" - Light squeeze");
  } else if (fsrReading < 150) {
    Serial.println(" - Medium squeeze");
  } else {
    Serial.println(" - Big squeeze");
 
	SMTP.setEmail("gPBLgroup3@gmail.com")
		.setPassword("pfvcyp27")
		.Subject("doorbell notification")\
		.setFrom("SIT gPBL Group3")
		.setForGmail();						// simply sets port to 465 and setServer("smtp.gmail.com");						
																   // message text from http://www.blindtextgenerator.com/lorem-ipsum
	if(SMTP.Send("af17048@shibaura-it.ac.jp", "the doorbell of the entrance rang!")){
    Serial.println(F("Message sent"));
 
	} else {
		Serial.print(F("Error sending message: "));
		Serial.println(SMTP.getError());
	} 
	
	Serial.println(millis() - startTime);
}
delay(100);
}
}
void loop()
{}
