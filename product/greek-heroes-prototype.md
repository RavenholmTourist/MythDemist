# Greek Heroes prototype brief

This document turns the learning-science and product requirements into the first buildable prototype. It is a design contract, not a claim that there is one universally correct lesson length.

## Learning-design basis

The format should be driven by three well-supported principles:

1. **One focused objective per micro-lesson.** Microlearning research commonly defines units by scope—one concept or skill—rather than by a magical duration. Evidence reviews report benefits, but also warn that “short” alone does not make instruction effective.
2. **Retrieval beats rereading.** Research on the testing effect shows that answering questions improves later retention more than simply restudying the same material. Every lesson therefore needs at least one low-pressure retrieval action.
3. **Spacing protects retention.** Distributed-practice research consistently favors revisiting ideas over time over doing everything in one session. Completion should expose material; delayed correct retrieval should establish mastery.

Supporting choices:

- **Immediate explanatory feedback** should state what was correct, why, and which source supports it. Feedback should help the learner know where they are going, how they are doing, and what to do next.
- **Variants should be a first-class skill.** Mythology is especially suited to questions like “Which source says this?” and “Which version is later reception?” These teach source literacy rather than one synthetic canon.
- **Optional depth must not block the core loop.** “Ask More” is a reward and a source-literacy feature, not another mandatory lesson step.

## Prototype lesson size

Use a measurable starting point, then adjust from the user’s feedback and completion data.

- **Core path:** 4–6 large cards, approximately 180–320 words total.
- **Reading time target:** 60–120 seconds for the core path.
- **Quiz:** 2 tap-to-answer questions:
  - one recall or comprehension check;
  - one source/variant check where the content supports it.
- **Immediate feedback:** 1–3 short sentences plus a source link.
- **Optional depth:** one “Ask More” card after each answer with 2–4 suggested prompts and cited passages.
- **Flavor:** at most one clearly labeled comparison card per lesson. Never count a modern adaptation as evidence for the ancient version.

If a lesson cannot fit this size, split it rather than compressing it. The estimate should be generated from word count and validated against actual user completion time.

## Greek Heroes pilot week

Use five daily lessons plus an optional synthesis review. Five required days gives a full theme without demanding a perfect seven-day streak.

| Day | Focus | Main evidence base | Learning outcome |
|---|---|---|---|
| 1 | What makes a Greek hero? | *Iliad*, *Odyssey*, Hesiodic genealogy where useful | Describe heroism as a source-specific ideal involving honor, excellence, divine ancestry or favor, and costly conflict—not a modern moral category. |
| 2 | Achilles: excellence, anger, and grief | *Iliad* | Explain that the *Iliad* presents a compressed episode centered on Achilles’ anger and its consequences, not the whole Trojan War. |
| 3 | Odysseus: cunning, identity, and return | *Odyssey* | Distinguish Odyssean intelligence and endurance from straightforward physical heroism. |
| 4 | Jason and Medea: quest and aftermath | *Argonautica* and Euripides’ *Medea* | Compare how an epic quest narrative and a later tragedy frame the same heroic cycle differently. |
| 5 | Theseus and Heracles as changing heroes | Pseudo-Apollodorus, Plutarch, and supporting tragedy | Recognize that later mythography and biography organize heroic traditions differently and preserve multiple variants. |
| Review | One hero, many versions | All week’s sources | Identify which claim belongs to which source and separate Greek evidence from Roman or modern reception. |

The first implementation may reduce this to Day 1–3 if authoring all five lessons would slow the UI prototype.

## Progress and mastery model

Track exposure separately from learning:

- **Seen:** card viewed or lesson opened.
- **Completed:** all required cards and quiz states reached.
- **Learning:** at least one correct answer for an outcome.
- **Secure:** correct on at least two separate days, including one delayed review.
- **Mastered:** correct on at least three attempts across a longer interval, with no unresolved misconception flag.

Store events, not only totals, so future adaptive logic can improve:

- lesson/card opened and completed;
- quiz answer, correctness, confidence, response time, and attempt count;
- review due date and review result;
- source/deep-dive opened;
- topic and learning-outcome mastery;
- streak activity, while making missed days non-punitive;
- likes, dislikes, issue tags, and free-text feedback;
- content version associated with every event.

Use local persistence first. Start with a versioned local-storage document for simplicity, then move event history to IndexedDB when the schema stabilizes or storage needs grow.

## Badge rules

Badges should reward learning behavior, not only time spent:

- **First Reading:** complete one lesson.
- **Source Scout:** open three cited source/deep-dive passages.
- **Variant Detective:** correctly answer five source-variant questions.
- **Hero Scholar:** reach “secure” mastery for the Greek Heroes week outcomes.
- **Weekly Synthesis:** complete the end-of-week review.
- **Returner:** complete reviews on three separate days.
- **Streak badges:** optional milestones at 3, 7, and 14 active days; never shame the learner for a missed day.
- **Critical Reader:** answer a disguised-pantheon or reception-vs-source question correctly.
- **Helpful Critic:** submit useful lesson feedback or report a content issue.

## Lesson feedback model

Collect feedback at two levels:

- **Lesson:** like/dislike, optional tags such as `too-long`, `too-easy`, `too-hard`, `unclear`, `want-more-sources`, `want-more-flavor`, plus free text.
- **Question/content:** report `wrong-answer`, `bad-choice`, `unclear`, `citation-problem`, `tone`, or `technical-issue`.

Feedback should create an editorial backlog linked to the exact content version. It should not automatically rewrite lessons without review.

## AI / Ask More boundary

The in-app LLM should be provider-agnostic. Gemini and OpenAI can sit behind the same request contract; do not choose the provider until the first retrieval path works.

Recommended answer modes:

- **Corpus only (default):** retrieve approved local passages, pass only those passages to the model, require citations, and validate every citation against returned chunk IDs.
- **Corpus + web (explicit opt-in):** allow internet retrieval, but label it separately. Web sources may add context or modern scholarship leads; they must not silently override the vetted corpus.
- **Unavailable:** if no relevant local evidence exists, say so and offer to switch to web-assisted mode.

Do not place API keys in browser code or commit them to the repository. For a personal local prototype, use a localhost service with keys loaded from environment variables or a local `.env` excluded from Git. If hosted later, use a secrets manager.

## Theme model

Use a data-driven theme rather than hard-coding Greek colors into components.

- **Global shell:** purple and teal.
- **Greek pantheon accent:** gold.
- **Neutral quiz mode:** graphite/slate with muted violet when the quiz must not reveal the pantheon.
- **Correctness:** use icons/text plus green/red states; never rely on color alone.
- **Accessibility:** preserve contrast, minimum touch targets, keyboard support, reduced motion, and readable typography. Pantheon accents should affect headers, progress accents, and decorative borders—not make body text hard to read.

## Art model

Start with institutional open-access sources before fan art:

- The Met Open Access: CC0 images and API.
- Art Institute of Chicago Open Access: CC0 images and API.
- Wikimedia Commons: usable only after checking the individual file page and license; Commons itself warns that reusers must verify the stated license.
- Fan art: include only with an explicit reusable license or creator permission. “Posted online” is not permission.

Each art record should store title, creator, date, collection/source, source URL, file/local path, license, license URL, required attribution, subjects, pantheon visibility, verification date, and notes. Ancient object images can support evidence; modern fan art should be labeled flavor unless it is an openly licensed illustration used only decoratively.

## Build order

1. Define the lesson, progress, badge, feedback, theme, and art schemas.
2. Author one verified Greek Heroes lesson.
3. Build the mobile-first reading/quiz/progress loop.
4. Add review scheduling, mastery, badges, and feedback.
5. Add corpus retrieval and citation validation.
6. Add the optional LLM service and provider adapter.
7. Add the art catalog and licensed images.
