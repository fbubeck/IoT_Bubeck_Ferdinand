
# HINWEISE ZUR BEARBEITUNG

## Das Project assignment2_2021_02 enthaelt 2 Verzeichnisse auf oberster Ebende:

	### /lib: hier sollte saemtlicher SourceCode abgelegt werden.

	### /tests: hier koennen bei Bedarf Tests abgelegt werden. Jedes Modul (also Datei), welche aus dem /lib-Verzeichnis getestet werden soll, sollte entsprechend der Ordnerstruktur in Unterordnern angelegt werden. Als Beispiel liegt ein Test fuer das Modul test_config_ready.py bei.

## Im Verzeichnis config sollen saemtliche Konfigurationen eingetragen werden. Dies betrifft speziell die Verbindung zum Message Broker als auch den Namen der Datenbank.

## Im Verzeichnis database sollte die SQLite Database angelegt werden.

## Im Paket dhbw_broker sollte via MQTTService die MQTT-Kommunikation abgebildet werden.

## Im Paket dhbw_util sind 2 Hilfsklassen vorhanden, die bei der Loesung der Aufgabe unterstuetzen, insbesondere Probleme mit Dateipfaden sollten dann vermieden werden koennen.

## AUSSCHLIESSLICH im Paket sensor_io und den vorgegebenen Klassen sollte der Code verwendet werden, welcher mit Sensorik/Aktorik (Temperatursensor + LED) arbeitet.

## Saemtliche vorgegebenen Klassen sollten auch verwendet werden, eigene Klassen duerfen aber hinzugefuegt werden.

## In der Datei .env kann der Pfad zum Ordner, in dem der Python Interpreter installiert ist, angegeben werden. Naeheres siehe: https://code.visualstudio.com/docs/python/environments

## Saemtliche externen Abhaengigkeiten sind in der beigefuegten requirements.txt zu pflegen.


