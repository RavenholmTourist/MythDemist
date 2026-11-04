# Streets of Rage 4 Survival Tracker — Developer Handoff

Everything a new session needs to continue, rebuild, or generalize this project.
Written 2026-11-02 by Devin, from the full project session.

---

## 1. What exists today

A browser app that digitizes two personal spreadsheets tracking **Streets of Rage 4**
Survival mode runs between two friends (Thomas and Craig), hosted free on GitHub Pages
with the GitHub repo itself as the data store.

- **Repo:** `RavenholmTourist/git_game` (public)
- **Live site:** https://ravenholmtourist.github.io/git_game/
- **Stack:** React 18 + TypeScript + Vite, no backend, no accounts
- **Storage:** JSON files in the repo (`data/coop-runs.json`, `data/solo-runs.json`),
  written via the GitHub Contents API using a fine-grained PAT the user pastes into
  the app's Settings tab (stored in that browser's localStorage only, never in code)
- **Deploy:** `.github/workflows/deploy.yml` — lint + build + GitHub Pages on push to `main`
- **Imported data:** 43 co-op runs, 3 solo runs (from the two original xlsx files)

## 2. Domain model

### Roster — 21 characters (`src/characters.ts`)

| Game | Characters |
|------|-----------|
| SoR4 | Axel, Blaze, Cherry, Floyd, Adam, Estel, Max, Shiva |
| SoR1 | Axel, Blaze, Adam |
| SoR2 | Axel, Blaze, Max, Skate |
| SoR3 | Axel, Blaze, Skate, Zan, Shiva, Roo |

- Each character has a portrait PNG in `public/img/portraits/{id}.png` where `id =
  {game}-{name}`, e.g. `sor4-axel`. Portraits were cropped/sourced from
  streetsofrage.fandom.com — fan wiki art, **personal use only**, do not monetize.
- `hasAltBlitz` is `false` for SoR1 characters only — they have no Alternate Blitz move.
- Portrait gotcha already fixed once: `sor1-*` vs `sor2-*` Axel/Blaze files were swapped;
  SoR1 Axel = blue bandana, SoR1 Blaze = red headband (verified against the wiki's
  SoR1 info cards).

### Co-op mode — 441 cells

- 21×21 matrix of **ordered** pairs: Thomas's character (rows) × Craig's (columns).
- `CoopRun`: `{ id, thomas, craig, thomasScore, craigScore, level, time, loggedAt }`
  - `thomas`/`craig` are character ids; scores/level are numbers; `time` is `mm:ss` or
    `h:mm:ss`; `loggedAt` is an ISO date string.
- Winner = higher score (ties possible but none logged yet). Scoreboard counts wins.

### Solo Deep mode — 78 cells

- 21 characters × 4 move combos (Default/Alternate Blitz × Default/Alternate Star)
  = 84, minus 6 invalid cells (3 SoR1 chars × 2 Alt-Blitz combos) = **78**.
- `SoloRun`: `{ id, character, blitz, star, level, score, time, loggedAt }`
- Matrix cells for SoR1 × Alt Blitz show "N/A" and are disabled.

### Randomiser

- Picks uniformly from **unlogged** combinations only (never repeats a cell).
- Results appear hidden behind scratch cards: co-op = 2 cards (Thomas then Craig,
  Craig's locked until Thomas's is revealed); solo = character card then moves card.
- Tap = instant reveal with a flash; drag = canvas `destination-out` scratch with
  auto-reveal at 45% cleared. Matrix highlight + "Log this run" stay hidden until
  all cards are revealed.

### Stats deck (`StatsDeck`, `CoopStats`, `SoloStats`)

- One swipeable deck per view — tab pills, ‹ › arrows, pointer swipe, slide animations.
- Co-op panels: Head to head (winning cell per row shown in that player's colour),
  Best pairs, Deepest runs, High scores, Characters (Combined/Thomas/Craig toggle),
  Close calls, Game vs game grid, Char vs char grid (all versions of each name merged),
  Records, Recent runs.
- Pair/deep rows show portraits with a purple **T** or blue **C** dot; the
  better-scoring player's portrait is on the left.
- Solo panels: Top scores, Deepest runs, By move combo, By game, Records, Recent runs.

## 3. UX / styling conventions

- Dark theme. CSS vars in `src/index.css`: `--thomas: #a970ff` (purple),
  `--craig: #3fa9f5` (blue), `--yellow` accent, `game-tag` per game.
- `.thomas-text` / `.craig-text` apply player colours to stats.
- Scoreboard leader shows a roast-chicken sprite (`public/img/chicken.png`, extracted
  via flood-fill white removal) via `::before`/`::after` on `.score-side.leading`.
- `MatrixFrame` wraps both matrices: **Full screen** button opens a fitted overlay with
  two-finger pinch zoom (CSS `zoom`, raw touch handlers), `+/−` buttons, Fit,
  ctrl+wheel, drag-scroll, ✕/Esc to close, `body.no-scroll` while open.
- Modals use `z-index: 300`; fullscreen matrix `z-index: 200`.
- Bebas Neue for headings/numbers, Inter for body.

## 4. Data layer (`src/lib/`)

- `github.ts`: Contents API read/write (`GET`/`PUT` with `sha`), base64 UTF-8 safe
  encode/decode. Settings (`SettingsView.tsx`) let the user set owner/repo/branch/token
  and test the connection. Token lives in `localStorage` under app keys only.
- `useRunStore.ts`: loads runs (fetch → `sor4.cache.{kind}` localStorage fallback),
  exposes save/delete which write back to GitHub and update the cache.
- `time.ts`: `parseTime` requires two-digit `mm:ss` or `h:mm:ss` — `1:2` is REJECTED
  (was a real bug). `formatTime` renders `00:12:34`.
- `coop.ts`: shared helpers — `pairKey`, `total`, `winner`, `pairLabel`.
- Settings key: `localStorage['sor4.settings']`.

## 5. Build & deploy

- `npm run lint`, `npm run build`, `npm run preview` (port 4173). Node 20 via nvm.
- GitHub Pages must be enabled manually once: repo **Settings → Pages → Source →
  GitHub Actions** (the PAT lacked permission to set it via API).
- Devin's token needed **Contents**, **Workflows**, **Pull requests** (RW) to push the
  workflow file; the app's token only needs **Contents RW** on the repo.
- GitHub Actions may report 'Resource not accessible by personal access token' for
  Pages-admin endpoints — use the web UI for those.
- Dev testing method: Playwright driving Chrome over CDP (`localhost:29229`), plus
  `Input.dispatchTouchEvent` for pinch/swipe emulation.

## 6. Neutral / multi-user version — design notes

### Requirements (from owner)

- Up to 4 named players, each with own solo + shared co-op tracking.
- Free to share with the SoR community (no cost, minimal setup, probably public repo).
- Browser first; a real app only if cheap.

### What must change vs. what reuses cleanly

| Area | Reuse | Change needed |
|------|-------|---------------|
| Matrices, forms, scratch cards, fullscreen, stats deck | ~everything | Player fields become dynamic player ids instead of hardcoded thomas/craig |
| `CoopRun` | shape | `{ players: [{playerId, char, score}, {playerId, char, score}] }` — still 2 slots per run |
| Matrix model | 21×21 | Per **player-pairing**: pick which two players' pairing to view; or a matrix per pair |
| Storage | swap layer only | GitHub-PAT model doesn't scale to strangers — see options below |
| Onboarding | none today | Need "add players, pick names + colours" profile setup |
| Hosting | GitHub Pages | Still free; or Netlify/Vercel for edge functions |

### Storage options for a community version

1. **localStorage/IndexedDB + JSON export/import** — zero backend, zero cost, works
   offline; data is per-device (export to share/backup). Simplest possible release:
   literally the current app minus the GitHub layer. Good "v1 for the community".
2. **Supabase / Firebase free tier** — real cloud sync across devices and members of a
   group; anonymous or magic-link auth; free tier is generous for this data volume
   (hundreds of tiny rows). Recommended if multi-device sync matters. PocketBase on a
   $0-5 VPS is the self-hosted equivalent.
3. **GitHub storage as today** — only viable if every group admin does the PAT dance;
   too much friction for community sharing. Not recommended.
4. A single shared public repo for everyone's data is a bad idea (one token would
   have to be shipped or proxied — security hole).

### "Real app" question

- A **PWA** (manifest + service worker, installable, offline, home-screen icon) gives
  ~90% of app feel for ~zero extra cost — recommended.
- Capacitor/TWA wrapping for actual store distribution: possible later, adds signing
  + store accounts for little gain at community-fan scale.

### Suggested model if built

- `Group`/`Room` entity: 1–4 player profiles `{id, name, color}`.
- Co-op matrix rendered for a **selected pairing** (2 of the ≤4 players); the 441-cell
  logic is unchanged per pairing. Randomiser rolls within the selected pairing.
- Solo matrix is per-player (pick which member you're viewing).
- Stats: head-to-head becomes per-pairing; most panels recompute over runs tagged
  with player ids — mostly the same aggregation code parameterized by player.

## 7. Known rough edges / backlog ideas

- No edit of which pairing a run belongs to without re-entering it.
- No backup/export button in the app UI (data is in the repo, but a download button
  is a nice add).
- Emoji (🎲 roll button) renders as tofu on systems without emoji fonts.
- Records panel: longest/shortest run cards are clickable; other stats aren't linked.
- Solo mode has no equivalent of the Char-vs-char-style breakdowns (smaller surface).
