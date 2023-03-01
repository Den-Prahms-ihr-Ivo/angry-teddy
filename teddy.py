#!/usr/bin/env python3

import RPi.GPIO as GPIO

from gpiozero import LED, Button
from subprocess import check_call

from random import randrange

from teddy_helper_functions.constants import *
from teddy_helper_functions.TeddyPlayer import TeddyPlayer
import time
import os
from teddy_helper_functions.LEDController import led_consumer
from threading import Thread, Timer
from queue import Queue
from rpi_ws281x import PixelStrip, ws

# https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/
# https://github.com/rpi-ws281x/rpi-ws281x-python/blob/master/examples/strandtest.py

current_playlist = 0

# Geteilte Warteschlange
led_queue = Queue()

# Consumer definieren
led_thread = Thread(target=led_consumer, args=(led_queue,))

# NeoPixel Definition
LED_STRIP = ws.WS2811_STRIP_GRB

led_strip = PixelStrip(LED_COUNT, LED_COM, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
led_strip.begin()

# GPIOs mit GPIO-Nummer ansprechen
GPIO.setmode(GPIO.BCM)

# Ein- und Ausgaenge definieren
# GPIOs 18-21 Sind Tabu, die werden vom Audio Schild benutzt.
GPIO.setup(PIR_SENSOR_GPIO, GPIO.IN)
#GPIO.setup(PLAYLIST_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
#GPIO.setup(EMPTY_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
#GPIO.setup(SHUTDOWN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

movement_led       = LED(MOVEMENT_LED)
movement_spotlight = LED(MOVEMENT_SPOTLIGHT)

playlist_btn = Button(PLAYLIST_BUTTON)
shutdown_btn = Button(SHUTDOWN_BUTTON, hold_time=2)
empty_btn    = Button(EMPTY_BUTTON)

sleep_timer = None

def play():
  """Spielt einen zufälligen Song aus der momentanen Playlist und passt die LEDs farblich an."""
  global current_playlist, led_strip

  player=TeddyPlayer() 
  player.play()
  player.quit()

  led_queue.put((LED_Mode.song, led_strip, PLAYLIST_MAPPING[current_playlist]))

def stop():
  """Stoppt den aktuellen Song, da manche Soundfiles viel zu lang sind."""
  player=TeddyPlayer() 
  player.stop()
  player.quit()

def advance_playlist():
  """Wählt die nächste Playlist aus und zeigt die aktuelle Playlist durch einen Farbcode an."""
  global current_playlist, led_strip
  current_playlist += 1
  current_playlist = 0 if current_playlist >= len(PLAYLIST_MAPPING) else current_playlist

  tmp_playlist = PLAYLIST_MAPPING[current_playlist]

  player=TeddyPlayer() 
  player.load(tmp_playlist["loading_path"])
  player.quit()

  led_queue.put((LED_Mode.playlist, led_strip, tmp_playlist))

# Eigentlich unnötig dafür ne extra Funktion zu haben
# Artefakt der anfänglichen Tests
def playlist_callback(button):
  advance_playlist()

def shutdown_callback(button):
  """Fährt das System für einen sicheres Trennen vom Stromkreis runter und räumt vorher noch auf."""
  global led_thread, led_queue
  
  # Sentinel Value in die Schlange hinzufügen und auf beenden des Threads warten
  led_queue.put((LED_Mode.shutdown, led_strip, None))
  led_thread.join()

  GPIO.cleanup()
  print("\n\nTschöö, gä!")
  check_call(['sudo', 'poweroff'])

def empty_callback(button):
  """Vorbereiteted Callback für den noch leeren Knopf"""
  print("Empty Button was pressed")
  stop()


def refresh_movement_detector():
  global movement_led, movement_spotlight, sleep_timer
  # Verlagert in extra movement callback-Funktion für eine 
  # enkoppelte Schaltung zwischen dem Pausieren der Erkennung von Bewegungen und dem Licht.
  # movement_led.off()
  # movement_spotlight.off()

  # Add Event again
  GPIO.add_event_detect(PIR_SENSOR_GPIO, GPIO.RISING, callback=detect_movement)

  # Refreshen vom Thread, da ich eine Threadinstanz nicht neustarten kann/darf
  sleep_timer = create_timer_thread()

# timer definieren
def create_timer_thread():
  return Timer(SLEEP_TIME, refresh_movement_detector)

sleep_timer = create_timer_thread()

def movement_timer_callback():
  global movement_led, movement_spotlight

  movement_led.off()
  movement_spotlight.off()

def detect_movement(PIR_Sensor):
  """
  Callback-Funktion fürs Erkennen von Bewegung und spielt einen zufälligen Song aus der aktuellen Playlist
  """
  global movement_led, movement_spotlight
  print("... BEWEGUNG ERKANNT!")
  
  # Song spielen
  play()

  # Remove Event – Sonst sammeln sich die Bewegungen und ich habe teilweise
  # multiple Song-Trigger.
  GPIO.remove_event_detect(PIR_SENSOR_GPIO)
  movement_led.on()
  movement_spotlight.on()
  movement_timer = Timer(MOVEMENT_TIMER_FADEOUT, movement_timer_callback)
  movement_timer.start()

  # Sleep Timer kümmert sich um das neue Hinzufügen des Call-Backs
  # nach Ablaufen der Zeit 
  sleep_timer.start()

  #time.sleep(SLEEP_TIMER)
  #GPIO.output(MOVEMENT_LED, False)

  # Add Event again
  #GPIO.add_event_detect(PIR_SENSOR_GPIO, GPIO.RISING, callback=detect_movement)


if __name__ == "__main__":
  # Initiale Playlist laden
  current_playlist = randrange(len(PLAYLIST_MAPPING))

  player=TeddyPlayer() 
  player.load(PLAYLIST_MAPPING[current_playlist]["loading_path"])
  player.quit()

  # LED Thread starten
  led_thread.start()
  # Anfangsanimation laufen lassen.
  led_queue.put((LED_Mode.startup, led_strip, None))
  
  time.sleep(START_UP_DELAY)
  led_queue.put((LED_Mode.ready, led_strip, PLAYLIST_MAPPING[current_playlist]))

  try:
    GPIO.setwarnings(False)
    GPIO.add_event_detect(PIR_SENSOR_GPIO, GPIO.RISING,  callback=detect_movement)

    playlist_btn.when_released = playlist_callback
    shutdown_btn.when_held = shutdown_callback
    empty_btn.when_released = empty_callback

    while True:
      time.sleep(0)

  except KeyboardInterrupt:
    # Sentinel Value in die Schlange hinzufügen und auf beenden des Threads warten
    led_queue.put((LED_Mode.shutdown, led_strip, None))
    led_thread.join()

    # clean up
    GPIO.cleanup()

    print("\n\nTschöö, gä!")

