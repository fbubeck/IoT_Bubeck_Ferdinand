import os
import glob
import time
import RPi.GPIO as GPIO
from datetime import datetime, timezone

# Quelle: https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/
class ThermoSensor:

    #  Initialisierung
    def __init__(self):
        # Der One-Wire EingangsPin wird deklariert und der integrierte PullUp-Widerstand aktiviert
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Nach Aktivierung des Pull-UP Widerstandes wird gewartet,
        # bis die Kommunikation mit dem DS18B20 Sensor aufgebaut ist
        print ('Warte auf Initialisierung des Sensors...')

        base_dir = '/sys/bus/w1/devices/'
        while True:
            try:
                device_folder = glob.glob(base_dir + '28*')[0]
                break
            except IndexError:
                time.sleep(0.5)
                continue
        self.device_file = device_folder + '/w1_slave'

    #  liest die Temperatur ein in °C und gibt ein Dictionary zurueck im Format: 
    #  { "timestamp" : "2020-09-16T08:00:01.345+02:00", "temperature" : 25, "unit" : "degrees Celsius" }
    def read(self):
        # Innere Methode zum Messen
        def TemperaturMessung(self):
                f = open(self.device_file, 'r')
                lines = f.readlines()
                f.close()
                return lines
        # Temperaturmessung und Auswertung
        lines = TemperaturMessung(self)
        timestamp = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = TemperaturMessung(self)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            dict = {
                "timestamp": timestamp,
                "temperature": int(temp_c),
                "unit": "degrees Celsius"
            }

            return dict
            
        
