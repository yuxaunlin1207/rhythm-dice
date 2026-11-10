from copy import deepcopy
from dataclasses import dataclass, field
from playback_setup import play_hit, categories
import random
from scamp import wait


@dataclass
class Pattern:
    pitches: list[list[int]]
    durs: list[list[float]]
    skipped_indices: list[int]
    silent_indices: list[int]
    instruments: list[str] = field(default_factory=lambda: list(categories))
    hocket: float = 0
    player_queue: list[str] = field(default_factory=list)
    last_player: str=None
    

    def play(self):
        n = sum(len(clump) for clump in self.pitches) # total number of notes
        i = 0; # which note we're on across all clumps
        
        for pitch_clump, dur_clump in zip(self.pitches, self.durs):
            if self.hocket:
                # I want num instruments to be between 1 and len(instruments)
                # when hocket = 1, it should be always 1
                # when hocket = 0, it should be always len(instruments)
                # when hocket = 0.5, it should bounce between 1 and 2 and 3, and it should transition gracefully
                total_num_instr = len(self.instruments)
                num_instruments = 1 + sum(random.random() >= self.hocket for _ in range(total_num_instr - 1))
                if num_instruments == total_num_instr:
                    clump_instr = self.instruments
                else:
                    clump_instr = [self.next_player_in_turn(self.instruments) for _ in range(num_instruments)]
            else:
                clump_instr = self.instruments
            
            for pitch, dur in zip(pitch_clump, dur_clump):
                #-6, -5, -4, -3, -2, -1   = i - n (backward counting)
                # 0,  1,  2,  3,  4,  5   =  i (the forward counting index)
                if (i in self.skipped_indices) or (i - n in self.skipped_indices):
                    pass # operation NULL
                elif (i in self.silent_indices) or (i - n in self.silent_indices):
                    wait(dur)
                else:
                    play_hit(clump_instr, pitch, 1, dur)                
                i += 1
                
    # T / F flags for each note
    def note_flags(self, indices):
        n = sum(len(clump) for clump in self.pitches) # num of total notes
        i = 0
        flags = []
        for clump in self.pitches:
            clump_flags = []
            for _ in clump:
                flag = (i in indices) or (i - n in indices)
                clump_flags.append(flag)
                i += 1
            flags.append(clump_flags)
        return flags
    
    def flags_to_indices(self, flags):
        indices = []
        i = 0
        for clump in flags:
            for flag in clump:
                if flag:
                    indices.append(i)
                i += 1
        return indices

    #invert first and then shift
    def pitch_shift(self, amount, invert=False):
        if invert:
            self.pitches = [[2 - p for p in clump] for clump in self.pitches] # invert line
        self.pitches = [[(p + amount) % 3 for p in clump] for clump in self.pitches] # shift line

    # rotate pattern with on/off retrograde
    def rotate(self, amount, retrograde=False):
        silent = self.note_flags(self.silent_indices) # T/F flags 
        # print(silent)
        skip_idx = self.note_flags(self.skipped_indices) # T/F flags
            
        if retrograde: 
            self.pitches = [clump[::-1] for clump in self.pitches[::-1]]
            self.durs = [clump[::-1] for clump in self.durs[::-1]] # retrograde in clumps
            silent = [clump[::-1] for clump in silent[::-1]] 
            skip_idx = [clump[::-1] for clump in skip_idx[::-1]]

        wrapped_amt = amount % len(self.pitches)
        self.pitches = self.pitches[wrapped_amt:] + self.pitches[:wrapped_amt]
        self.durs = self.durs[wrapped_amt:] + self.durs[:wrapped_amt]
        
        silent = silent[wrapped_amt:] + silent[:wrapped_amt]
        self.silent_indices = self.flags_to_indices(silent) # turn T/F flags back to numbers
        
        skip_idx = skip_idx[wrapped_amt:] + skip_idx[:wrapped_amt]
        self.skipped_indices = self.flags_to_indices(skip_idx) # turn T/F flags back to numbers
    
    # a random rotate with 50% retro or invert and skipping a note, shift 0-2 levels
    def random_variant(self):
        variant = deepcopy(self)
        variant.rotate(random.randint(0, len(variant.pitches)-1),
                       retrograde=random.random() < 0.5)
        variant.pitch_shift(random.choice([0 , 1, 2]),
                            invert=random.random() < 0.5)
        
        if random.random() < 0.5:
            n = sum(len(clump) for clump in self.pitches) # count notes
            variant.silent_indices = [random.randint(0, n-1)]
            
        return variant
        
    # hand back a new player for every hocketed clump inside play(), make sure no repeat
    def next_player_in_turn(self, pool):
        if len(self.player_queue) == 0:
            self.player_queue = random.sample(pool, len(pool))
            # keep trying until getting a diff player
            while self.player_queue[0] == self.last_player and len(self.player_queue)>1: 
                self.player_queue = random.sample(pool, len(pool))
        self.last_player = self.player_queue.pop(0)
        return self.last_player
    
    # plays the pattern forever and each repetition goes to the next player
#     def for_pattern_rotate_instr(self):
#         instr_pool = self.instruments.copy()
#         while True:
#             self.instruments = [self.next_player_in_turn(instr_pool)]
#             print(self.instruments)
#             self.play()

    # continue the player turn-taking from the prev pattern 
    def continue_turns_from(self, prev):
        self.player_queue = prev.player_queue
        self.last_player = prev.last_player
        
