from prototypes import get_pattern
from scamp import *
from playback_setup import *
from copy import deepcopy
import random


#  =================
#        Sect 1    
#  =================
def wood_sect1():
    p1 = get_pattern(1)
    p1.instruments = ["wood"]
    last_combo = None
    
    # in every group of 8 reps for pattern 1, there is one variation
    for group in range(8):
        change_at = random.randint(0,7)
        for rep in range(8):
            if rep == change_at:
                variant = deepcopy(p1)
                # variant.pitch_shift(0, invert=True)
                combo = (False, 0, False)
                while combo == (False, 0, False) or combo == last_combo:
                    combo = (random.random()<0.5, # invert?
                             random.randint(0, 2), # shift amount
                             random.random()<0.5 # retrograde?
                             )
                last_combo = combo
                print(group, change_at, combo)
                
                (invert, shift, retro) = combo
                variant.pitch_shift(shift, invert=invert)
                if retro:
                    variant.rotate(0,retrograde=True)
                
                variant.play()
                
            else :
                p1.play()


def metal_sect1():
    p2 = get_pattern(2)
    p2.instruments = ["metal"]
    i = 0 # which cycle we're on
    
    while s.beat() <= 32:
        p2.skipped_indices = [-1] if i % 2 == 1 else []
        p2.silent_indices = [0] if i in [3, 5] else []
        
        p2.play()
        i += 1
        
    order = random.sample(range(7), 7) # shuffle [0, ... ,6]
    start = s.beat() # where erosion begins
    
    while s.beat() < 48:
        p2.skipped_indices = [-1] if i % 2 == 1 else []
        
        full_len = sum(sum(clump) for clump in p2.durs)
        last_note_dur = p2.durs[-1][-1]
        cycle_len = full_len - last_note_dur if i % 2 == 1 else full_len
        
        progress = (s.beat() + cycle_len - start) / (48 - start) # measure at the end of each cycle
        how_many = round(progress * 7) #in int
        
        p2.silent_indices = order[0 : how_many]
        p2.play()
        i += 1
        
        
def skin_sect1():
    p3 = get_pattern(3)
    p3.instruments = ["skin"]
    
    page_gaps = [2.5, 2, 1.5, 1]
    for cycle_num, gap in enumerate(page_gaps):
        if cycle_num < 3:
            p3.silent_indices = [-1] # silence the last note
        else:
            p3.silent_indices = [] # silence nothing
        
        p3.play()
        wait(gap)
    
    n = sum(len(clump) for clump in p3.pitches) # total number of notes
    order = random.sample(range(n), n) # shuffle [0, ... ,n]
    start = s.beat()
    
    full_len = sum(sum(clump) for clump in p3.durs)
    
    while s.beat() + full_len <= 48: # check if notes fit
        gap = max(0, gap - 0.5) # shrink gap every cycle
        cycle_len = full_len + gap
        
        progress = (s.beat() + cycle_len - start) / (48 - start) # measure at the end of each cycle
        how_many = round(progress * n)
        p3.silent_indices = order[0 : how_many]
        p3.play()
        wait(gap)
            

def play():
    fork(wood_sect1)
    wait(4) # metal enters at beat 4
    fork(metal_sect1)
    wait(10.5)
    fork(skin_sect1)
    wait_for_children_to_finish()
