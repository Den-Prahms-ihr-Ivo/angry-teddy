#!/usr/bin/env python3

from musicpd import MPDClient
from constants import *

class TeddyPlayer:
  def __init__(self):
    self.client = MPDClient()
    self.client.connect(HOST, PORT)
    self.client.timeout = 10
    self.client.idletimeout = None 


  def quit(self):
    self.client.close()
    self.client.disconnect()

  def get_playlists(self):
    val = self.client.listplaylists()
    return val

  def get_playing(self):
    name = "unknown"
    val = self.client.currentsong()

    if "title" in val:
      name = val["title"]
    elif "file" in val:
      name = val["file"]
    else:
      name = "unknown"

    return name

  def load(self, playlist):
    print(f"Loading Playlist: {playlist}")
    self.client.clear()
    self.client.load(playlist)

  def play(self):
    self.client.play()

  def stop(self):
    self.client.stop()