import RPi.GPIO as GPIO
import time

import subprocess
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


################################################ LEDS FUNCTIONS ################################################
# BCM Number of LED indicators
leds = [5, 13, 19, 6]
displayBOO = False

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


################################################ DISPLAY FUNCTIONS ################################################
def init_display():
    # Create the I2C interface.
    i2c = busio.I2C(SCL, SDA)

    # Create the SSD1306 OLED class.
    # The first two parameters are the pixel width and pixel height.  Change these
    # to the right size for your display!
    disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

    # Clear display.
    disp.fill(0)
    disp.show()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new("1", (disp.width, disp.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)

    # Load default font.
    font = ImageFont.load_default()

    # Alternatively load a TTF font.  Make sure the .ttf font file is in the
    # same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    # font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

    return disp,draw,image,font

def update_display(display_object,draw_object,img_prm,fnt_prm):
    # Draw a black filled box to clear the image.
    draw_object.rectangle((0, 0, display_object.width, display_object.height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    #cmd = "hostname -I | cut -d' ' -f1"
    #IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    
    cmd = '/usr/bin/vcgencmd measure_temp'
    CPUTemp = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'cut -f 1 -d " " /proc/loadavg'
    CPULoad = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"RAM: %s/%sMB %.0f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%dGB  %s", $3,$2,$5}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    # bottom = disp.height - padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Write four lines of text.
    draw_object.text((x, top + 0), "CPU " + CPUTemp.replace("=",": "), font=fnt_prm, fill=255)
    draw_object.text((x, top + 8), "CPU load: " + CPULoad, font=fnt_prm, fill=255)
    draw_object.text((x, top + 16), MemUsage, font=fnt_prm, fill=255)
    draw_object.text((x, top + 25), Disk, font=fnt_prm, fill=255)

    # Display image.
    display_object.image(img_prm)
    display_object.show()

def update_display_boo(display_object,draw_object,img_prm,fnt_prm):
    # Draw a black filled box to clear the image.
    draw_object.rectangle((0, 0, display_object.width, display_object.height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    
    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    # bottom = disp.height - padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Write four lines of text.
    draw_object.text((x, top + 0), "IP: " + IP, font=fnt_prm, fill=255)

    # Display image.
    display_object.image(img_prm)
    display_object.show()


def main():
    init_gpio()
    disp,draw,img,fnt = init_display()
    try:
        while True:
            start_leds(0.1)
            if displayBOO:
                update_display_boo(disp,draw,img,fnt)
            else:
                update_display(disp,draw,img,fnt)
            time.sleep(1)
            stop_leds()
            time.sleep(1)
            displayBOO = not displayBOO
            
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("BYE")

if __name__ == "__main__":
    main()