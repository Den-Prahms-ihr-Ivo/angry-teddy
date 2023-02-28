#!/usr/bin/env python3
from rpi_ws281x import Color

HOST = 'localhost'
PORT = '6600'


SLEEP_TIME            = 100 # Schalfenszeit nach dem Erkennen einer Bewegung, bis wieder eine erkannt werden kann
LED_TIMER_FADEOUT     = 5 # Zeit in Sekunden, bis Playlist ausfadet
START_UP_DELAY        = 5 # Zeit in Sekunden, die das System wartet bis die Bewegungserkennung einsetzt. 
MOVEMENT_TIMER_FADEOUT= 5 # Zeit, die das Spotlight beim Erkennen einer Bewegung leuchtet 
                          # Diese Zahl muss kleiner sein als SLEEP_TIME.

# GPIOs 18-21 Sind Tabu, die werden vom Audio Schild benutzt.
PIR_SENSOR_GPIO       = 23
MOVEMENT_LED          = 24
MOVEMENT_SPOTLIGHT    = 25

PLAYLIST_BUTTON       = 16
EMPTY_BUTTON          = 6
SHUTDOWN_BUTTON       = 5

# LED strip configuration:
# PWM Pins PWM0 = 12/18 PWM1 = 13/19
LED_COUNT         = 48      # Number of LED pixels.
LED_COUNT_HALF    = 22      # Split für die Hälfte der beiden Seiten
LED_COM           = 13      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ       = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA           = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS    = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT        = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL       = 1       # set to '1' for GPIOs 13, 19, 41, 45 or 53 # TODO: falls das nicht funktinoiert, nimm, da sich die Angaben widersprechen



from enum import Enum
class LED_Mode(Enum):
    (playlist, song, startup, ready, shutdown) = range(5)


PLAYLIST_MAPPING = [
  {
    "loading_path": "russian",
    # Farbe des Backdrops - eine zweistellige Liste aus RGB-Tripeln
    "colour": [(0, 255, 20), (255, 0, 20)],
    # Farben bei Playlistauswahl - eine Liste aus Color-Objekten
    "playlist_colours": [Color(255, 255, 255), Color(0, 255, 20), Color(255, 0, 20)], 
  },{
    "loading_path": "german",
    # Farbe des Backdrops - eine zweistellige Liste aus RGB-Tripeln
    "colour": [(230, 0, 20), (255, 0, 208)],
    # Farben bei Playlistauswahl - eine Liste aus Color-Objekten
    "playlist_colours": [Color(0, 0, 0), Color(230, 0, 20), Color(255, 0, 208)], 
  },{
    "loading_path": "chaos",
    # Farbe des Backdrops - eine zweistellige Liste aus RGB-Tripeln
    "colour": [(255, 0, 20), (255, 0, 20)],
    # Farben bei Playlistauswahl - eine Liste aus Color-Objekten
    "playlist_colours": [Color(255, 0, 20), Color(255, 0, 20), Color(255, 0, 20)], 
  },{
    "loading_path": "french",
    # Farbe des Backdrops - eine zweistellige Liste aus RGB-Tripeln
    "colour": [(20, 255, 0), (255, 0, 20)],
    # Farben bei Playlistauswahl - eine Liste aus Color-Objekten
    "playlist_colours": [Color(20, 255, 0), Color(255, 255, 255), Color(255, 0, 20)], 
  },{
    "loading_path": "spetsnaz",
    # Farbe des Backdrops - eine zweistellige Liste aus RGB-Tripeln
    "colour": [(255, 0, 20), (255, 0, 206)],
    # Farben bei Playlistauswahl - eine Liste aus Color-Objekten
    "playlist_colours": [Color(255, 0, 20), Color(255, 0, 206), Color(255, 0, 20)], 
  },{
    "loading_path": "polish",
    # Farbe des Backdrops - eine zweistellige Liste aus RGB-Tripeln
    "colour": [(255, 0, 20), (255, 255, 255)],
    # Farben bei Playlistauswahl - eine Liste aus Color-Objekten
    "playlist_colours": [Color(255, 0, 20), Color(255, 255, 255), Color(0, 0, 0)], 
  },{
    "loading_path": "zombie",
    # Farbe des Backdrops - eine zweistellige Liste aus RGB-Tripeln
    "colour": [(0, 20, 255), (0, 20, 255)],
    # Farben bei Playlistauswahl - eine Liste aus Color-Objekten
    "playlist_colours": [Color(0, 20, 255), Color(0, 20, 255), Color(0, 20, 255)], 
  },{
    "loading_path": "screaming",
    # Farbe des Backdrops - eine zweistellige Liste aus RGB-Tripeln
    "colour": [(183, 255, 0), (183, 255, 0)],
    # Farben bei Playlistauswahl - eine Liste aus Color-Objekten
    "playlist_colours": [Color(183, 255, 0), Color(183, 255, 0), Color(183, 255, 0)], 
  },{
    "loading_path": "dreadnaught",
    # Farbe des Backdrops - eine zweistellige Liste aus RGB-Tripeln
    "colour": [(0, 255, 20), (255, 255, 255)],
    # Farben bei Playlistauswahl - eine Liste aus Color-Objekten
    "playlist_colours": [Color(0, 255, 20), Color(255, 255, 255), Color(0, 255, 20)], 
  },{
    "loading_path": "english",
    # Farbe des Backdrops - eine zweistellige Liste aus RGB-Tripeln
    "colour": [(0, 255, 20), (255, 10, 10)],
    # Farben bei Playlistauswahl - eine Liste aus Color-Objekten
    "playlist_colours": [Color(255, 10, 10), Color(255, 255, 255), Color(0, 255, 20)], 
  },{
    "loading_path": "italian",
    # Farbe des Backdrops - eine zweistellige Liste aus RGB-Tripeln
    "colour": [(20, 0, 255), (255, 0, 20)],
    # Farben bei Playlistauswahl - eine Liste aus Color-Objekten
    "playlist_colours": [Color(20, 0, 255), Color(255, 255, 255), Color(255, 0, 20)], 
  },{
    "loading_path": "dutch",
    # Farbe des Backdrops - eine zweistellige Liste aus RGB-Tripeln
    "colour": [(255, 0, 111), (255, 0, 111)],
    # Farben bei Playlistauswahl - eine Liste aus Color-Objekten
    "playlist_colours": [Color(255, 0, 111), Color(255, 255, 255), Color(20, 255, 0)], 
  }
]
