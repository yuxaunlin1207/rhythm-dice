from prototypes import get_pattern
from copy import deepcopy
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


# wait until it's this voice's turn, and play this voice reps times
def play_voice(voice, entry_delay, reps):
    wait(entry_delay)
    for _ in range(reps):
        voice.play()
        
# skip one note, add 0-2 grace notes when following the leader in canon        
def make_loose_imitation(voice):
    durs = [d for clump in voice.durs for d in clump] # one duration per note
    n = len(durs)
    
    #skip one random note
    skipped = random.randint(0, n-1)
    voice.skipped_indices = [skipped]
    # only notes that are 16ths or longer can get grace note
    decoratable_notes = [i for i in range(n) if durs[i] >= 1/4 and i != skipped]
    num_of_grace_notes = min(random.randint(0,2), len(decoratable_notes))
    voice.grace_indices = random.sample(decoratable_notes, num_of_grace_notes)
        
def round_down_to(n, step):
    return int(n / step) * step

def play_phrases(pattern, middle_end):
    pattern_len = sum(sum(clump) for clump in pattern.durs)
    
    while s.beat() + pattern_len <= middle_end:
        num_players = random.choice([1, 1, 2, 2, 2, 3]) # 1, 2, or 3 with odds 2:3:1
        phrase_len = random.uniform(3, 6)
        
        # decide how many repetitions on a pattern
        potential_reps = max(2, round(phrase_len / pattern_len))
        reps_that_fit = (middle_end - s.beat()) // pattern_len
        reps = int(min(potential_reps, reps_that_fit))
        
        variant = pattern.random_variant()
        variant.instruments = random.sample(categories, num_players) # num_players play on random instr
        
        # get texture
        if num_players == 1:
            texture = "unison"
        else:
            texture = random.choice(["unison"] + ["canon"] * 3 + ["independent"] * 2) # choose one texture
            
        # play diff textures    
        if texture == "unison":
            for _ in range(reps):
                variant.play()
                
        elif texture == "independent":
            offsets = [0] + [random.randint(0, 4) / 4 for _ in range(num_players - 1)]
            room_before_middle_end = middle_end - s.beat() - pattern_len * reps
            latest_voice = max(offsets)
            if latest_voice > room_before_middle_end:
                scale = room_before_middle_end / latest_voice
                offsets = [round_down_to(offs * scale, 0.25) for offs in offsets]
            for player, offset in zip(variant.instruments, offsets):
                voice = pattern.random_variant()
                voice.instruments = [player]
                fork(play_voice, args=(voice, offset, reps))
            wait_for_children_to_finish()
            
        elif texture == "canon":
            # order the players, skin leads if present
            # if skin is among the players
            # take skin out of the list, then put it back at position 0
            players = variant.instruments.copy()
            if "skin" in players:
                players.remove("skin")
                players.insert(0, "skin")
                
            # roll the gaps between entries: 1-4 beats, half-beat steps
            delays = [random.randint(2, 8) / 2 for _ in range(num_players -1)]
            
            # shrink the canon if it'll run past middle
            room_before_middle_end = middle_end - s.beat() - pattern_len * reps
            total_delay = sum(delays)
            if total_delay > room_before_middle_end:
                scale = room_before_middle_end / total_delay # on what scale to shrink
                delays = [round_down_to(dl * scale, 0.5) for dl in delays]
                                
            # start each voice in its own fork
            entry = 0
            for i, player in enumerate(players):
                voice = deepcopy(variant)
                voice.instruments = [player]
                
                if i > 0:
                    make_loose_imitation(voice)
                    
                fork(play_voice, args=(voice, entry, reps))
                
                if i < len(delays): # stops from reading past delays
                    entry += delays[i]
                    
            # the phrase ends when the last voice finishes
            wait_for_children_to_finish()
            
            
            
        
        
            
    wait(middle_end - s.beat()) # rest when can't fit in one pattern

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
    play_phrases(pattern, closing_start)
    
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
    
    