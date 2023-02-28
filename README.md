# Ein wütender Teddy

Ein Teddybär, der dich beim Betreten des Zimmers anschreit.

Die Schritte, zum Einrichten des Raspberrys, habe ich leider nicht dokumentiert.
Auch die, beim Start ausgeführten, Scripts sind hier nicht zu finden

- Einrichten des Audiointerfaces
- Automatisches Mounten des USB-Sticks
- Automatisches erstellen und updaten der Playlists bei einem Neustart
- Automatisches starten des Teddy-Scripts
- Installieren von Python und der ganze Kleinkram

Das Script <teddy.py> wird nach dem Start des Raspberrys automatisch ausgeführt und der Teddy ist betriebsbereit

### Achtung - Samplerate der verwendeten Soundfiles

Aus einem, mir bis jetzt unerfindlichem, Grund kann mein verwendetes Audio Hifi DAC (HiFi DAC HAT PCM5122) nur 48kHz Audiofiles abspielen.

Darauf beim Befüllen des USB-Sticks achten!
