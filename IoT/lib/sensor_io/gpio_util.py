import RPi.GPIO as GPIO

# Ein Grundsatz der Verwendung von RPI.GPIO besagt, dass die Main Methode frei von GPIO actions sein soll.
# Aus diesem Grund wurde die Methode GPIO.cleanup() in diese separate Datei ausgelagert.
def cleanup():
    GPIO.cleanup()