#!/usr/bin/env python3

from queue import Queue
from threading import Timer
from teddy_helper_functions.constants import LED_Mode, LED_TIMER_FADEOUT, LED_COUNT_HALF
import time 

from rpi_ws281x import Color

# Hier musste jetzt noch Timer und so hinzufügen
# und später dann die LED Kontrolle

led_timer = None

# ###########################################
# Animationen
# ###########################################
#
def fade_out(led_strip, left_colour, right_colour, wait_ms=50, step=3):
  print("Fade Out....")
  left_r = left_colour[0]
  left_g = left_colour[1]
  left_b = left_colour[2]

  right_r = right_colour[0]
  right_g = right_colour[1]
  right_b = right_colour[2]

  while True:

    for i in range(0, LED_COUNT_HALF):
      led_strip.setPixelColor(i, Color(right_r, right_g, right_b))
    
    for i in range(LED_COUNT_HALF, led_strip.numPixels() - 3):
      led_strip.setPixelColor(i, Color(left_r, left_g, left_b))

      
    led_strip.show()

    if (left_r <= 0 and left_g <= 0 and left_b <= 0 and right_r <= 0 and right_g <= 0 and right_b <= 0):
      break

    left_r = max(0, left_r - step)
    left_g = max(0, left_g - step)
    left_b = max(0, left_b - step)

    right_r = max(0, right_r - step)
    right_g = max(0, right_g - step)
    right_b = max(0, right_b - step)

    time.sleep(wait_ms / 1000.0)

  print("Fertig mit Fade OUT-Function")

def playlist_black_out(led_strip):
  
  for i in range(led_strip.numPixels() - 3, led_strip.numPixels()):
    led_strip.setPixelColor(i, Color(0, 0, 0))
    
  led_strip.show()


def blackout(led_strip):
  for i in range(led_strip.numPixels() - 3, led_strip.numPixels()):
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

def animate_startup(led_strip, wait_ms=100):
  print("Starting animation ....")

  c = (50, 255, 5)
  colour = Color(*c)

  for _ in range(3):
    for q in range(3):
      for i in range(0, led_strip.numPixels(), 3):
          led_strip.setPixelColor(i + q, colour)
      led_strip.show()
      time.sleep(wait_ms / 1000.0)
      for i in range(0, led_strip.numPixels(), 3):
          led_strip.setPixelColor(i + q, 0)
  
  fade_out(led_strip, c, c)

def animate_shutdown(led_strip, wait_ms=50):
  colour = Color(255, 0, 0)

  for _ in range(2):
    for q in range(3):
      for i in range(0, led_strip.numPixels(), 3):
          led_strip.setPixelColor(i + q, colour)
      led_strip.show()
      time.sleep(wait_ms / 1000.0)
      for i in range(0, led_strip.numPixels(), 3):
          led_strip.setPixelColor(i + q, 0)
  
  blackout(led_strip)


def animate_ready(led_strip, signal):
  global led_timer

  _, colour, playlist_colours = signal.values()

  led_strip.setPixelColor(led_strip.numPixels() - 3, playlist_colours[2])
  led_strip.setPixelColor(led_strip.numPixels() - 2, playlist_colours[1])
  led_strip.setPixelColor(led_strip.numPixels() - 1, playlist_colours[0])

  led_strip.show()
  # Der Grundgedanke hier ist, 5 Sekunden die LEDs leuchten zu lassen und dann auszufaden

  # besteht bereits ein timer, dann cancel ihn
  if led_timer is not None:
    led_timer.cancel()

  led_timer = Timer(LED_TIMER_FADEOUT/2, lambda: playlist_black_out(led_strip))
  led_timer.start()

  fade_out(led_strip, colour[0], colour[1], wait_ms=40, step=10)

# ###########################################
# Bearbeiten von Input Signalen
# ###########################################
#
def process_playlist_change(led_strip, signal):
  global led_timer

  # LEDs starten
  _, colour, playlist_colours = signal.values()

  print(f"Sprachenfarbe: {colour}")

  for i in range(0, led_strip.numPixels()):
    led_strip.setPixelColor(i, Color(0, 0, 0))

  print(playlist_colours[2])

  led_strip.setPixelColor(led_strip.numPixels() - 3, playlist_colours[2])
  led_strip.setPixelColor(led_strip.numPixels() - 2, playlist_colours[1])
  led_strip.setPixelColor(led_strip.numPixels() - 1, playlist_colours[0])

  led_strip.show()
  # Der Grundgedanke hier ist, 5 Sekunden die LEDs leuchten zu lassen und dann auszufaden

  # besteht bereits ein timer, dann cancel ihn
  if led_timer is not None:
    led_timer.cancel()

  led_timer = Timer(LED_TIMER_FADEOUT, lambda: playlist_black_out(led_strip))
  led_timer.start()

def process_song_change(led_strip, signal):
  global led_timer

  # TODO: implement
  # LEDs starten
  _, colour, _ = signal.values()
  left_colour  = colour[0]
  right_colour = colour[1]

  print(f"Sprachenfarbe: {left_colour} - {right_colour}")

  for i in range(0, LED_COUNT_HALF):
    led_strip.setPixelColor(i, Color(right_colour[0], right_colour[1], right_colour[2]))
  
  for i in range(LED_COUNT_HALF, led_strip.numPixels() - 3):
    led_strip.setPixelColor(i, Color(left_colour[0], left_colour[1], left_colour[2]))

  led_strip.show()
  # Der Grundgedanke hier ist, 5 Sekunden die LEDs leuchten zu lassen und dann auszufaden

  # besteht bereits ein timer, dann cancel ihn
  # Da habe ich mich vorerst aus folgendem Grund gegen entschieden:
  # - Die Playlist-LEDs "hängen" nach einem schnellen Erkennen einer Bewegung
  # - auf Grund der Erkennungs-Wartezeit kann es nicht zu einer Überschneidung kommen.
  #if led_timer is not None:
    #led_timer.cancel()

  led_timer = Timer(LED_TIMER_FADEOUT, lambda: fade_out(led_strip, left_colour, right_colour))
  led_timer.start()

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
      break

    # item hat jetzt die Form (LED_Mode, LED_Strip Objekt, signal )
    mode, led_strip, signal = item #TODO: Mode shutdpwn

    if mode == LED_Mode.playlist:
      process_playlist_change(led_strip, signal)

    elif mode == LED_Mode.song:
      process_song_change(led_strip, signal)

    elif mode == LED_Mode.startup:
      animate_startup(led_strip)

    elif mode == LED_Mode.ready:
      animate_ready(led_strip, signal)

    elif mode == LED_Mode.shutdown:
      animate_shutdown(led_strip)
      break

  print("LED Consumer ist fertig!")

