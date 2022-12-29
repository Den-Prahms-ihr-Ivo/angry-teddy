#!/usr/bin/env python3

import RPi.GPIO as GPIO
from teddy_helper_functions.constants import *
from teddy_helper_functions.TeddyPlayer import TeddyPlayer
import time
import os
from teddy_helper_functions.LEDController import led_consumer
from threading import Thread, Timer
from queue import Queue
from rpi_ws281x import PixelStrip

# https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/
# https://github.com/rpi-ws281x/rpi-ws281x-python/blob/master/examples/strandtest.py

current_playlist = 0

# Geteilte Warteschlange
led_queue = Queue()

# Consumer definieren
led_thread = Thread(target=led_consumer, args=(led_queue,))


# NeoPixel Definition
led_strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
led_strip.begin()

# GPIOs mit GPIO-Nummer ansprechen
GPIO.setmode(GPIO.BCM)

# Ein- und Ausgaenge definieren
# GPIOs 18-21 Sind Tabu, die werden vom Audio Schild benutzt.
GPIO.setup(PIR_SENSOR_GPIO, GPIO.IN)
GPIO.setup(SWITCH_PLAYLIST_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(MOVEMENT_LED, GPIO.OUT)


def play():
  """Spielt einen zufälligen Song aus der momentanen Playlist und passt die LEDs farblich an."""
  global current_playlist, led_strip

  player=TeddyPlayer() 
  player.play()
  print(f"Now playling: {player.get_playing()}")
  player.quit()

  led_queue.put((LED_Mode.song, led_strip, PLAYLIST_MAPPING[current_playlist]["colour"]))

def advance_playlist():
  """Wählt die nächste Playlist aus und zeigt die aktuelle Playlist durch einen Farbcode an."""
  global current_playlist, led_strip
  current_playlist += 1
  current_playlist = 0 if current_playlist >= len(PLAYLIST_MAPPING) else current_playlist

  tmp_playlist = PLAYLIST_MAPPING[current_playlist]

  player=TeddyPlayer() 
  player.load(tmp_playlist["loading_path"])
  player.quit()

  led_queue.put((LED_Mode.playlist, led_strip, tmp_playlist["colour"]))

# Eigentlich unnötig dafür ne extra Funktion zu haben
# Artefakt der anfänglichen Tests
def button_callback(button):
  advance_playlist()

def shutdown(button):
  """Fährt das System für einen sicheres Trennen vom Stromkreis runter und räumt vorher noch auf."""
  global led_thread, led_queue

  # Sentinel Value in die Schlange hinzufügen und auf beenden des Threads warten
  led_queue.put(None)
  led_thread.join()

  GPIO.cleanup()

  print("\n\nTschöö, gä!")
  os.system("sudo shutdown -h now")
  time.sleep(1)

  
def refresh_movement_detector():
  GPIO.output(MOVEMENT_LED, False)

  # Add Event again
  GPIO.add_event_detect(PIR_SENSOR_GPIO, GPIO.RISING, callback=detect_movement)

# timer definieren
sleep_timer = Timer(SLEEP_TIME, refresh_movement_detector)

def detect_movement(PIR_Sensor):
  """
  Callback-Funktion fürs Erkennen von Bewegung und spielt einen zufälligen Song aus der aktuellen Playlist
  """
  print("... BEWEGUNG ERKANNT!")
  
  # Song spielen
  play()

  # Remove Event – Sonst sammeln sich die Bewegungen und ich habe teilweise
  # multiple Song-Trigger.
  GPIO.remove_event_detect(PIR_SENSOR_GPIO)
  GPIO.output(MOVEMENT_LED, True)
  
  # Sleep Timer kümmert sich um das neue Hinzufügen des Call-Backs
  # nach Ablaufen der Zeit 
  sleep_timer.start()

  #time.sleep(SLEEP_TIMER)
  #GPIO.output(MOVEMENT_LED, False)

  # Add Event again
  #GPIO.add_event_detect(PIR_SENSOR_GPIO, GPIO.RISING, callback=detect_movement)


if __name__ == "__main__":

  # Initiale Playlist laden
  player=TeddyPlayer() 
  player.load(PLAYLIST_MAPPING[current_playlist]["loading_path"])
  player.quit()

  # LED Thread starten
  led_thread.start()
  # Anfangsanimation laufen lassen.
  led_queue.put((LED_Mode.startup, led_strip, None))
  
  time.sleep(START_UP_DELAY)

  try:
    GPIO.setwarnings(False)
    GPIO.add_event_detect(SWITCH_PLAYLIST_GPIO, GPIO.FALLING, callback=button_callback)
    GPIO.add_event_detect(PIR_SENSOR_GPIO, GPIO.RISING, callback=detect_movement)
    # TODO
    #GPIO.add_event_detect(SHUTDOWN_BUTTON, GPIO.RISING, callback=shutdown)

    while True:
      time.sleep(0)

  except KeyboardInterrupt:
    # Sentinel Value in die Schlange hinzufügen und auf beenden des Threads warten
    led_queue.put(None)
    led_thread.join()

    # clean up
    GPIO.cleanup()
    print("\n\nTschöö, gä!")

