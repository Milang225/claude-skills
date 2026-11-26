// Rend le calque d'animation image par image avec Chrome headless (protocole DevTools, sans dépendance).
// Usage : node render.mjs <config.json> <dossier_sortie> [liste_de_temps_en_secondes]
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";

const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const [, , cfgPath, outDir, onlyTimes] = process.argv;
const cfg = JSON.parse(fs.readFileSync(cfgPath, "utf8"));
const html = "file://" + path.resolve(path.dirname(new URL(import.meta.url).pathname), cfg.html || "scene.html");
const PORT = 9300 + Math.floor(Math.random() * 500);
const PAGES = cfg.workers || 4;
fs.mkdirSync(outDir, { recursive: true });

const profile = fs.mkdtempSync(path.join(os.tmpdir(), "amf-chrome-"));
const chrome = spawn(CHROME, [
  "--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  "--hide-scrollbars", "--mute-audio", "--no-first-run", "--no-default-browser-check",
  "--allow-file-access-from-files", "--force-color-profile=srgb", "about:blank",
], { stdio: "ignore" });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function http(p, method = "GET") {
  for (let i = 0; i < 80; i++) {
    try { const r = await fetch(`http://127.0.0.1:${PORT}${p}`, { method }); return await r.json(); }
    catch { await sleep(150); }
  }
  throw new Error("Chrome ne répond pas");
}

class Page {
  constructor(ws) { this.ws = ws; this.id = 0; this.pending = new Map(); this.events = [];
    ws.onmessage = (m) => { const d = JSON.parse(m.data);
      if (d.id && this.pending.has(d.id)) { const { res, rej } = this.pending.get(d.id); this.pending.delete(d.id);
        d.error ? rej(new Error(JSON.stringify(d.error))) : res(d.result); }
      else if (d.method) this.events.push(d.method); }; }
  send(method, params = {}) { const id = ++this.id;
    return new Promise((res, rej) => { this.pending.set(id, { res, rej }); this.ws.send(JSON.stringify({ id, method, params })); }); }
  async eval(expr) { const r = await this.send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails).slice(0, 800)); return r.result.value; }
}

async function openPage() {
  const t = await http(`/json/new?about:blank`, "PUT");
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
  const p = new Page(ws);
  await p.send("Page.enable");
  await p.send("Emulation.setFocusEmulationEnabled", { enabled: true }).catch(() => {});
  await p.send("Emulation.setDeviceMetricsOverride", { width: cfg.W, height: cfg.H, deviceScaleFactor: cfg.dsf, mobile: false });
  await p.send("Emulation.setDefaultBackgroundColorOverride", { color: { r: 0, g: 0, b: 0, a: 0 } });
  await p.send("Page.navigate", { url: html });
  for (let i = 0; i < 1200 && !p.events.includes("Page.loadEventFired"); i++) await sleep(50);   // machine chargée : jusqu'à 60 s
  console.log("  page prête", p.events.includes("Page.loadEventFired"));
  await p.eval(`init(${JSON.stringify(cfg)})`);
  return p;
}

try {
  const pages = await Promise.all(Array.from({ length: PAGES }, openPage));
  const n = Math.round(cfg.duration * cfg.fps);
  const jobs = onlyTimes ? onlyTimes.split(",").map((s, i) => ({ i, t: +s, name: `test_${String(i).padStart(2, "0")}.png` }))
    : Array.from({ length: n }, (_, i) => ({ i, t: i / cfg.fps, name: `${String(i).padStart(5, "0")}.png` }));
  let next = 0, done = 0;
  const t0 = Date.now();
  const withTimeout = (pr, ms) => Promise.race([pr, new Promise((_, rej) => setTimeout(() => rej(new Error("délai dépassé")), ms))]);
  async function renderOne(slot, j) {
    for (let essai = 1; essai <= 2; essai++) {
      try {
        await withTimeout(pages[slot].eval(`renderAt(${j.t})`), 20000);
        const shot = await withTimeout(pages[slot].send("Page.captureScreenshot", { format: "png", fromSurface: true }), 30000);
        fs.writeFileSync(path.join(outDir, j.name + ".tmp"), Buffer.from(shot.data, "base64"));
        fs.renameSync(path.join(outDir, j.name + ".tmp"), path.join(outDir, j.name));
        return;
      } catch (e) {
        console.log(`  image ${j.name} : ${e.message} (essai ${essai}/2) — nouvel onglet`);
        try { pages[slot].ws.close(); } catch {}
        pages[slot] = await openPage();
      }
    }
    failed.push(j);   // rendue plus tard en définition réduite puis agrandie (voir monteur.py)
  }
  const failed = [];
  await Promise.all(pages.map(async (_, slot) => {
    while (next < jobs.length) {
      const j = jobs[next++];
      if (!onlyTimes && fs.existsSync(path.join(outDir, j.name))) { done++; continue; }
      // calque arrière : hors des fenêtres utiles, une image vide suffit
      if (!onlyTimes && cfg.windows && cfg.blank && !cfg.windows.some(([a, b]) => j.t >= a - 0.05 && j.t < b + 0.05)) {
        fs.linkSync(cfg.blank, path.join(outDir, j.name)); done++; continue;
      }
      await renderOne(slot, j);
      if (++done % 100 === 0) console.log(`  animation ${done}/${jobs.length} (${((Date.now() - t0) / done).toFixed(0)} ms/image)`);
    }
  }));
  console.log(`  ${jobs.length} images rendues en ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  if (failed.length) {
    fs.writeFileSync(path.join(outDir, "echecs.json"), JSON.stringify(failed));
    console.log(`  ${failed.length} image(s) trop lourde(s) en pleine définition : ${failed.map((j) => j.name).join(", ")}`);
    process.exitCode = 3;
  }
} finally {
  chrome.kill("SIGKILL");
  await sleep(300);
  try { fs.rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 }); } catch {}
}
