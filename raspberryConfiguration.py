from time import sleep
from neopixel import *
import RPi.GPIO as GPIO
import random

# LED strip configuration:
LED_COUNT      = 7       # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

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
SPEAKER_PIN = 2
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

# Color
RED   = Color(255,  0,  0)
GREEN = Color(  0,255,  0)
BLUE  = Color(  0,  0,255)
WHITE = Color(  0,  0,  0)

def getStrip():
     # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    return strip

def setLedColor(strip, led, color):
    strip.setPixelColor(led-1, color)
    strip.show()

def buzzer():
    for i in range(25):
        GPIO.output(SPEAKER_PIN, True)
        sleep(0.005)
        GPIO.output(SPEAKER_PIN, False)
        sleep(0.005)

def validation(strip, led):
    for i in range(3):
        setLedColor(strip, led, GREEN)
        buzzer()
        sleep(0.25)
        setLedColor(strip, led, WHITE)
        sleep(0.25)

def setAllLedColor(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()

def setAllLedRandColor(strip):
    rand1 = random.randint(0,255)
    rand2 = random.randint(0,255)
    rand3 = random.randint(0,255)
    setAllLedColor(strip, Color(rand1,rand2,rand3))
    sleep(0.2)
