from gpiozero import PWMLED
import RPi.GPIO as GPIO
import time

class Led:

    #  Initialisierung
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.LED_ROT = 24
        self.LED_GRUEN = 23
        self.dauer = 0.5
        GPIO.setup(self.LED_ROT, GPIO.OUT, initial= GPIO.LOW)
        GPIO.setup(self.LED_GRUEN, GPIO.OUT, initial= GPIO.LOW)

    #  laesst die LED dauerhaft GRUEN LEUCHTEN
    def set_ok_status(self):
        GPIO.output(self.LED_ROT,GPIO.LOW)
        GPIO.output(self.LED_GRUEN,GPIO.HIGH) 
        time.sleep(self.dauer)

    #  laesst die LED fuer n Sekunden ROT BLINKEN 
    def set_warning_error_status(self):
        GPIO.output(self.LED_ROT,GPIO.LOW)
        GPIO.output(self.LED_GRUEN,GPIO.LOW)
        try:
            while True:
                GPIO.output(self.LED_ROT,GPIO.HIGH)
                time.sleep(self.dauer)
                GPIO.output(self.LED_ROT,GPIO.LOW)
                time.sleep(self.dauer)
        finally:
            GPIO.close()

    #  laesst die LED dauerhaft ROT LEUCHTEN 
    def set_permanent_error_status(self):
        GPIO.output(self.LED_GRUEN,GPIO.LOW)
        GPIO.output(self.LED_ROT,GPIO.HIGH) 
        time.sleep(self.dauer)

