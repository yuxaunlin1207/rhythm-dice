from scamp import *
from playback_setup import *
import random
from prototypes import get_pattern

    
# -- ending of the piece --
def play(last_variant):
    tail_len = 30 # in beats
    tail_start = s.beat()
    tail_end = tail_start + tail_len
    
    p1 = get_pattern(1)
    p1.instruments = categories.copy()
    p1.hocket = 1
    
    # CROSSFADE: (~10 beats): Section 4's last variant becomes P1
    crossfade_len = 10
    crossfade_end = tail_start + crossfade_len
    prev = last_variant
    while s.beat() < crossfade_end:
        p1_odds = (s.beat() - tail_start) / crossfade_len # progress through the crossfade
        cur = p1 if random.random() < p1_odds else last_variant
        cur.continue_turns_from(prev)
        cur.play()
        prev = cur
        
    # -- regroup (~9 beats) --
    p1_len = sum(sum(clump) for clump in p1.durs)
    regroup_reps = round(9 / p1_len)
    p1.continue_turns_from(prev)
    
    for rep in range(regroup_reps):
        progress = rep / (regroup_reps - 1)
        p1.hocket = 1 - progress # linear progress
        # p1.hocket = 1 - progress**2 # curve progress
        p1.play()
        
        
    # -- Ending: tutti to hocket to wood solo --
    ending_reps = int((tail_end - s.beat()) // p1_len)
    leaving_order = random.sample(["skin", "metal"], 2)
    exit_points = [ending_reps // 3, 2 * ending_reps // 3]
    
    for rep in range(ending_reps):
        if rep in exit_points:
            p1.instruments.remove(leaving_order.pop(0))
            p1.player_queue = []
            
        progress = rep / max(1, ending_reps - 1)
        p1.hocket = progress
        # p1.hocket = progress ** 2 # stays near tutti longer, then fades out
        p1.play()
    
    wait(tail_end - s.beat())