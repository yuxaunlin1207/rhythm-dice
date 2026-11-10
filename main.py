from playback_setup import s, notated_parts
import section1
import section2thru4
import random

NOTATE = True
SKIP_PLAYBACK = False


if NOTATE:
    s.start_transcribing(
        list(notated_parts.values())
    )
if SKIP_PLAYBACK:
    s.fast_forward()
    
random.seed(42)   
# section1.play()
section2thru4.play()
    
if NOTATE:
    performance = s.stop_transcribing()
    score = performance.to_score(time_signature="4/4")
    score.show() 
