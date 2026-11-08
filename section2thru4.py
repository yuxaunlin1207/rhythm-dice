from prototypes import get_pattern
from scamp import *
from playback_setup import *
import random



# def play():
# #     start_beat = s.beat()
#     p_all = get_pattern(1)
#     p_all.instruments = ["metal", "wood", "skin"]
# #     while s.beat() - start_beat < 30:
#     for i in range(10):
#         p_all.hocket = i / 9
#         p_all.play()

def section(pattern, beat_len=40):
    pattern_len = sum(sum(clump) for clump in pattern.durs)
    
    # --- opening unison ---
    pattern.instruments = random.sample(categories,random.randint(1,3)) # choose players
    opening_len = random.randint(10, 15) *.01 * beat_len
    reps = max(2, round(opening_len / pattern_len)) # make repetition at least 2
    print(pattern.instruments,reps)
    
    for _ in range(reps):
        pattern.play()
    
    
    
# Play sections
def play():
    section(get_pattern(1))
    section(get_pattern(3))
    section(get_pattern(2))
    
    