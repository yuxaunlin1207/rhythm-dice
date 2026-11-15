# Time Stretch

**for percussion trio** · Yuxuan Lin · 2026

This piece is a work in progress for percussion trio that will consist of three movements. It explores the idea of creating a gradual crossfade between music composed entirely by hand and music generated solely by a computer under human guidance. The work seeks to investigate how traditional compositional techniques, computer-assisted algorithmic composition, and computer-driven composition produce different musical results when given exactly the same raw motifs and instrumental constraints as starting points for development.

**Duration:** ca. 15 minutes · **Movements:** I. One Notch at a Time    II. Rhythm Dice    III. Title TBA

This repository holds the two technical parts of the piece:

| Folder | What it is | Who it's for |
|---|---|---|
| [`score/`](score/) | Python code that generated the raw material and structure of the score | Anyone curious about how the piece was made |
| [`performance-app/`](performance-app/) | A phone app the three players use in Movement II | Performers and technicians |

---

## For performers

Movement II needs **three iPhones**, one per player, running a small offline web app. You don't need a sound system, speakers, or cables.

- **App link:** https://yuxaunlin1207.github.io/rhythm-dice/performance-app/
- **Step-by-step setup:** [`performance-app/README.md`](performance-app/README.md)

Allow about 30 minutes for the first setup and 2 minutes before each rehearsal.

> **Please keep the phones a surprise.** The phone section works only if the audience doesn't expect it. Don't mention phones or electronics in program notes, posters, or stage announcements, and keep phones out of sight until the moment marked in the score.

**Score and parts:** available from the composer. Please contact: linyuxuan127@gmail.com or fill in the contact form at https://yuxuanlin.com/

---

## How the score was made

The code in [`score/`](score/) is a generative system written in Python with [SCAMP](http://scamp.marcevanstein.com/). Each run is driven by a random **seed**, and produces both the raw musical material and an overall structure for the piece.

The code does not write the finished score by itself. I ran it with many seeds, kept the ones that gave the most promising results, and then sliced and combined material from those runs by hand. The final score loosely follows the structure the code designed, and keeps the material that is most interesting to play.

### Files

| File | What it does |
|---|---|
| `development.py` | develops each pattern into its unique section |
| `main.py` | runs the entire piece from beginning to end |
| `opening.py` | runs the hardcoded beginning of the movement |
| `pattern.py` | a collections of patterns, i.e. motifs of the piece |
| `playback_setup.py` | maps the pitches and sets up the score |
| `prototypes.py` | a collection of methods that prototypes developmental ideas |
| `tail.py` | ending of the piece |

### Running it

You need Python 3.12 and SCAMP:

```
pip install scamp
```

Then, from the `score/` folder:

```
python main.py
```

### Seeds used in the piece

These seeds produced the material used in the final score:

| Seed | Used for |
|---|---|
| `random.seed(3)` | Movement II, opening section |
| `random.seed(72)` | Movement II, pattern 1 development |
| `random.seed(30)` | Movement II, pattern 3 development |
| `random.seed(2)` | Movement II, pattern 2 development and movement ending |

---

## License

The code in this repository (`score/` and `performance-app/`) is released
under the MIT License. You're free to use, host, and adapt it.

The musical work *Time Stretch*, including the score, parts, and recordings,
is © 2026 Yuxuan Lin(ASCAP). All rights reserved. For performance materials or
permission requests, please fill out the contact form in https://yuxuanlin.com/.

## Contact

Yuxuan Lin: https://yuxuanlin.com/ Contact form included in website.
