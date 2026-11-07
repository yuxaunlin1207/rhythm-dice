from prototypes import get_pattern
from scamp import *
from playback_setup import *
import random



def play():
#     start_beat = s.beat()
    p_all = get_pattern(1)
    p_all.instruments = ["metal", "wood", "skin"]
#     while s.beat() - start_beat < 30:
    for i in range(10):
        p_all.hocket = i / 9
        p_all.play()