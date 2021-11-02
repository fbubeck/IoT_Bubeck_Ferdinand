import sys, os
import time
import json
import re
sys.path.append(os.path.realpath('..'))
sys.path.append(os.path.realpath('../lib')) # Paketaufloesung ermoeglicht Zugriff auf alles unter /lib
from dhbw_util import config_reader
from dhbw_broker import mqtt_service
from dhbw_util import db_helper
from sensor_io import led
from sensor_io import thermo_sensor
import threading
from sensor_io import gpio_util

# Ab hier Start der Anwendung und schreiben des individuellen Codes

def main():
    #Objekte initialisieren
    reader = config_reader.ConfigReader()
    leds = led.Led()
    sensor = thermo_sensor.ThermoSensor()

    #Broker Config auslesen und Objekt erzeugen
    mqttServiceData = reader.read_config('brokerConfig.json')
    broker = mqtt_service.MqttService(mqttServiceData)
    

    #Datenbank Config auslesen und Objekt erzeugen
    dbConfig = reader.read_config('dbConfig.json')
    DB = db_helper.DbHelper(dbConfig)
    DB.create_db()

    frequency = 5 # 5 Sekunden Wartezeit

    # Methode, welche Sensorwerte ausliest und alle 5 Sekunden an den MQTT Broker sendet
    def produce():
        try:
            while True:
                temp = sensor.read()
                broker.publish(temp)
                DB.save_measurement(temp)
                time.sleep(frequency)
        except KeyboardInterrupt:
            gpio_util.cleanup()

    # Methode, welche alle 5 Sekunden Messages vom MQTT Broker empfängt und für die Steuerung der LED auswertet
    def consume():
        try:
            while True:
                time.sleep(frequency)
                message = broker.subscribe()
                print(message)
                temp = message.get("temperature")
                if (temp <= 20):
                    leds.set_ok_status()

                elif (temp >= 50 | temp >= 25):
                   leds.set_permanent_error_status()
                    
                else:
                    pass
                    #leds.set_warning_error_status()
        except KeyboardInterrupt:
            gpio_util.cleanup()

    # Einsatz von Threads zur Realisierung von Nebenläufigkeit und Erhaltung von einem Dauerzustand (Senden/Empfangen)
    # Threads initialisieren
    producer = threading.Thread(target = produce)
    consumer= threading.Thread(target = consume)

    # Threads starten
    producer.start()
    consumer.start()

        
if __name__ == '__main__':
    main()