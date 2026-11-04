# AGENTS.md — SoR4 Survival Tracker Development Guide

> This file gives future AI coding assistants the project context, conventions, and recurring patterns needed to work efficiently on this codebase without re-discovering them each session.

---

## 1. Project Identity

- **App:** A browser tracker for **Streets of Rage 4** Survival mode runs — co-op head-to-head and solo "deep" runs across the full character roster.
- **Stack:** React 18 + TypeScript + Vite. No backend, no accounts. GitHub Pages hosting.
- **Repo:** `RavenholmTourist/sor4-survival-tracker` (this repo — fresh start).
- **Reference implementation:** `RavenholmTourist/git_game` (public), live at <https://ravenholmtourist.github.io/git_game/>. That repo holds the working two-player version (Thomas vs Craig) plus all imported run data. **Clone/copy from it — do not rebuild from scratch.**
- **Handoff doc:** `SOR4_TRACKER_HANDOFF.md` at repo root is the authoritative spec. Read it first.

---

## 2. The Task

Recreate the tracker in this repo, generalised from the hardcoded two-player version. **Status: ported and generalised.** `git_game`'s code was brought in as the baseline, then refactored.

- **Up to 4 named players** (`Player {id, name, color}` in IDB), each with solo tracking plus shared co-op tracking per ordered player-pairing.
- First-run **onboarding** (`Onboarding.tsx`) creates 1–4 profiles; `SettingsView` manages them afterwards (edit/delete blocked while runs reference a player).
- **Co-op pairing selector** in `CoopView` (ordered A↓ vs B→; picking the already-selected player swaps slots). Solo **player selector** in `SoloView`. Selections persist in localStorage.
- **Community-shareable:** local-first storage, no setup — see §6. **PWA**: `public/manifest.webmanifest` + hand-rolled cache-first `public/sw.js`, icons generated from `logo.png`.

### What reuses vs. what changes

| Area | Reuse | Change needed |
|------|-------|---------------|
| Matrices, forms, scratch cards, fullscreen view, stats deck | ~everything | Player fields become dynamic player ids instead of hardcoded `thomas`/`craig` |
| `CoopRun` | shape | `{ players: [{playerId, char, score}, {playerId, char, score}] }` — still 2 slots per run |
| Matrix model | 21×21 per pairing | Pick which two players' pairing to view; 441-cell logic is unchanged per pairing |
| Storage | swap layer only | See §6 — open decision |
| Onboarding | none in old app | Need "add players, pick names + colours" profile setup |
| Stats | same aggregations | Parameterised by player id; head-to-head becomes per-pairing |

---

## 3. Domain Model (unchanged from reference)

### Roster — 21 characters (`src/characters.ts`)

| Game | Characters |
|------|-----------|
| SoR4 | Axel, Blaze, Cherry, Floyd, Adam, Estel, Max, Shiva |
| SoR1 | Axel, Blaze, Adam |
| SoR2 | Axel, Blaze, Max, Skate |
| SoR3 | Axel, Blaze, Skate, Zan, Shiva, Roo |

- Character id format: `{game}-{name}` (e.g. `sor4-axel`). Portraits live at `public/img/portraits/{id}.png`.
- `hasAltBlitz` is `false` for SoR1 characters only.
- **Portraits (decided):** ship the existing wiki-sourced art for now (free fan tracker, accepted risk), behind a **pluggable portrait system** — lookup order: user-uploaded override → `portraits/{id}.png` → `portraits-duo/{id}.png` → letter tile. Uploads managed in Settings (IDB blobs).
- **Art direction (locked):** final portrait style = full-colour character art, silhouette cutout on transparent bg (Floyd-style), in an invisible square for consistent scaling/positioning. **Game marker = just the numeral 1/2/3/4 bottom-left in the game's colour — NO "SOR" text.** Game colours: SoR1 `#ff6b6b` red, SoR2 `#5ec8ff` blue, SoR3 `#8be36b` green, SoR4 `#ffcc00` yellow (same as `game-tag` CSS vars — keep them in sync).
- **Source art:** `art-src/full/{id}.png` = best full-body art per slot scraped from the SoR wiki (Fandom API + CDN, curl w/ browser headers — urllib gets TLS-fingerprint-blocked, API works w/o auth). SoR4 slots = clean alpha cutouts already. SoR3 = painted art. SoR2 = B&W line art. Weak slots: sor1-adam (bio card w/ text), sor1-axel (52×98 low-res), sor3-shiva (line art) — flag for replacement via ComfyUI or better sources.
- **ComfyUI plan (owner installing):** restyle SoR1/2/3 art into SoR4's illustration style while keeping each character's classic design (img2img/IP-Adapter on `art-src/full/`). `_tmp/` holds scrape intermediates + contact sheets.

### Co-op matrix — 441 cells

- 21×21 ordered pairs (player A rows × player B cols). Same character both sides is legal.
- `CoopRun`: `{ id, loggedAt, players: [CoopSide, CoopSide], level, time }` where `CoopSide = {playerId, char, score}`. `players[0]` = row player, `players[1]` = column player — order matters, a run belongs to exactly one ordered pairing.
- `time` is `mm:ss` or `h:mm:ss`; `loggedAt` is ISO date. Winner = higher score.

### Solo matrix — 78 cells

- 21 characters × 4 move combos (Default/Alternate Blitz × Default/Alternate Star) = 84, minus 6 invalid (3 SoR1 chars × 2 Alt-Blitz combos) = **78**. Invalid cells render "N/A", disabled.
- `SoloRun`: `{ id, loggedAt, playerId, character, blitz, star, level, time, score }`.

### Randomiser

- Picks uniformly from **unlogged** combinations only. Scratch-card reveal flow (tap = instant, drag = canvas `destination-out`, auto-reveal at 45% cleared). Co-op: second player's card locked until first is revealed. Matrix highlight + "Log this run" stay hidden until all cards revealed.

### Stats deck

- Swipeable card deck per view (tab pills, ‹ › arrows, pointer swipe). Recompute panels per selected pairing / player. See handoff §2 for the full panel list.

---

## 4. Coding Conventions

- **TypeScript strict typing everywhere** — params, returns, locals. No `any` without reason.
- Functional components + hooks. `src/lib/` for data layer, feature components at `src/components/`.
- **Existing comments/docs are never deleted or modified unless explicitly asked.**
- Dark theme via CSS vars in `src/index.css`. Player colours are dynamic: `--pa`/`--pb` are set inline on the co-op `<section>` (and `--pa` on solo) from the selected pairing/player, with defaults on `:root`. Use `.pa-text`/`.pb-text`, `.winner-dot.a/.b`, `.score-side.a/.b` — never hardcode a player colour or name.
- Bebas Neue for headings/numbers, Inter for body.
- Modals `z-index: 300`; fullscreen matrix overlay `z-index: 200`. `body.no-scroll` while overlay open.
- `MatrixFrame` fullscreen: pinch zoom via CSS `zoom` + raw touch handlers, ctrl+wheel, drag-scroll, Esc to close. Keep these behaviours.
- Emoji glyphs render as tofu on some systems — prefer text/SVG (🎲 and 🔒 were removed for this reason).

---

## 5. Data Layer (`src/lib/`)

- `db.ts` — IndexedDB `kv` store wrapper (`dbGet`/`dbSet`/`dbDel`), `DB_KEYS` constants, calls `navigator.storage.persist()`. Single store keyed by `runs:coop`, `runs:solo`, `players`, `portraits`.
- `useRunStore.ts` — `{runs, loading, saving, error, reload, setAll, mutate}` per kind (`'coop'`/`'solo'`), backed by IDB. `mutate(fn)` re-reads latest then writes — keeps the shape a future sync layer needs.
- `usePlayers.ts` — `PlayersStore` (players/save/saveAll/remove/get), `MAX_PLAYERS = 4`, `PLAYER_COLORS` palette (first two = original Thomas/Craig colours), `UNKNOWN_PLAYER` fallback for dangling ids.
- `portraits.tsx` — `PortraitsProvider` + `usePortraits()` context. Overrides stored as IDB blobs, served as object URLs. Lookup order in `Portrait`/`CharacterFace`: override → bundled `img/portraits/{id}.png` → `PortraitFallback` letter tile on img error.
- `coop.ts` — `Side = 0|1` (0 = rows, 1 = cols), `pairKey`, `pairingKey`, `runPairing`, `total`, `winner → 0|1|'tie'`, `initial(name)` for dot letters.
- `time.ts` — `parseTime` requires two-digit `mm:ss` or `h:mm:ss`. `1:2` is REJECTED — was a real bug, do not loosen. `formatTime` renders `00:12:34`.
- localStorage only for UI prefs: `sor4.pairing`, `sor4.solo-player`.

---

## 6. Storage — Decided

**Local-first: IndexedDB + JSON export/import. No backend.** Rationale: players are profiles, not users — runs are logged on one device during couch sessions, so cloud sync solves a problem that mostly doesn't exist. One hosted Pages instance serves the whole community; each visitor's data stays siloed in their own browser.

- Use **IndexedDB** (with `navigator.storage.persist()`) for run/profile data; `localStorage` only for lightweight settings. Plain localStorage risks browser eviction.
- JSON export/import doubles as the backup feature the old app never had — include it in the UI.
- Keep the store behind a clean async interface (the old `useRunStore` shape) so Supabase-style sync could bolt on later without a rewrite. Do NOT build sync now.
- The GitHub PAT/Contents-API layer (`github.ts`, Settings token UI) is dropped entirely from the port.

Existing data to migrate: `data/coop-runs.json` (43 runs) + `data/solo-runs.json` (3 runs) at repo root (kept out of `public/` deliberately — not shipped). Import via Settings → Import JSON; three legacy shapes are detected — bare `thomas`/`craig` coop arrays, bare solo arrays, and the old app's `{coop, solo}` export bundle — all get a player-mapping dialog then merge by id. Export format is `TrackerBackup` (`{app, version: 2, players, coop, solo}`) — full replace on restore.

---

## 7. Build & Verify

- `npm run lint`, `npm run build`, `npm run preview` (port 4173). Node 20 — this machine has no system Node; a portable copy lives at `/tmp/node-v20.19.0-win-x64` (re-download `node-v20.19.0-win-x64.zip` if gone; `export PATH=/tmp/node-v20.19.0-win-x64:$PATH`).
- Deploy: `.github/workflows/deploy.yml` — lint + build + Pages on push to `main`.
- GitHub Pages must be enabled once manually: repo **Settings → Pages → Source → GitHub Actions**.
- Prior project testing method: Playwright driving Chrome over CDP (`Input.dispatchTouchEvent` for pinch/swipe). Reuse for scratch-card and matrix-zoom verification — canvas scratch and pinch zoom are the fiddliest interactions and can't be verified in jsdom.
- No unit test suite — lint + build + interactive smoke is the bar; match or exceed it.

---

## 8. Common Pitfalls

1. **SoR1 vs SoR2 portraits were swapped once** — SoR1 Axel = blue bandana, SoR1 Blaze = red headband. Verify against wiki info cards if touching portraits.
2. **Ordered pairs matter** — (A,B) and (B,A) are different cells. `pairKey` must preserve order.
3. **Time parsing is strict** — two-digit seconds required (`1:02` yes, `1:2` no). Don't "fix" the rejection.
4. **Scratch card gating** — co-op card 2 is locked until card 1 reveals; log UI hidden until all revealed. Easy to break when refactoring.
5. **`hasAltBlitz`** — only SoR1 lacks it. SoR2/SoR3 characters DO have Alt Blitz combos.
6. **Randomiser never repeats cells** — rolls must filter already-logged combinations, and must be scoped to the selected pairing/player.
7. **`destination-out` scratch uses canvas** — jsdom-level tests can't verify it; use the Playwright/CDP path.

---

## 9. Documentation Files

| File | Purpose |
|------|---------|
| `SOR4_TRACKER_HANDOFF.md` | Authoritative spec — domain model, UX conventions, generalisation design. Read first. |
| `AGENTS.md` | This file. |
| Old repo `RavenholmTourist/git_game` | Reference implementation + all data + portraits |

---

## 10. User Working Style Observations

- **Sends "Continue" frequently** — means keep executing the current plan, don't re-explain or re-plan.
- **Expects implementation, not suggestions.** When asked to build something, deliver working code with all hooks wired.
- **Tolerates large multi-step tasks** spanning multiple sessions. Use todo lists to track progress.
- **Prefers terse progress updates** over verbose explanations.
- **Typos in requests are common** — infer intent, don't ask for clarification on obvious meaning.
- **Expects verification** — lint + build clean, plus a Playwright/functional check for interactive features.
