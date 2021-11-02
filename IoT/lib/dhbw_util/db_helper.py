
# Helferklasse analog zu Folien Hardwarenahe Programmierung IoT-Entwicklung mit Python, S. 23-27 auszuprogrammieren
import sqlite3
from sqlite3 import Error
import sys
import os
import json

class DbHelper:

    #  Initialisierung mittels dbName als String, welcher aus der dbConfig.json vorher ausgelesen werden sollte
    def __init__(self, dbConfig):
        # Datenbankname aus Config Datei abspeichern
        self.db_name = dbConfig.get('dbName')
        
        sys.path.append(os.path.realpath('..'))
        dir = os.path.dirname(__file__)
        self.db_path = os.path.join(dir, 'database/' + str(self.db_name))
        print(self.db_path)


    # DB Datei einlesen und "Verbindung" zur DB herstellen
    def create_connection(self):
        #Hinweis zur Verbindung:   DB Pfad self.db_path im Objekt verwenden
        connection = None
        try:
            connection = sqlite3.connect(self.db_path)
            return connection
        except Error as error:
            print(error)
        return connection
    
    #  Legt die Datenbank an, wenn sie noch nicht existiert
    def create_db(self):
        sql_create_measurements_table = """ CREATE TABLE IF NOT EXISTS measurements(id integer PRIMARY KEY, timestamp DATETIME, sensor_temperature INTEGER, unit VARCHAR); """

        connection = self.create_connection()

        if connection is not None:
            self.create_table(connection, sql_create_measurements_table)
        else:
            print("Fehler! Verbindungsaufbau gescheitert.")

    # Legt ueber die aktive Verbindung eine Tabelle an via SQL Befehl als String
    def create_table(self, connection, create_table_sql):
        try:
            cursor = connection.cursor()
            cursor.execute(create_table_sql)
        except Error as error:
            print(error)


    # measurement ist Tupel (Zeitstempel, Messwert, Einheit)
    def save_measurement(self, measurement):
        try:
            connection = self.create_connection()
            cursor = connection.cursor()
            print("Verbindung offen.")

            timestamp = measurement["timestamp"]
            temp = measurement["temperature"]
            unit = measurement["unit"]
            params = (timestamp, temp, unit)

            sqlite_insert_query = """INSERT INTO ‘measurements‘
                (’id’, ’timestamp’, ’sensor_temperature’, 'unit')
                VALUES (NULL, ?, ?, ?);""" # Null für Autoincrement

            cursor.execute(sqlite_insert_query, params)
            connection.commit()
            print("Einfügen erfolgreich für %s Datensätze: ", cursor.rowcount)
            cursor.close()
        except sqlite3.Error as error:
            print("Fehler beim Einfügen", error)
        finally:
            if (connection):
                connection.close()
                print("Verbindung geschlossen")


    # gibt eine Liste von Tupeln zurueck mit Format entsprechend save_measurement
    def read_measurements(self):
        results = []
        try:
            connection = self.create_connection(self)
            cursor = connection.cursor()
            sqlite_select_query = """SELECT * from measurements"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            print("%s Messwerte gefunden", len(records))
            for row in records:
                results.append((row[1], row[2]))# row ist 3-Tupel (ID, Zeitstempel, Messwert)
            cursor.close()
            return results
        except sqlite3.Error as error:
            print("Fehler beim Lesen aus Tabelle", error)
        finally:
            if (connection):
                connection.close()

