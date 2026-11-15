/* Phone Percussion — main program.
   Normally you don't need to edit this file. Change sounds and keys in config.js.

   How it works:
   1. Sounds are loaded and decoded into memory when the app opens.
   2. The player picks a part (saved on the phone), then sees a black standby screen.
   3. Holding the standby screen unlocks audio and opens the iPhone keyboard.
   4. Each key typed into a hidden text box plays the sound mapped to it.
   5. Locking the phone or leaving the app returns to standby.

   Sound uses the Web Audio API directly (lowest latency, any number of
   overlapping hits). p5.js draws the screen. */

// ---------------------------------------------------------------- audio setup
// "Play sound in silent mode" setting (Sound check screen).
//   ON  -> iOS "playback" audio: plays even when the phone is on silent (recommended).
//   OFF -> iOS "ambient" audio:  muted when the phone is on silent.
// Turn it OFF only if a phone makes no sound with it ON.
let playInSilent = localStorage.getItem("phonePercussionPlayInSilent") !== "off";
function applyAudioMode() {
  try { if (navigator.audioSession) navigator.audioSession.type = playInSilent ? "playback" : "ambient"; } catch (e) {}
}
applyAudioMode();

const AudioCtx = window.AudioContext || window.webkitAudioContext;
let ctx, limiter;

function makeContext() {
  ctx = new AudioCtx({ latencyHint: "interactive" });
  // Gentle limiter so many overlapping hits don't distort.
  limiter = ctx.createDynamicsCompressor();
  limiter.threshold.value = -1;
  limiter.knee.value = 0;
  limiter.ratio.value = 20;
  limiter.attack.value = 0.001;
  limiter.release.value = 0.05;
  limiter.connect(ctx.destination);
}
makeContext();

// A tiny silent sound played through a normal <audio> element during a touch.
// On iPhone this switches the phone into "media playback", which web audio needs.
function makeSilentWavURL() {
  const n = 4410, buf = new ArrayBuffer(44 + n * 2), v = new DataView(buf);
  const w = (o, s) => [...s].forEach((c, i) => v.setUint8(o + i, c.charCodeAt(0)));
  w(0, "RIFF"); v.setUint32(4, 36 + n * 2, true); w(8, "WAVE"); w(12, "fmt ");
  v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true);
  v.setUint32(24, 44100, true); v.setUint32(28, 88200, true); v.setUint16(32, 2, true);
  v.setUint16(34, 16, true); w(36, "data"); v.setUint32(40, n * 2, true);
  return URL.createObjectURL(new Blob([buf], { type: "audio/wav" }));
}
const unlockEl = new Audio(makeSilentWavURL());
unlockEl.setAttribute("playsinline", "");

const buffers = new Map(); // file path -> decoded audio
let player = null;         // the chosen part from PLAYERS
let keymap = {};           // single key -> list of sound files
let mode = "setup";        // "setup" | "standby" | "live"
let hits = [];             // for visuals
let offlineReady = false;

function updateInfo() {
  document.getElementById("standbyInfo").textContent =
    (player ? player.label : "") + (offlineReady ? "  ·  offline ✓" : "  ·  not saved offline yet");
}

const SPECIAL = ["space", "backspace", "return", "other"];
const SENTINEL = "        "; // the hidden text box always holds these spaces so backspace always works

// ---------------------------------------------------------------- elements
const $ = (id) => document.getElementById(id);
const keysEl = $("keys");
const standbyEl = $("standby");
const setupEl = $("setup");
const holdArea = $("holdArea");
document.documentElement.style.setProperty("--hold", HOLD_TO_START_MS + "ms");

// ---------------------------------------------------------------- loading
function buildKeymap(cfg) {
  const m = {};
  for (const [k, v] of Object.entries(cfg.keys)) {
    const files = [].concat(v);
    if (SPECIAL.includes(k)) m[k] = files;
    else for (const ch of k.toLowerCase()) m[ch] = files;
  }
  return m;
}

async function loadSound(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(url);
  const data = await res.arrayBuffer();
  return await ctx.decodeAudioData(data);
}

async function loadPlayer(id) {
  player = PLAYERS[id];
  keymap = buildKeymap(player);
  localStorage.setItem("phonePercussionPlayer", id);

  const files = [...new Set(Object.values(keymap).flat())].filter((f) => !buffers.has(f));
  setText("loadStatus", "Loading sounds…");
  const results = await Promise.allSettled(files.map(async (f) => buffers.set(f, await loadSound(f))));
  const missing = files.filter((f, i) => results[i].status === "rejected");

  if (missing.length) {
    setText("loadStatus", "Could not load: " + missing.join(", "), "bad");
    return false;
  }
  setText("loadStatus", "");
  updateInfo();
  return true;
}

// ---------------------------------------------------------------- playing
function hit(name) {
  const files = keymap[name] || keymap.other;
  if (!files || !files.length) return;
  const buf = buffers.get(files[Math.floor(Math.random() * files.length)]);
  if (!buf) return;
  if (ctx.state !== "running") ctx.resume();

  const src = ctx.createBufferSource();
  src.buffer = buf;
  const v = player.pitchVariation || 0;
  src.playbackRate.value = 1 + (Math.random() * 2 - 1) * v;

  const gain = ctx.createGain();
  gain.gain.value = player.volume ?? 1;
  src.connect(gain);
  gain.connect(limiter);
  src.start();

  hits.push({ x: Math.random(), y: Math.random(), t: performance.now() });
}

function resetField() {
  keysEl.value = SENTINEL;
  keysEl.setSelectionRange(SENTINEL.length, SENTINEL.length);
}

keysEl.addEventListener("input", (e) => {
  if (mode !== "live") { resetField(); return; }
  const type = e.inputType || "";
  if (type.startsWith("delete")) hit("backspace");
  else if (type === "insertLineBreak" || type === "insertParagraph") hit("return");
  else if (type === "insertText" && e.data) {
    for (const ch of e.data.slice(0, 4)) hit(ch === " " ? "space" : ch.toLowerCase());
  }
  // Autocorrect replacements and other edits are ignored on purpose.
  resetField();
});

// ---------------------------------------------------------------- modes
let wakeLock = null;

// Must be called during a touch. Wakes the phone's audio in every known way.
function unlockAudio() {
  if (ctx.state === "closed") makeContext();
  try { unlockEl.currentTime = 0; unlockEl.play().catch(() => {}); } catch (e) {}
  ctx.resume().then(updateDiag, updateDiag);
  const b = ctx.createBuffer(1, 1, ctx.sampleRate);
  const s = ctx.createBufferSource();
  s.buffer = b; s.connect(ctx.destination); s.start();
}

function goLive() {
  unlockAudio();
  mode = "live";
  standbyEl.classList.add("hidden");
  resetField();
  keysEl.focus(); // must happen during the touch, or iOS won't show the keyboard
  try { navigator.wakeLock?.request("screen").then((l) => (wakeLock = l)).catch(() => {}); } catch (e) {}
}

function goStandby() {
  mode = "standby";
  keysEl.blur();
  setupEl.classList.add("hidden");
  standbyEl.classList.remove("hidden");
  try { wakeLock?.release(); } catch (e) {}
  wakeLock = null;
}

function goSetup() {
  mode = "setup";
  keysEl.blur();
  localStorage.removeItem("phonePercussionPlayer");
  standbyEl.classList.add("hidden");
  setupEl.classList.remove("hidden");
}

document.addEventListener("visibilitychange", () => {
  if (document.hidden && mode === "live") goStandby();
});
window.addEventListener("pagehide", () => { if (mode === "live") goStandby(); });

// ---------------------------------------------------------------- hold to start
let pressStart = null;
function onPressStart(e) {
  e.preventDefault();
  pressStart = performance.now();
  standbyEl.classList.add("holding");
}
function onPressEnd(e) {
  e.preventDefault();
  standbyEl.classList.remove("holding");
  const held = pressStart !== null && performance.now() - pressStart >= HOLD_TO_START_MS;
  pressStart = null;
  if (held) goLive();
}
function onPressCancel() { pressStart = null; standbyEl.classList.remove("holding"); }

holdArea.addEventListener("touchstart", onPressStart, { passive: false });
holdArea.addEventListener("touchend", onPressEnd, { passive: false });
holdArea.addEventListener("touchcancel", onPressCancel);
holdArea.addEventListener("mousedown", onPressStart); // for testing on a computer
holdArea.addEventListener("mouseup", onPressEnd);
holdArea.addEventListener("mouseleave", onPressCancel);
$("changePlayer").addEventListener("click", goSetup);

// ---------------------------------------------------------------- setup screen
function setText(id, text, cls) {
  const el = $(id);
  el.textContent = text;
  el.classList.remove("good", "bad");
  if (cls) el.classList.add(cls);
}

for (const [id, cfg] of Object.entries(PLAYERS)) {
  const b = document.createElement("button");
  b.textContent = cfg.label;
  b.addEventListener("click", async () => {
    unlockAudio();
    if (await loadPlayer(id)) goStandby();
  });
  $("playerButtons").appendChild(b);
}

// ---------------------------------------------------------------- sound check
function updateDiag() {
  $("silentToggle").checked = playInSilent;
  $("silentState").textContent = playInSilent ? "ON (recommended)" : "OFF";
  const silentText = !navigator.audioSession ? "silent-mode setting not supported here"
    : playInSilent ? "plays in silent mode ✓" : "muted in silent mode ⚠︎";
  const ios = navigator.audioSession ? ` (iOS: ${navigator.audioSession.type})` : "";
  setText("diag", `Audio: ${ctx.state} · ${silentText}${ios}`,
          ctx.state === "running" ? "good" : "bad");
}

// Test 1: a beep made by web audio (the engine the app uses).
$("beepBtn").addEventListener("click", () => {
  unlockAudio();
  const osc = ctx.createOscillator(), g = ctx.createGain();
  osc.frequency.value = 880;
  g.gain.setValueAtTime(0.5, ctx.currentTime);
  g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
  osc.connect(g); g.connect(ctx.destination);
  osc.start(); osc.stop(ctx.currentTime + 0.4);
  setTimeout(updateDiag, 200);
});

// Test 2: one of the sound files through a plain <audio> element (no web audio).
$("fileBtn").addEventListener("click", () => {
  const first = [].concat(Object.values(PLAYERS)[0].keys.space)[0];
  const a = new Audio(first);
  a.setAttribute("playsinline", "");
  a.play().catch((e) => setText("diag", "Plain audio failed: " + e.message, "bad"));
});

// "Play sound in silent mode" toggle: change the iOS audio type and rebuild the audio engine.
$("silentToggle").addEventListener("change", () => {
  playInSilent = $("silentToggle").checked;
  localStorage.setItem("phonePercussionPlayInSilent", playInSilent ? "on" : "off");
  applyAudioMode();
  try { ctx.close(); } catch (e) {}
  makeContext();
  unlockAudio();
  setTimeout(updateDiag, 200);
});
updateDiag();

// ---------------------------------------------------------------- offline
async function checkOffline() {
  if (!("serviceWorker" in navigator) || !window.caches) {
    setText("offlineStatus", "Offline saving isn't available here. Open the app from the Home Screen icon over https.", "bad");
    return;
  }
  try {
    await navigator.serviceWorker.ready;
    const files = allAppFiles();
    let saved = 0;
    for (const f of files) if (await caches.match(f, { ignoreSearch: true })) saved++;
    if (saved === files.length) {
      setText("offlineStatus", "✓ Saved for offline use", "good");
      offlineReady = true;
      updateInfo();
      return;
    }
    setText("offlineStatus", `Saving for offline use… (${saved}/${files.length})`);
  } catch (e) {
    setText("offlineStatus", "Still saving for offline use…");
  }
  setTimeout(checkOffline, 2000);
}

if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(() => {});
checkOffline();

// If a part was chosen before, go straight to standby.
(async () => {
  const saved = localStorage.getItem("phonePercussionPlayer");
  if (saved && PLAYERS[saved] && (await loadPlayer(saved))) goStandby();
})();

// ---------------------------------------------------------------- visuals (p5.js)
function setup() {
  createCanvas(windowWidth, windowHeight);
  pixelDensity(2);
}

function draw() {
  background(0);
  if (!SHOW_VISUALS || mode !== "live") return;
  const now = performance.now();
  hits = hits.filter((h) => now - h.t < 600);
  noStroke();
  const top = height * 0.45; // stay above the keyboard
  for (const h of hits) {
    const a = 1 - (now - h.t) / 600;
    fill(255, 200 * a);
    circle(24 + h.x * (width - 48), 40 + h.y * (top - 60), 8 + 28 * (1 - a));
  }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}
