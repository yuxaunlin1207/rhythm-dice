/* Service worker: saves every file on the phone so the app works offline.
   Strategy: try the network first (so updates arrive when online), and fall
   back to the saved copy instantly when offline. No need to edit this file. */

importScripts("config.js");

const CACHE = "phone-percussion";
const NETWORK_TIMEOUT_MS = 2000;

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) =>
      Promise.all(
        allAppFiles().map((f) =>
          cache.add(new Request(f, { cache: "reload" })).catch(() => {})
        )
      )
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

function withTimeout(promise, ms) {
  return new Promise((resolve, reject) => {
    const t = setTimeout(() => reject(new Error("timeout")), ms);
    promise.then((v) => { clearTimeout(t); resolve(v); },
                 (e) => { clearTimeout(t); reject(e); });
  });
}

async function networkFirst(request) {
  const cache = await caches.open(CACHE);
  try {
    const response = await withTimeout(fetch(request, { cache: "no-store" }), NETWORK_TIMEOUT_MS);
    if (response && response.ok) cache.put(request, response.clone());
    return response;
  } catch (err) {
    const saved = await cache.match(request, { ignoreSearch: true });
    if (saved) return saved;
    throw err;
  }
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;
  event.respondWith(networkFirst(req));
});
