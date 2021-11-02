import paho.mqtt.client as mqtt
import json
import time


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

        #Instanziierung MQTT Client
        self.client = mqtt.Client()
        self.client.connect(self.brokerHost, int(self.brokerPort))
    
    # MQTT Nachricht absetzen
    def publish(self, data):

        def on_publish(client, userdata, result):
            print("data published")

        self.client.on_publish = on_publish
        data_json = json.dumps(data)
        self.client.publish(self.dataTopic, data_json, 1)



    # MQTT Nachrichten erwarten
    def subscribe(self): 
        
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.client.subscribe(self.dataTopic, 1)
            else:
                print("client is not connected")        

        def on_message(client, userdata, message):
            self.message = json.loads(message.payload.decode("utf-8"))
           

        self.client.on_connect = on_connect 
        self.client.on_message = on_message

        self.client.loop_start()

        return self.message


