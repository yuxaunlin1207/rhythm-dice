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

def section(pattern, section_len=40):
    print(s.beat())
    section_start = s.beat()
    pattern_len = sum(sum(clump) for clump in pattern.durs)
    
    # --- opening unison ---
    pattern.instruments = random.sample(categories,random.randint(1,3)) # choose players
    opening_len = random.randint(10, 15) *.01 * section_len
    reps = max(2, round(opening_len / pattern_len)) # make repetition at least 2
    print(pattern.instruments,reps)
    
    for _ in range(reps):
        pattern.play()
        
    # --- closing hocket ---
    closing_len = random.uniform(0.25, 0.35) * section_len # a rough random length
    closing_reps = max(2, round(closing_len / pattern_len))
    closing_len = closing_reps * pattern_len # rounded len by num of reps
    section_end = section_start + section_len
    closing_start = section_end - closing_len
    
    # --- middle ---
    wait(closing_start - s.beat()) # for now
    
    # -- hocket dail --
    pattern.instruments = categories.copy()
    ramp_reps = 0.75 * closing_reps # how many reps the dail takes to go from 0 to 1
    for rep in range(closing_reps):
        pattern.hocket = min(1, rep / ramp_reps) # never above 1
        pattern.play()
    
    
    
        
    wait(section_end - s.beat())
    print(s.beat())
    
    
    
    
# Play sections
def play():
    section(get_pattern(1))
    section(get_pattern(3))
    section(get_pattern(2))
    
    