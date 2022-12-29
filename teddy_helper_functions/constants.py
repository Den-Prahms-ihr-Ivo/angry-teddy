#!/usr/bin/env python3

HOST = 'localhost'
PORT = '6600'

SLEEP_TIME = 10 # Schalfenszeit nach dem Erkennen einer Bewegung, bis wieder eine erkannt werden kann

# GPIOs 18-21 Sind Tabu, die werden vom Audio Schild benutzt.
PIR_SENSOR_GPIO       = 23
MOVEMENT_LED          = 24
SWITCH_PLAYLIST_GPIO  = 25
SHUTDOWN_BUTTON       = -1 # TODO!!!!

# LED strip configuration:
# PWM Pins PWM0 = 12/18 PWM1 = 13/19
LED_COUNT         = 16      # Number of LED pixels.
LED_PIN           = 13      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ       = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA           = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS    = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT        = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL       = 1       # set to '1' for GPIOs 13, 19, 41, 45 or 53 # TODO: falls das nicht funktinoiert, nimm, da sich die Angaben widersprechen

LED_TIMER_FADEOUT     = 5 # Zeit in Sekunden, bis Playlist ausfadet
START_UP_DELAY        = 5 # Zeit in Sekunden, die das System wartet bis die Bewegungserkennung einsetzt. 


from enum import Enum
class LED_Mode(Enum):
    (playlist, song, startup) = range(3)


PLAYLIST_MAPPING = [
  {
    "loading_path": "russian",
    "colour": "#ccc",
    # TODO: playlists_colour oder so... 
  },{
    "loading_path": "german",
    "colour": "#ccc",
  },{
    "loading_path": "chaos",
    "colour": "#ccc",
  },{
    "loading_path": "french",
    "colour": "#ccc",
  },{
    "loading_path": "spetsnaz",
    "colour": "#ccc",
  },{
    "loading_path": "polish",
    "colour": "#ccc",
  },{
    "loading_path": "zombie",
    "colour": "#ccc",
  },{
    "loading_path": "screaming",
    "colour": "#ccc",
  },{
    "loading_path": "dreadnaught",
    "colour": "#ccc",
  },{
    "loading_path": "english",
    "colour": "#ccc",
  },{
    "loading_path": "italian",
    "colour": "#ccc",
  },{
    "loading_path": "dutch",
    "colour": "#ccc",
  }
]
