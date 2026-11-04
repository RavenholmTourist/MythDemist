# SoR4 Survival Tracker

A browser app for tracking Streets of Rage 4 Survival mode completion challenges — generalised for up to 4 players and shareable with the community. Successor to the two-player tracker in `RavenholmTourist/git_game`.

- **Co-op**: a 21×21 matrix of every ordered character pairing (441 cells) for a chosen pair of players. Head-to-head win scoreboard, a randomiser that only picks unplayed pairings, scratch-card reveals, and a stats deck.
- **Solo Deep**: a 21×4 matrix of character × Blitz/Star move combos per player (78 valid). SoR1 Axel, Blaze and Adam have no Alternate Blitz, so those cells are blocked.
- **Players**: 1–4 named profiles, each with a colour. Co-op matrices and stats are per ordered pairing; solo progress is per player.

## Data storage

Everything is stored locally in the browser (IndexedDB) — no accounts, no backend, works offline once loaded.

- **Settings → Backup & restore** exports/imports all players and runs as one JSON file. Export regularly; clearing browser data erases everything.
- Legacy JSON files from the old two-player tracker (`data/coop-runs.json`, `data/solo-runs.json` in this repo) can be imported with a player-mapping step.
- **Settings → Character portraits** lets you replace any portrait with your own image, stored on-device.

## Development

```bash
npm install
npm run dev      # local dev server
npm run lint
npm run build    # outputs dist/
npm run preview  # serve the build on :4173
```

Pushing to `main` deploys to GitHub Pages via `.github/workflows/deploy.yml`. Set **Settings → Pages → Source** to "GitHub Actions" once.

`scripts/import_xlsx.py` was a one-off import of the original Google Sheets exports for the legacy app. It needs `openpyxl` and produces the old `thomas`/`craig` run format.

## Credits

Character portraits come from the [Streets of Rage Wiki](https://streetsofrage.fandom.com/wiki/Streets_of_Rage_Wiki). Streets of Rage © SEGA. Streets of Rage 4 © Dotemu, Lizardcube and Guard Crush Games. This is a fan-made, non-commercial tool.
