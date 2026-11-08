# Project Mythos

A source-grounded, mobile-first mythology learning prototype.

## Current prototype

The first usable slice is a dependency-free local web app because Node.js is not installed in the current environment. It includes:

- a mobile home dashboard with today’s lesson, week progress, learning stats, and badges;
- registry-driven pantheon libraries for Greek, Norse, Egyptian, Celtic, Slavic, Japanese, and Roman traditions;
- simple local pantheon logos with distinct accent themes;
- a five-lesson Greek Heroes week plus starter lessons for six additional pantheons;
- tap-based navigation with optional swipe;
- deferred quiz answers with a scratch-card result reveal;
- Memory practice built from completed lessons;
- source excerpts and local corpus links;
- multi-card rabbit-hole topics;
- eight-week arc plans generated from local learning history;
- local lesson/card/question progress, mastery, badges, streaks, likes/dislikes, and feedback;
- a purple/teal global shell with support for neutral quiz theming;
- JSON schemas for lessons, progress, pantheons, arcs, weeks, topics, and art.

## Run locally

For the app plus the corpus assistant API, run:

```bash
python tools/mythos_server.py --port 4873
```

Then open:

```text
http://localhost:4873/
```

A plain static server also works, but the assistant falls back to local passage retrieval rather than the backend endpoint.

## Assistant provider

Without a provider, `/api/assistant` returns retrieval-only evidence. To enable generated answers, either export these settings in your shell or copy `.env.example` to `.env` and fill in the values. `.env` is ignored by git.

```bash
MYTHOS_LLM_PROVIDER=openai|anthropic|ollama
MYTHOS_LLM_MODEL=<model-name>
MYTHOS_LLM_API_KEY=<key-not-required-for-ollama>
# optional endpoint override
MYTHOS_LLM_BASE_URL=<provider-url>
```

The assistant is intentionally extractive: a configured model selects verbatim quotations from retrieved passages, not a freely synthesized or fact-verified answer. The backend checks response shape, quotation wording, retrieved IDs, and that every output word is accounted for by those quotations. Relevance and interpretation still require judgement. Invalid output and provider failures fall back to local evidence. Retrieval respects the selected tradition, separates XML editorial notes, and excludes personal-local-only copies. The local server allowlists app paths and does not serve `.env` or developer files.

## Daily curriculum pacing

Lessons unlock by local calendar day, including across daylight-saving changes. Each programme run has its own module starts, lesson completions, and assessments. When a module starts, day one is available immediately and each later day unlocks after midnight. A completed module releases the next on the following local day; the app refreshes on midnight or resume without interrupting a lesson. Retakes do not move the first completion date. Arc choices are hidden during a run; on the day after completion the home screen offers up to three eligible recommendations, with honest handling of fewer options. Generated revision tracks reuse existing modules, not newly authored content. Historical learner data is retained; revised lessons and assessment banks require current-version completion. Programme prerequisites are defined in `content/curriculum/programme-gates.json`: `arc.greek-heroes` is the starter, most programmes require one named completion, and later tradition programmes also require broader curriculum progress.

## Verify

Validate content and regenerate the shared/retrieval indexes:

```bash
python -B tools/content_pipeline.py --check
python -B tools/test_regressions.py
python -B tools/test_assistant.py
python -B tools/content_pipeline.py
python -B tools/test_browser.py
```

With the local server running, open:

```text
http://localhost:4873/tests/browser-smoke.html
```

The browser runner starts its own server with the provider disabled and uses a temporary Chrome profile. Supply `--chrome PATH` if Chrome is not discovered. It tests calendar/run migration invariants and completes all 40 Greek lessons and eight authored assessments using simulated local-day rollovers, then checks the completion handoff, gates, scratch reveal, rabbit hole, Memory practice, and assistant evidence. The smoke page uses a separate `mythos.test.progress.v1` key; it never clears real learner progress. Read `AGENTS.md` before further development. Greek lessons remain editorial drafts pending independent scholarly review; passing tests is not certification.

## Important paths

- `index.html`, `styles.css`, `src/app.js` — prototype shell and interaction logic
- `content/pantheons.json` — active/planned pantheon registry and content paths
- `content/index.json` — generated content index
- `tools/content_pipeline.py` — validation and index generation
- `tools/mythos_server.py` — static app plus `/api/assistant`
- `tools/mythos_assistant.py` — retrieval, grounded prompt, provider calls, and citation validation
- `tools/build_retrieval_index.py` — corpus chunk index generation
- `content/retrieval/index.json` — generated retrieval corpus
- `content/curriculum/greek/greek-heroes-week-01.json` — Greek week plan
- `content/curriculum/norse/norse-gods-week-01.json` — Norse week plan
- `content/curriculum/arcs/` — shared/cross-pantheon arc records
- `content/lessons/` — pantheon lesson modules
- `content/corpus/` — local source manifests and texts
- `data/schemas/` — content and learner-state contracts
- `product/greek-heroes-prototype.md` — learning and product design brief

## Source and rights rule

Ancient-source claims must be tied to a stable source record and locator. Roman reception and modern adaptation material are stored separately from Greek evidence. Some corpus records are marked `personal-local-only`; generated or exported lesson text should prefer cleared translations and preserve provenance.
