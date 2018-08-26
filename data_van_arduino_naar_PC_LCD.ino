#include "DHT.h" //gebruik 1.2.2 anders werkt dit prgm niet
#define DHTPIN 7     //welke pin de dht11 aan verbonden is (moet digitale pin zijn!!!)
#define DHTTYPE DHT11   //type bepalen 
DHT dht(DHTPIN, DHTTYPE);// verplichte lijn o prgm te laden
#include <SoftwareSerial.h>//serial communicatie toestaan

#include <LiquidCrystal.h>
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
byte a[8] = {
  0b01100,
  0b10010,
  0b10010,
  0b01100,
  0b00000,
  0b00000,
  0b00000,
  0b00000
};


void setup() 
{
    //LiquidCrystal lcd(45,35,47,49,51,53);//LCD setup

    lcd.begin(20, 4);
    lcd.createChar(0,a);
    lcd.setCursor(0, 1);//start voor waar de print moet starten
    lcd.clear();
    pinMode(A0, INPUT);
    Serial.begin(9600);
    while (!Serial) 
      {
      // wachten tot ubs is aangesloten
      }
      //setSyncProvider
    Serial.println("Data send testing");
}

void loop() 
  { 
   
lcd.clear();
    while(1)
     {

      int T = dht.readTemperature();//temperatuur; set readTemperature(true) voor fahrenheit
      int V = dht.readHumidity();//vochtigheid
      delay(2000);// wacht 2 seconde
      int licht =analogRead(A0);
      int zuurstof=analogRead(A1);

      
      

      Serial.print(T);// stuur de data door(temperatuur,vochtigheid, seconden na start)
      Serial.print(" ");
      Serial.print(V);
      Serial.print(" ");
      Serial.print(licht);
      Serial.print(" ");
      Serial.print(zuurstof);     
      Serial.println();
      //start lcd display
      lcd.setCursor(0, 0);
      lcd.print("T=");
      lcd.setCursor(3, 0);
      lcd.print(T);
      lcd.setCursor(8, 0);
      lcd.write(byte(0));
      lcd.setCursor(9, 0);
      lcd.print("C");

      lcd.setCursor(0, 1);
      lcd.print("v=");
      lcd.setCursor(3, 1);
      lcd.print(V);
      lcd.setCursor(8, 1);
      lcd.print("%");

      lcd.setCursor(0, 2);
      lcd.print("L=");
      lcd.setCursor(3, 2);
      lcd.print(licht);
      lcd.setCursor(8, 2);
      lcd.print("lux");

      lcd.setCursor(0, 3);
      lcd.print("z=");
      lcd.setCursor(3, 3); 
      lcd.print(zuurstof);
      lcd.setCursor(8, 3);
      lcd.print("ppm");
      

      
      }
  }
