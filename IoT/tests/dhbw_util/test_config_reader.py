import sys, os
sys.path.append(os.path.realpath('./lib')) # Paketaufloesung ermoeglicht Zugriff auf alles unter /lib

import unittest
from unittest.mock import MagicMock
from dhbw_util.config_reader import ConfigReader # Zu testendes Modul wird importiert

class TestConfigReader(unittest.TestCase):

    def test_read_config(self):
       reader = ConfigReader()
       config = reader.read_config('brokerConfig.json')
       self.assertEqual(config.get('broker_port'), '1883') # Pruefe ob der Port 1883 configuriert wurde


    def test_read_config_with_mock(self):
         reader = ConfigReader()
         reader.read_config = MagicMock(return_value= { "broker_port" : '1884'})

         config = reader.read_config('brokerConfigUndEinTippfehler.json') # Simuliert einen Schreibfehler im SourceCode
         
         reader.read_config.assert_called_with('brokerConfig.json') # Prueft, ob der korrekte Dateiname uebergeben wurde und wird hier fehlschlagen

if __name__ == '__main__':
        print('TEST started!')
        unittest.main()
