import paho.mqtt.client as mqtt
import json

# Quelle: https://www.eclipse.org/paho/index.php?page=clients/python/index.php
# Quelle: https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
class MqttService:

    #  Initialisierung mittels zuvor eingelesener Datei brokerConfig.json
    def __init__(self, broker_config):
        # Attibute aus Config Datei für spätere Verwendung abspeichern
        self.brokerHost = broker_config.get('broker_host')
        self.brokerPort = broker_config.get('broker_port')
        self.dataTopic = broker_config.get('data_topic')
        self.message = {
                "timestamp": "init",
                "temperature": 0,
                "unit": "degrees Celsius"
            }

        # Instanziierung MQTT Client
        self.client = mqtt.Client()
        self.client.connect(self.brokerHost, int(self.brokerPort))
    
    # MQTT Nachricht absetzen
    def publish(self, data):
        # Callback Function, wenn Daten abgesendet wurden
        def on_publish(client, userdata, result):
            print("broker: data published")
        # Callback Zuweisung
        self.client.on_publish = on_publish
        # Payload in JSON umwandeln und mit publish an den Broker senden
        data_json = json.dumps(data)
        self.client.publish(self.dataTopic, data_json, 1)


    # MQTT Nachrichten erwarten
    def subscribe(self): 
        # Callback Function, wenn Client connected ist
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.client.subscribe(self.dataTopic, 1)
            else:
                print("client is not connected")

        # Callback Function, wenn eine Message empfangen wurde
        def on_message(client, userdata, message):
            print("broker: data received")
            self.message = json.loads(message.payload.decode("utf-8"))

        # Callback Zuweisungen
        self.client.on_connect = on_connect 
        self.client.on_message = on_message
        # Abrufen von Nachrichten durch inbuild loop aufrecht erhalten
        self.client.loop_start()

        return self.message


