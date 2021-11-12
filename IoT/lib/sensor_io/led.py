import RPi.GPIO as GPIO
import time

# Quelle: https://github.com/DennisSchulmeister/dhbwka-wwi-iottech-quellcodes/blob/master/03%20Python/Entwicklung%20eines%20IoT-Devices/loesung/src/my_iot_device/statusled.py
class Led:

    #  Initialisierung
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.LED_ROT = 24
        self.LED_GRUEN = 23
        self.dauer = 0.5
        GPIO.setup(self.LED_ROT, GPIO.OUT)
        GPIO.setup(self.LED_GRUEN, GPIO.OUT)

    #  laesst die LED dauerhaft GRUEN LEUCHTEN
    def set_ok_status(self):
        GPIO.output(self.LED_ROT,GPIO.LOW)
        GPIO.output(self.LED_GRUEN,GPIO.HIGH) 
        time.sleep(self.dauer)

    #  laesst die LED fuer n Sekunden ROT BLINKEN 
    def set_warning_error_status(self):
        GPIO.output(self.LED_GRUEN,GPIO.LOW) 
        pwm = GPIO.PWM(self.LED_ROT, 10)

        pwm.start(25)
        print("LED blinkt")

    #  laesst die LED dauerhaft ROT LEUCHTEN 
    def set_permanent_error_status(self):
        GPIO.output(self.LED_GRUEN,GPIO.LOW)
        GPIO.output(self.LED_ROT,GPIO.HIGH) 
        time.sleep(self.dauer)

