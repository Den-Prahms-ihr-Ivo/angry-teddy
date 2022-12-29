#!/usr/bin/env python3

from queue import Queue
from threading import Timer
from constants import LED_Mode, LED_TIMER_FADEOUT
import time 

from rpi_ws281x import Color

# Hier musste jetzt noch Timer und so hinzufügen
# und später dann die LED Kontrolle

led_timer = None

# ###########################################
# Animationen
# ###########################################
#
def fade_out():
  # TODO: implement
  print("Fade Out....")

def blackout():
  # TODO: implement
  print("BlackOUT!")

  return # TODO anpassen, ich muss immer den strip übergeben
  for i in range(max(led_strip.numPixels(), led_strip.numPixels())):
    led_strip.setPixelColor(i, Color(0, 0, 0))
    led_strip.show()

def wheel(pos):
  """Generate rainbow colors across 0-255 positions."""
  if pos < 85:
    return Color(pos * 3, 255 - pos * 3, 0)
  elif pos < 170:
    pos -= 85
    return Color(255 - pos * 3, 0, pos * 3)
  else:
    pos -= 170
    return Color(0, pos * 3, 255 - pos * 3)

def theaterChaseRainbow(strip, wait_ms=50):
  """Rainbow movie theater light style chaser animation."""
  for j in range(256):
    for q in range(3):
      for i in range(0, strip.numPixels(), 3):
        strip.setPixelColor(i + q, wheel((i + j) % 255))
      strip.show()
      time.sleep(wait_ms / 1000.0)
      for i in range(0, strip.numPixels(), 3):
        strip.setPixelColor(i + q, 0)

def animate_startup():
  # TODO: implement
  print("Starting animation ....")

# ###########################################
# Bearbeiten von Input Signalen
# ###########################################
#
def process_playlist_change(led_strip, signal):
  global led_timer

  # TODO: implement
  # LEDs starten
  print(f"Playlist Farbwahl: {signal}")

  # Der Grundgedanke hier ist, 5 Sekunden die LEDs leuchten zu lassen und dann auszufaden

  # besteht bereits ein timer, dann cancel ihn
  if led_timer is not None:
    led_timer.cancel()

  # neuen Timer stellen
  led_timer = Timer(LED_TIMER_FADEOUT, fade_out)
  led_timer.start()

def process_song_change(led_strip, signal):
  # Hier einfach irgendwelche Effekte laufen lassen
  print(f"Song Farbwahl: {signal}")

# ###########################################
# Consumer Definition
# ###########################################
#
def led_consumer(queue: Queue):
  print("LED Consumer läuft...")
  while True:
    item = queue.get()

    if item is None:
      # LEDs auschhalten & Loop beenden
      blackout()
      break

    # item hat jetzt die Form (LED_Mode, LED_Strip Objekt, signal )
    mode, led_strip, signal = item

    if mode == LED_Mode.playlist:
      process_playlist_change(led_strip, signal)

    elif mode == LED_Mode.song:
      process_song_change(led_strip, signal)

    elif mode == LED_Mode.startup:
      animate_startup()

  print("LED Consumer ist fertig!")
