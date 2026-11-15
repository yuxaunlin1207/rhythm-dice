"""
Develop a single pattern into a section of music.

A section has three parts:

    OPENING   ~10-15%   1-3 players state the pattern in unison
    MIDDLE    the rest  a string of short phrases, each with a random variant,
                        random players, and a random texture:
                          unison | canon | independent | call and response
    CLOSING   ~25-35%   everyone plays while a "hocket dial" gradually splits
                        the pattern between them; ends exactly on the section end

Read top-down: develop_pattern() -> the three parts -> the textures -> helpers.
"""

from prototypes import get_pattern
from copy import deepcopy
from itertools import accumulate
from scamp import *
from playback_setup import *
import random


# ---------------------------------------------------------------------------
#  Odds for the middle section (relative weights)
# ---------------------------------------------------------------------------

PLAYER_COUNT_WEIGHTS = {1: 2, 2: 3, 3: 1}

TEXTURE_WEIGHTS = {            # only used when there are 2+ players
    "unison": 1,
    "independent": 2,
    "canon": 3,
    "call_and_response": 3,
}


# ===========================================================================
#  The section
# ===========================================================================

def develop_pattern(pattern, length=40):
    """
    Play a `length`-beat section built from `pattern`:
        opening (unison)  ->  middle (varied phrases)  ->  closing (hocket build-up)
    Returns the last variant played, so the next section can pick up from it.
    """
    print(s.beat())
    section_end = s.beat() + length
    pattern_len = pattern_length(pattern)

    # The closing is anchored to the END of the section, so plan it first:
    # it lasts a whole number of reps and finishes exactly at section_end.
    closing_reps = plan_closing_reps(pattern_len, length)
    closing_start = section_end - closing_reps * pattern_len

    play_opening(pattern, length)
    play_middle(pattern, closing_start)           # the middle fills the gap
    last_variant = play_closing(pattern, closing_reps)

    wait(beats_until(section_end))
    print(s.beat())
    return last_variant


# ===========================================================================
#  The three parts
# ===========================================================================

def play_opening(pattern, section_length):
    """1-3 random players play the pattern in unison for ~10-15% of the section (2+ reps)."""
    pattern.instruments = random.sample(categories, random.randint(1, 3))
    opening_len = random.randint(10, 15) * .01 * section_length
    reps = max(2, round(opening_len / pattern_length(pattern)))
    print(pattern.instruments, reps)
    repeat(pattern, reps)


def play_middle(pattern, end_beat):
    """
    The middle: keep playing short phrases until there's no room for another full
    pattern before `end_beat`, then rest until `end_beat`.
    Each phrase = a random variant, 1-3 random players, and a texture.
    """
    pattern_len = pattern_length(pattern)

    while fits_before(pattern_len, end_beat):
        # --- pick the ingredients of this phrase ---
        num_players = weighted_choice(PLAYER_COUNT_WEIGHTS)
        reps = choose_phrase_reps(pattern_len, beats_until(end_beat))
        spare_beats = beats_until(end_beat) - reps * pattern_len  # room for staggered entries

        variant = pattern.random_variant()
        variant.instruments = random.sample(categories, num_players)
        texture = choose_texture(num_players)

        # --- play it ---
        if texture == "unison":
            play_unison(variant, reps)
        elif texture == "independent":
            play_independent(pattern, variant.instruments, reps, spare_beats)
        elif texture == "canon":
            play_canon(variant, reps, spare_beats)
        elif texture == "call_and_response":
            play_call_and_response(variant, reps)

    wait(beats_until(end_beat))  # rest through leftover time too short for a full pattern


def play_closing(pattern, closing_reps):
    """
    Everyone plays. The hocket dial ramps from 0 to 1 over the first 75% of the
    closing, splitting the pattern between players. Every ~6 beats (never on the
    first rep) a new variant takes over, continuing the players' turn order.
    """
    pattern.instruments = categories.copy()
    ramp_reps = 0.75 * closing_reps
    reps_per_variant = max(1, round(6 / pattern_length(pattern)))

    current = pattern
    for rep in range(closing_reps):
        if rep > 0 and rep % reps_per_variant == 0:
            new_variant = pattern.random_variant()
            new_variant.continue_turns_from(current)
            current = new_variant

        current.hocket = min(1, rep / ramp_reps)
        current.play()

    return current


# ===========================================================================
#  Textures for the middle section
# ===========================================================================

def play_unison(variant, reps):
    """All players play the same variant together."""
    repeat(variant, reps)


def play_independent(pattern, players, reps, spare_beats):
    """
    Each player plays its own random variant of the pattern. The first enters on
    time; the others enter 0-1 beat late (16th-note grid), squeezed if needed so
    everyone still finishes before the middle ends.
    """
    offsets = [0] + [random.randint(0, 4) / 4 for _ in players[1:]]
    offsets = shrink_to_fit(offsets, span=max(offsets), room=spare_beats, step=0.25)

    for player, offset in zip(players, offsets):
        voice = with_player(pattern.random_variant(), player)
        fork_voice(voice, entry_delay=offset, reps=reps)
    wait_for_children_to_finish()


def play_canon(variant, reps, spare_beats):
    """
    Players enter one after another, 1-4 beats apart (half-beat steps); "skin"
    leads if it's playing. Followers imitate loosely. Entry gaps are squeezed
    if needed so the last voice still finishes before the middle ends.
    """
    players = move_to_front(variant.instruments, "skin")

    gaps = [random.randint(2, 8) / 2 for _ in players[1:]]
    gaps = shrink_to_fit(gaps, span=sum(gaps), room=spare_beats, step=0.5)
    entry_times = accumulate([0] + gaps)

    for i, (player, entry) in enumerate(zip(players, entry_times)):
        voice = with_player(deepcopy(variant), player)
        is_follower = i > 0
        if is_follower:
            make_loose_imitation(voice)
        fork_voice(voice, entry_delay=entry, reps=reps)

    wait_for_children_to_finish()  # the phrase ends when the last voice finishes


def play_call_and_response(variant, reps):
    """
    One player calls; the others answer while the caller softly echoes the call.
    Each exchange takes two reps: [loud call] then [responses + soft call].
    An odd leftover rep gets a final call with no response.
    """
    caller = random.choice(variant.instruments)
    responders = [p for p in variant.instruments if p != caller]

    loud_call = with_player(deepcopy(variant), caller)
    soft_call = deepcopy(loud_call)
    soft_call.volume = 0.3

    responses = [with_player(make_response(loud_call), p) for p in responders]

    for _ in range(reps // 2):
        loud_call.play()
        for response in responses:
            fork_voice(response)          # responses play once, loud...
        soft_call.play()                  # ...over a soft echo of the call
        wait_for_children_to_finish()

    if reps % 2 == 1:
        loud_call.play()


def make_response(call):
    """
    A responder's answer to the call:
        25%  a transformed version of the call
        25%  a transformed version, loosely imitated
        50%  the call itself, loosely imitated
    """
    roll = random.random()
    if roll < 0.25:
        return call.random_variant()    # random_variant() returns a transformed copy

    if roll < 0.5:
        response = call.random_variant()
    else:
        response = deepcopy(call)
    make_loose_imitation(response)
    return response


def make_loose_imitation(voice):
    """
    Roughen an imitating voice: skip one random note, and add 0-2 grace notes
    (only on notes a 16th or longer, and not on the skipped note).
    """
    durs = [d for clump in voice.durs for d in clump]  # one duration per note
    n = len(durs)

    skipped = random.randint(0, n - 1)
    voice.skipped_indices = [skipped]

    decoratable = [i for i in range(n) if durs[i] >= 1/4 and i != skipped]
    num_grace_notes = min(random.randint(0, 2), len(decoratable))
    voice.grace_indices = random.sample(decoratable, num_grace_notes)


# ===========================================================================
#  Planning decisions
# ===========================================================================

def plan_closing_reps(pattern_len, section_length):
    """The closing lasts ~25-35% of the section, rounded to whole reps (at least 2)."""
    closing_len = random.uniform(0.25, 0.35) * section_length
    return max(2, round(closing_len / pattern_len))


def choose_phrase_reps(pattern_len, beats_left):
    """Aim for a 3-6 beat phrase (at least 2 reps), but never more reps than fit."""
    target_reps = max(2, round(random.uniform(3, 6) / pattern_len))
    reps_that_fit = beats_left // pattern_len
    return int(min(target_reps, reps_that_fit))


def choose_texture(num_players):
    """A single player can only play in unison; otherwise pick a weighted-random texture."""
    if num_players == 1:
        return "unison"
    return weighted_choice(TEXTURE_WEIGHTS)


def shrink_to_fit(gaps, span, room, step):
    """
    If staggered entries `span` more beats than there's `room` for, scale all the
    gaps down proportionally, rounding down to a grid of `step` beats.
    """
    if span <= room:
        return gaps
    scale = room / span
    return [round_down_to(gap * scale, step) for gap in gaps]


# ===========================================================================
#  Small helpers
# ===========================================================================

def pattern_length(pattern):
    """Total length of a pattern in beats."""
    return sum(sum(clump) for clump in pattern.durs)


def beats_until(time):
    return time - s.beat()


def fits_before(num_beats, deadline):
    """Is there room to play `num_beats` more beats before `deadline`?"""
    return s.beat() + num_beats <= deadline


def repeat(pattern, reps):
    for _ in range(reps):
        pattern.play()


def play_voice(voice, entry_delay, reps):
    """Wait until it's this voice's turn, then play it `reps` times."""
    wait(entry_delay)
    repeat(voice, reps)


def fork_voice(voice, entry_delay=0, reps=1):
    """Start a voice playing in parallel (see play_voice)."""
    fork(play_voice, args=(voice, entry_delay, reps))


def with_player(voice, player):
    """Assign a single player to a voice, and return the voice."""
    voice.instruments = [player]
    return voice


def move_to_front(items, item):
    """Copy of `items` with `item` moved to the front (if present)."""
    items = items.copy()
    if item in items:
        items.remove(item)
        items.insert(0, item)
    return items


def weighted_choice(weights):
    """Pick a key from a {option: weight} dict."""
    return random.choices(list(weights), weights=list(weights.values()))[0]


def round_down_to(n, step):
    return int(n / step) * step