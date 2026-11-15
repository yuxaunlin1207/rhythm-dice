# Phone Percussion — Movement II

**Rhythm Dice, for percussion trio — Yuxuan Lin**

Late in Movement II, the three players take their phones out of their pockets and begin to "type." Each key plays a short percussive sound from the phone's own speaker the moment a finger touches it. This README covers everything you need to set up the phones and perform that section.

**The surprise is the most important part.** The audience must not see any phones, cables, speakers, or screens until the moment written in the score.

---

## What you need

- **3 iPhones**, one per player, running iOS 17 or newer. Each player uses their own phone.
- **A computer** for the one-time setup (Part 1 only).
- **About 30 minutes** for the first setup. After that, each rehearsal needs about 2 minutes of prep.

No speakers, cables, or sound system are needed. The sound comes from the phones.

---

## Part 1 — Put the app online (do this once)

The app is a small website. Each phone downloads it once and keeps a copy, so after that it works with no internet.

> **Shortcut:** if the composer's link below still works, skip to Part 2.
> Composer's link: `https://yuxaunlin1207.github.io/rhythm-dice/performance-app/`

Otherwise, host your own free copy with GitHub Pages:

1. Go to **github.com** and create a free account (or sign in).
2. Click **+** (top right) → **New repository**.
3. Name it `phone-percussion`, choose **Public**, and click **Create repository**.
4. On the next page, click **uploading an existing file**.
5. Open the `phone-percussion` folder on your computer. Select **everything inside it**:
   - `index.html`, `config.js`, `sketch.js`, `sw.js`, `manifest.json`, `README.md`
   - the folders `lib`, `icons`, and `sounds`

   Drag them all into the upload box.

   ⚠️ Drag the files *inside* the folder, not the folder itself. `index.html` must sit at the top level of the repository.
6. Click **Commit changes** and wait for the upload to finish.
7. Go to **Settings** → **Pages** (left sidebar).
8. Under **Branch**, choose **main** and **/(root)**, then click **Save**.
9. Wait 1–2 minutes, then refresh the page. Your link appears at the top, something like:
   `https://YOUR-USERNAME.github.io/phone-percussion/`

Send that link to all three players.

---

## Part 2 — Install the app on each phone (do this once)

Each player does this on their own phone, connected to Wi-Fi:

1. Open the link in **Safari**. It must be Safari, not Chrome.
2. Tap the **Share** button (a square with an arrow pointing up). On newer iOS, it may be inside the **•••** menu.
3. Scroll down and tap **Add to Home Screen** → **Add**.
4. Close Safari. Open the new **Phone Perc** icon on your Home Screen.

   ⚠️ From now on, always open the app from this icon, never from Safari.
5. Tap your part: **Player 1**, **Player 2**, or **Player 3**.
6. You'll see a black screen. Look at the faint text in the bottom-left corner. Wait until it says **offline ✓**. It may take a few seconds.

The phone now remembers your part and works without internet.

---

## Part 3 — Phone setting (do this once)

The app uses its own keyboard, so you don't need to change any iPhone keyboard settings. Only one setting matters:

**Settings → Display & Brightness → Auto-Lock**: set to **Never**. You will lock the phone yourself with the side button.

Set it back after the concert.

---

## Part 4 — Before every rehearsal and the concert

Do this backstage, about 15 minutes before you go on. Tick every box.

- [ ] Battery is above 50%.
- [ ] **Silent mode is OFF.** Use the switch or Action button on the side of the phone. The app normally plays even on silent, but this is a safety net.
- [ ] **Volume is all the way up.**
- [ ] **Do Not Disturb is ON.** Swipe down from the top-right corner → **Focus** → **Do Not Disturb**.
- [ ] Bluetooth is OFF, so the sound can't go to someone's headphones or a car.
- [ ] Open **Phone Perc** from the Home Screen. The black screen should show your part and **offline ✓** at the bottom.
- [ ] **Test it:** hold the black screen until the line fills, let go, tap a few keys, and listen.
- [ ] **Lock the phone** with the side button. This takes it back to the black screen.
- [ ] Put the phone in your pocket, screen facing your leg.

⚠️ **Do not close the app** by swiping it away. Just lock the phone with the side button.

---

## Part 5 — During the performance

When the score tells you to take out your phone:

1. Take the phone out naturally, the way you'd check a message.
2. **Unlock it** with Face ID or Touch ID. You'll see the black screen.
3. **Hold your thumb anywhere** on the screen until the thin line grows fully (under one second), then **let go**.
4. The app's keyboard appears. **Play it like typing.** Each key sounds **the moment your finger touches it**. Lifting your finger makes no sound, so release however feels natural.

| Keys | Sound |
|---|---|
| Top row (Q W E R T Y U I O P) | high click |
| Middle row (A S D F G H J K L) | middle click |
| Bottom row (Z X C V B N M) | low click |
| Space bar | thump |
| Delete (⌫) | snap |
| Return | thump |
| ⇧ (shift) and 123 | small tick |

Your part (Player 1, 2, or 3) has its own set of sounds, so the three phones sound different from each other.

**Tips**
- Hold the phone up and toward the audience when the score allows. Phone speakers are small, and the speaker is on the bottom edge.
- You can press several keys at once, for example with both thumbs. Each one makes its own sound.
- Only the keyboard plays. Touching the black area above it does nothing.
- Nothing is typed on screen, only small fading dots appear. That's normal.
- The keyboard doesn't vibrate like the normal iPhone keyboard. That's expected.

---

## If something goes wrong

| Problem | Fix |
|---|---|
| No sound at all | Turn Silent mode off and turn the volume up. Then lock and unlock the phone and hold the screen again. If there's still no sound, see **Sound check** below. |
| The menu says "Could not load" | Connect to Wi-Fi and open the app again from the Home Screen icon. |
| The app opened the part menu instead of the black screen | Tap your part again. |
| After unlocking, I see the Home Screen, not the app | Tap the **Phone Perc** icon. It returns to your black screen. |
| The keyboard won't appear | Hold longer, until the line is fully drawn, then lift your thumb. |
| Some taps make no sound | Make sure you're touching the keyboard at the bottom of the screen. The black area above it doesn't play. |
| Sound plays from headphones/another device | Turn Bluetooth off. |

### Sound check

Use this if the phone makes no sound but white dots appear when you tap the keys.

1. Tap **change part** at the bottom of the black screen.
2. Open **Sound check** at the bottom of the menu.
3. Tap **Test 1: beep** and **Test 2: sound file**. You should hear a beep and a thump.
4. Check the switch **Play sound in silent mode**. It should be **ON**.
5. If Test 1 makes no sound with the switch ON, turn it **OFF** and try Test 1 again.
   - **If it now beeps,** leave it OFF on this phone. From now on, **this player must check that Silent mode is off before every performance**, because with the switch OFF the phone goes quiet on silent.
   - **If it still makes no sound,** turn the switch back ON and contact the composer.
6. Choose your part again.

The phone remembers this setting.

---

## For composers and technicians

### Changing the sounds

1. Put your sound files (`.wav` or `.mp3`, under one second each) in `sounds/p1`, `sounds/p2`, or `sounds/p3`.
2. Open `config.js` in any text editor. For each player, set which keys play which file. The instructions are at the top of the file. On the phone's keyboard, the ⇧ and 123 keys play the `"other"` sound.
3. Upload the changed files to the same GitHub repository (**Add file → Upload files**).
4. On each phone, while on Wi-Fi: open the app and wait about 10 seconds. It downloads the new files and saves them automatically.

Tips for loud, clear sounds on a phone speaker:
- Normalize each file close to full level.
- Phone speakers can't play deep bass. Sounds above about 200 Hz carry best.
- Trim silence from the start of each file so it plays the instant a key is pressed.

### The "Play sound in silent mode" switch

This switch sets the type of iOS audio the app uses:

| Switch | iOS audio type | Behavior |
|---|---|---|
| **ON** (default) | Playback | Plays even when the phone is on silent. Stops other apps' audio. |
| **OFF** | Ambient | Muted when the phone is on silent. Mixes with other apps' audio. |

ON is recommended for performance, so a phone switched to silent by accident still sounds. OFF exists as a fallback for a phone that stays silent with ON. The setting is saved on each phone separately.

### Testing on a computer

From the project folder, run `python3 -m http.server 8000` and open `http://localhost:8000` in a browser. Choose a part, click and hold the black screen, release, then click the on-screen keys or type on your computer keyboard. Like on the phone, sounds play on press.

### Files

| File | What it does |
|---|---|
| `config.js` | **Sounds and key mapping. The only file you normally edit.** |
| `index.html` | The page and its layout |
| `sketch.js` | The program: loads sounds, draws the on-screen keyboard, plays a sound on each key press, draws visuals (p5.js) |
| `sw.js` | Saves all files on the phone for offline use |
| `manifest.json` | Makes the Home Screen icon open full-screen |
| `lib/p5.min.js` | The p5.js library (v1.11), stored locally so nothing loads from the internet |
| `sounds/` | Sound files for each player |
| `icons/` | Home Screen icons |
