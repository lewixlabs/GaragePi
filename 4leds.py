import RPi.GPIO as GPIO
import time 

# BCM Number of LED indicators
leds = [5, 13, 19, 6]

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for i in range(len(leds)):
        GPIO.setup(leds[i], GPIO.OUT)
        GPIO.output(leds[i], GPIO.LOW)

def start_leds(secs_between_leds):
        for led in leds:
            GPIO.output(led, GPIO.HIGH)
            time.sleep(secs_between_leds)
            #GPIO.output(led, GPIO.LOW)
    
def stop_leds():
        for led in leds:
            GPIO.output(led, GPIO.LOW)   

def main():
    init_gpio()
    try:
        while True:
            start_leds(0.1)
            time.sleep(2)
            stop_leds()
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("BYE")

if __name__ == "__main__":
    main()