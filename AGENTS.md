# Project Mythos: development contract

## Purpose and current truth

Mythos is a local, source-grounded mythology learning app, not an authority that can invent a single canon. Prioritise trustworthy teaching over more traditions, more cards, or confident completion claims. The dependency-free frontend uses ES modules; Python serves the app and optional assistant. Greek Heroes has eight explicit five-lesson modules. Other programmes are scaffolds/reuse unless their manifests and authored content prove otherwise.

Read this file, the relevant schemas, neighbouring code, and the actual source passage before editing. Work in small, testable batches. Never call a scaffold, a schema pass, or an AI editorial pass scholarly approval. Do not mark tasks complete merely because files exist.

## Authoritative files and regeneration

- Canonical authored content: `content/lessons/**`, `content/curriculum/**`, corpus manifests, and schemas. Edit these deliberately; increment lesson `version` when facts, questions, or source meaning change.
- `content/curriculum/programmes.json` explicitly maps Greek Heroes to its eight modules. `programme-gates.json` controls prerequisites. Do not bypass gates through tradition switching.
- A selected week JSON is the single source of truth for its lesson list and authored assessment bank. Do not let a duplicated assessment cached in a programme manifest or saved plan override the week file.
- Derived artifacts: `content/index.json` and `content/retrieval/index.json`. Rebuild with `python -B tools/content_pipeline.py` only after read-only checks pass. Do not manually patch generated indexes to conceal a content error.
- `build_greek_programme.py` is a retired, guarded one-time migration after version 2. `build_greek_week.py` is a read-only compatibility check. They must NEVER overwrite hand-edited lessons.
- Other `add_*`, `build_pantheon_scaffolds.py`, `expand_pantheon_weeks.py`, `enrich_*`, and `deepen_generated_lessons.py` are disabled historical scaffold utilities, NOT normal build commands. Their preserved specifications are reference material only; the entry guards prevent execution/import-time writes. Do not remove those guards or run them on the working corpus. Any future generator must default to preview/check, be import-safe, stage output, and refuse existing authored targets. Audit registry/manifests too, not just lessons.
- Validation failure must leave the last working indexes untouched. Keep `--check` read-only. Preserve original corpus files and their attribution/license headers.

## Source integrity: non-negotiable

1. Open the local record, confirm the work, author, translator, genre, and relevant passage. Confirm the locator is in that work, not another work in an anthology. Avoid matching a preface, summary, or translator footnote as ancient text.
2. `evidenceType: quotation` means `excerpt` is verbatim from the local text, allowing whitespace normalisation ONLY. No spelling fixes, omitted words joined without notice, invented punctuation, or silent modernisation. Use `source_evidence.py` for matching. A machine match proves wording exists, not that it supports a claim.
3. `evidenceType: paraphrase` means `excerpt` is our prose, explicitly labelled as such, and `evidenceQuote` contains verbatim supporting text. Never put a paraphrase in quotation marks or call an evidence cue a quotation. Legacy untyped references are unverified, not implicitly quoted.
4. Cite book/chapter/section or a named speech plus a reproducible local anchor. Do not invent ancient line numbers from Gutenberg physical lines. A whole volume or “Heracles traditions” is not a useful locator.
5. Attach every factual claim and quiz answer to relevant declared references. A comparison needs evidence for EACH work/figure compared, not a single convenient Iliad reference. Keep interpretation visibly distinct from narrative fact.
6. Epic, tragedy, mythography, biography, reception, scholarship, folklore, and ethnography are different evidence. Plutarch is not an eyewitness to Theseus. Frazer's account of Pausanias is not Frazer witnessing a legendary hero. Ovid is Roman reception when used in the Greek curriculum. Do not merge versions silently.
7. Respect living traditions, regional differences, and community-specific practice. An epic underworld scene is not proof of a historical cult ritual or everybody's beliefs. Avoid calling every tradition a pantheon.
8. Preserve rights metadata. `personal-local-only` records must not enter generated lesson quotations, assistant evidence, or browser retrieval indexes. Never weaken these controls to make a build pass.
9. `review.status: reviewed` records a substantive editorial check of claim support, locators, pedagogy, and rights; it is not a scholarly credential. If the user explicitly requests an AI-led editorial review, set `reviewType: editorial`, name the AI editor, and state in the notes that this is not independent scholarly review or scholarly certification. Use `reviewType: independent-scholarly` only for an actual named human expert review. Automated validation alone never qualifies.

## Teaching and assessment quality

- Teach the concrete scene first: who acts, what happens, what changes, and why the source distinction matters. Do not substitute abstract “heroism depends on context” slogans for a story the learner has not been taught.
- Five cards should have five useful purposes, not repeat one interpretation. Use clear sentences, readable source excerpts, and one-thumb mobile layouts. Explain unfamiliar terms such as apotheosis. Avoid unsupported universal claims.
- Every single-choice question needs one defensible answer, parallel plausible distractors, and an explanation of the distinction. Wrong answers should reflect real confusions, not “sources are irrelevant” straw men. Do not always place the correct answer first.
- Weekly assessments contain five separately authored questions (`assessment.questions` entries pair `lessonId` with `question`). They are not rotating copies of daily quizzes. Include narrative recall and source/comparison judgement that the cards actually teach.
- Assessment completion is participation-based, not a hidden pass threshold. Be honest about low scores and keep mistakes available for practice; do not equate taking a quiz with secure mastery.
- Preserve neutral daily choices until scratch reveal, Replay lesson, Memory practice, source dialogs, deep dives, and navigation back Home.

## Progression invariants

- `src/progression.js` contains pure run/calendar functions; `src/app.js` coordinates UI and persistence. Test pure rules AND real app transitions.
- Global lesson history/mastery is not proof of completion in a new programme. Run-specific starts, completions, answers, and assessments live in `arcPlans[arcId].weekStates`. Reusing a module must not inherit its earlier start or assessment.
- A week completes only after all its current-version lessons and the current authored assessment bank are completed in that run. Next module and final handoff unlock the FOLLOWING local calendar day.
- Use calendar date components, never elapsed local-midnight milliseconds divided by 24 hours. Cover DST, leap/year boundaries, backward clock movement, missed days, and idle tabs. Refresh on midnight/focus/visibility without interrupting an in-flight lesson.
- Retakes preserve first assessment completion time; record later attempts separately. New assessment content requires a new completion, not credit from the old bank.
- Migration must preserve eligible history and refuse pre-run credit. Do not reset learner data or rewrite plan creation dates to hide migration problems. Preserve the v1 storage key for compatibility.
- Completion statistics must be scoped to the programme; do not include unrelated weak outcomes. Recommend up to three eligible programmes and explain fewer/none honestly. Generated revision tracks reuse content; do not call them newly authored curricula.

## Assistant and server safety

- `.env` and provider keys stay local and must never be served, logged, read into a review response, committed, or sent to the browser. Static paths are allowlisted; test encoded traversal, hidden files, directory listing, and symlink escape boundaries. Keep loopback binding.
- Current assistant mode is deliberately extractive: a model may select verbatim retrieved quotations, NOT freely synthesize a “verified answer.” Citation ID membership cannot establish factual entailment. The backend validates response shape, exact quotations, and complete accounting of output text. Do not re-enable free prose without an explicit design/review and adversarial grounding tests.
- Preserve tradition/genre/translator/coverage boundaries in retrieval and prompts. Parse XML and separate editor notes from primary text. Do not label all raw file content as ancient testimony.
- Invalid provider output, unsupported queries, or provider failures must degrade safely to local evidence. Do not leak provider errors or use real hosted APIs in automated tests. Backend and browser fallback filters must agree.

## Verification and delivery

From repository root (Python with `jsonschema`; no Node runtime required):

```text
python -B tools/content_pipeline.py --check
python -B tools/test_regressions.py
python -B tools/test_assistant.py
python -B tools/content_pipeline.py
python -B tools/test_browser.py
```

`test_browser.py` uses installed Chrome/Chromium (`--chrome PATH` if needed), a temporary profile/server, and no provider. It runs pure calendar/run regressions and the full 40-lesson/eight-assessment browser flow with simulated day rollovers. Test storage is `mythos.test.progress.v1`; production is `mythos.progress.v1`. Never clear the latter for testing. Test pages must use `?test=1` when loading the app.

Add a failing regression before a fix where practical. Cover incorrect answers and locked states, not only the happy path. Assert actual scores/persisted state rather than assuming answer A is correct. Keep browser errors at zero. Add targeted comments explaining invariants and security/source decisions, not noisy line-by-line narration.

Before finishing: review the diff, run the commands relevant to your changes, state exactly what passed and what could not be tested, and disclose remaining editorial uncertainty. Do not claim a real provider was verified by a mock test. Never silently drop blocked work. Do not push, commit, delete user files, reset progress, or alter repository security settings without the user's explicit instruction.
