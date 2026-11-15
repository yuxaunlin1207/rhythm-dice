/* =====================================================================
   PHONE PERCUSSION — SETTINGS
   This is the only file you need to edit to change sounds or keys.
   ===================================================================== */

// How long (in milliseconds) a player must hold the black standby screen
// before the keyboard appears. Stops sounds from starting by accident.
const HOLD_TO_START_MS = 600;

// Show small fading dots above the keyboard when a key is played.
// Set to false for a completely black screen.
const SHOW_VISUALS = true;

/* ---------------------------------------------------------------------
   KEY MAP FOR EACH PLAYER

   On the left, put the keys. On the right, put the sound file.
     "qwertyuiop": "sounds/p1/click-high.wav"
        -> every letter in "qwertyuiop" plays that sound.
     "a": "sounds/p1/thump.wav"
        -> only the "a" key plays that sound.

   To make a key choose randomly from several sounds, use a list:
     "zxcvbnm": ["sounds/p1/low-1.wav", "sounds/p1/low-2.wav"]

   Special key names:
     "space"      the space bar
     "backspace"  the delete key
     "return"     the return key
     "other"      any key not listed (numbers, punctuation, etc.)

   pitchVariation: small random pitch change on each hit, so repeated
                   notes sound less mechanical (0 = off, 0.03 = subtle).
   volume:         loudness of this player's sounds (1.0 = normal).

   Use .wav or .mp3 files. Keep them short (under one second).
   --------------------------------------------------------------------- */
const PLAYERS = {
  1: {
    label: "Player 1",
    keys: {
      "qwertyuiop": "sounds/p1/click-high.wav",
      "asdfghjkl":  "sounds/p1/click-mid.wav",
      "zxcvbnm":    "sounds/p1/click-low.wav",
      "space":      "sounds/p1/thump.wav",
      "backspace":  "sounds/p1/snap.wav",
      "return":     "sounds/p1/thump.wav",
      "other":      "sounds/p1/tick.wav",
    },
    pitchVariation: 0.02,
    volume: 1.0,
  },

  2: {
    label: "Player 2",
    keys: {
      "qwertyuiop": "sounds/p2/click-high.wav",
      "asdfghjkl":  "sounds/p2/click-mid.wav",
      "zxcvbnm":    "sounds/p2/click-low.wav",
      "space":      "sounds/p2/thump.wav",
      "backspace":  "sounds/p2/snap.wav",
      "return":     "sounds/p2/thump.wav",
      "other":      "sounds/p2/tick.wav",
    },
    pitchVariation: 0.02,
    volume: 1.0,
  },

  3: {
    label: "Player 3",
    keys: {
      "qwertyuiop": "sounds/p3/click-high.wav",
      "asdfghjkl":  "sounds/p3/click-mid.wav",
      "zxcvbnm":    "sounds/p3/click-low.wav",
      "space":      "sounds/p3/thump.wav",
      "backspace":  "sounds/p3/snap.wav",
      "return":     "sounds/p3/thump.wav",
      "other":      "sounds/p3/tick.wav",
    },
    pitchVariation: 0.02,
    volume: 1.0,
  },
};

/* ===================== No need to edit below this line ===================== */

const APP_FILES = [
  "./",
  "index.html",
  "config.js",
  "sketch.js",
  "manifest.json",
  "lib/p5.min.js",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "icons/apple-touch-icon.png",
];

// Every file the app needs, including all sound files listed above.
function allAppFiles() {
  const files = new Set(APP_FILES);
  for (const p of Object.values(PLAYERS)) {
    for (const v of Object.values(p.keys)) {
      [].concat(v).forEach((f) => files.add(f));
    }
  }
  return [...files];
}
