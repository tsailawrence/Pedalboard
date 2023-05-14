
from pedalboard import Pedalboard, Chorus, Reverb
from pedalboard.io import AudioFile

# Make a Pedalboard object, containing multiple audio plugins:


board = Pedalboard([Chorus(), Reverb(room_size=0.25)])
