
import json
import sys
import os

# Utility-Klasse zum Einlesen der Dateien im Ordner /config. 
class ConfigReader:

    def __init__(self):
        sys.path.append(os.path.realpath('..'))
        self.dir = os.path.dirname(__file__)

# Das zurueckgegebene Objekt ist ein Dictionary, die Werte koennen so gelesen werden:  data.get('Name_der_Eigenschaft_im_JSON')
    def read_config(self, filename):
        file_path = os.path.join(self.dir, '../config/' + filename)
        with open(file_path) as json_file:
            data = json.load(json_file)
            return data
           