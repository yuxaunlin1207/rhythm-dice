from playback_setup import s, notated_parts
import opening
from development import develop_pattern
from prototypes import get_pattern
import tail
import random

NOTATE = True
SKIP_PLAYBACK = False


if NOTATE:
    s.start_transcribing(
        list(notated_parts.values())
    )

if SKIP_PLAYBACK:
    s.fast_forward()
    
# random.seed(42)   
# opening.play()
# random.seed(2)
# develop_pattern(get_pattern(1))
# random.seed(2)
# develop_pattern(get_pattern(3))
random.seed(2)
last_variant = develop_pattern(get_pattern(2))
tail.play(last_variant)
    
if NOTATE:
    performance = s.stop_transcribing()
    score = performance.to_score(time_signature="4/4")
    score.show() 
