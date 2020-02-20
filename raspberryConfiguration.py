from time import sleep
from neopixel import *
import RPi.GPIO as GPIO

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# LED strip configuration:
LED_COUNT      = 7       # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Touch Sensor configuration:
TOUCH_PIN_1 = 5
TOUCH_PIN_2 = 19
TOUCH_PIN_3 = 20
TOUCH_PIN_4 = 21
TOUCH_PIN_5 = 25
TOUCH_PIN_6 = 26
TOUCH_PIN_7 = 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TOUCH_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TOUCH_PIN_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TOUCH_PIN_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TOUCH_PIN_5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TOUCH_PIN_6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TOUCH_PIN_7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Buzzer configuration
SPEAKER_PIN = 4
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)

# Button configuration
BUTTON_PIN_1 = 13
BUTTON_PIN_2 = 14
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# OLED Display configuration
DISPLAY_PIN = 24
disp = Adafruit_SSD1306.SSD1306_128_64(rst=DISPLAY_PIN)
disp.begin() 

# Color
RED   = Color(255,  0,  0)
GREEN = Color(  0,255,  0)
BLUE  = Color(  0,  0,255)
WHITE = Color(  0,  0,  0)

def setLedColor(led, color):
    strip.setPixelColor(led-1, color)
    strip.show()

def setAllLedColor(color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()

def buzzer():
    for i in range(25):
        GPIO.output(SPEAKER_PIN, True)
        sleep(0.005)
        GPIO.output(SPEAKER_PIN, False)
        sleep(0.005)

def validation(led):
    for i in range(3):
        setLedColor(led, GREEN)
        buzzer()
        sleep(0.25)
        if i==2:
            setLedColor(led, GREEN)
        else:
            setLedColor(led, RED)
            sleep(0.25)

def loadscreen():
    disp.clear()
    disp.display()
    image = Image.open('logo.ppm').convert('1')
    disp.image(image)
    disp.display()

def clearscreen():
    disp.clear()
    disp.display()

def helloWord():
    disp.clear()
    disp.display()
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((0,0),'Hello',font=font,fill=255)
    draw.text((0,10),'World!',font=font,fill=255)
    disp.image(image)
    disp.display()
