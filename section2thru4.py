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
    section_end = section_start + section_len
    pattern_len = sum(sum(clump) for clump in pattern.durs)
    
    # --- opening unison ---
    pattern.instruments = random.sample(categories,random.randint(1,3)) # choose players
    opening_len = random.randint(10, 15) *.01 * section_len
    reps = max(2, round(opening_len / pattern_len)) # make repetition at least 2
    print(pattern.instruments,reps)
    
    for _ in range(reps):
        pattern.play()
        
    # --- Plans when the closing section will start, which is 25-35% of the section,
    # in whole reps, ending exactly at section_end ---
    closing_len = random.uniform(0.25, 0.35) * section_len # a rough random length
    closing_reps = max(2, round(closing_len / pattern_len))
    closing_len = closing_reps * pattern_len # rounded len by num of reps
    closing_start = section_end - closing_len
    
    # --- middle ---
    wait(closing_start - s.beat()) # for now
    
    # -- hocket dial --
    pattern.instruments = categories.copy()
    ramp_reps = 0.75 * closing_reps # how many reps the dail takes to go from 0 to 1
    
    reps_per_variant = max(1, round(6 / pattern_len))
    current_pattern = pattern
    
    # every ~6 beats (never at the start), switch to a new variant, keeping the player turns going
    for rep in range(closing_reps):
        time_for_new_variant = rep != 0 and rep % reps_per_variant == 0
        if time_for_new_variant:
            new_variant = pattern.random_variant()
            new_variant.continue_turns_from(current_pattern)
            current_pattern = new_variant
            
        current_pattern.hocket = min(1, rep / ramp_reps) # never above 1
        current_pattern.play()
        
    
    
    
        
    wait(section_end - s.beat())
    print(s.beat())
    
    
    
    
# Play sections
def play():
    section(get_pattern(1))
    section(get_pattern(3))
    section(get_pattern(2))
    
    