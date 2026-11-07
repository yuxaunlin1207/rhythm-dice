from scamp import *

s = Session()
s.tempo = 60

perc_playback = s.new_part("Playback Part", preset="Standard")

notated_parts = {
    "metal": s.new_silent_part("Perc 1"),
    "wood": s.new_silent_part("Perc 2"),
    "skin": s.new_silent_part("Perc 3 ")
}

notated_pitches = [67, 71, 74]

perc_mapping = {
    "skin": [35, 45, 63],
    "wood": [77, 76, 75],
    "metal": [51, 46, 81]
}

categories = ["skin", "wood", "metal"]


def play_hit(instruments: list[str], low_mid_hi: int, volume, 
             duration, properties=None):
    if low_mid_hi is not None:
        for category in instruments:
            notated_pitch = notated_pitches[low_mid_hi]
            notated_part = notated_parts[category]
            notated_part.play_note(notated_pitch, volume, duration,
                                   properties=properties, blocking=False) # play the notated note
            perc_playback.play_note(perc_mapping[category][low_mid_hi],
                                    volume, duration, properties=properties, blocking=False) # play the playback note
            
    wait(duration) # runs for both notes and rests