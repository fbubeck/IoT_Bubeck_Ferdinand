import sys, os
import time
sys.path.append(os.path.realpath('..'))
sys.path.append(os.path.realpath('../lib')) # Paketaufloesung ermoeglicht Zugriff auf alles unter /lib
from dhbw_util import config_reader
from dhbw_broker import mqtt_service
from dhbw_util import db_helper
from sensor_io import led
from sensor_io import thermo_sensor
import threading
from sensor_io import gpio_util

# Der nachfolgende Code wurde von Ferdinand Bubeck geschrieben, basierend auf der Vorlesung und den angegebenen Quellen

def main():
    # Objekte initialisieren
    reader = config_reader.ConfigReader()
    leds = led.Led()
    sensor = thermo_sensor.ThermoSensor()

    # Broker Config auslesen und Broker-Objekt erzeugen
    mqttServiceData = reader.read_config('brokerConfig.json')
    broker = mqtt_service.MqttService(mqttServiceData)

    # Datenbank Config auslesen und DB-Objekt erzeugen
    dbConfig = reader.read_config('dbConfig.json')
    DB = db_helper.DbHelper(dbConfig)
    DB.create_db()

    # Variable für das Intervall von Senden und Abrufen
    frequency = 5


    # Methode, welche Sensorwerte ausliest, in die DB speichert und alle 5 Sekunden an den MQTT Broker sendet
    def produce():
        try:
            while True:
                temp = sensor.read()
                broker.publish(temp)
                DB.save_measurement(temp)
                time.sleep(frequency)
        except KeyboardInterrupt:
            gpio_util.cleanup()

    # Globale Variablen außerhalb der Nested Function initialisieren
    start = 0
    flag = True # Flag, wenn Temperatur erstmalig über 20 Grad ist, damit Zeit ab diesem Zeitpunkt gestoppt werden kann

    # Methode, welche alle 5 Sekunden Messages vom MQTT Broker empfängt und für die Steuerung der LED auswertet
    def consume():
        try:
            while True:
                time.sleep(frequency)
                # Messages vom Broker abrufen und für späteren Ablauf speichern
                message = broker.subscribe()
                print("message payload: ", message)
                temp = message.get("temperature")
                # Überprüfen, ob Temperatur erstmalig über 20 Grad ist und Timer ab diesem Zeitpunkt starten
                nonlocal flag
                if (temp > 20 and flag == True):
                    print("Zeit neu gesetzt")
                    nonlocal start
                    start = time.time()
                    flag = False

                # Berechne Zeitdauer zwischen Zeitpunkt, bei dem Temp das 1. mal über 20 Grad ist und jedem weiteren Schleifendurchlauf
                now = time.time()
                duration = int(now-start)
                print("Timer: ", duration)

                # LED Steuerung:
                # Liegt die Temperatur bei maximal 20 °C, leuchtet die LED kontinuierlich grün, Flag wird wieder aktiviert
                if (temp <= 20):
                    leds.set_ok_status()
                    flag = True

                # Liegt die Temperatur für maximal 60 Sekunden über 20°C und unter 50°C, blinkt die LED rot
                elif (temp > 20 and temp < 50 and duration < 60):
                    leds.set_warning_error_status()

                # Ab 50°C oder bei Temperaturwerten über 25 °C länger als 60 Sekunden leuchtet die LED kontinuierlich rot
                elif (temp >= 50 or temp > 25 and duration > 60):
                   leds.set_permanent_error_status()

        except KeyboardInterrupt:
            gpio_util.cleanup()

    # Einsatz von Threads zur Realisierung von Nebenläufigkeit und Erhaltung von einem Dauerzustand (Senden/Empfangen)
    # Threads initialisieren
    producer = threading.Thread(target = produce)
    producer.name = "iot-producer-thread"
    consumer = threading.Thread(target = consume)
    consumer.name = "iot-consumer-thread"

    # Threads starten
    producer.start()
    consumer.start()

        
if __name__ == '__main__':
    main()