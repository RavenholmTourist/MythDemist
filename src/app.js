import { calendarDays, runWeek, completionDate, finishAssessment, migratePlan, assessmentKey } from './progression.js';

const REGISTRY_URL = "./content/pantheons.json";
const ART_URL = "./content/art/catalog.json";
const INDEX_URL = "./content/index.json";
const SHARED_MAP_URL = "./content/curriculum/shared/learning-map.json";
const RETRIEVAL_URL = "./content/retrieval/index.json";
const ACTIVE_PANTHEON = "greek";
// Smoke tests use separate storage; visiting a test page must not erase real learning history.
const STORAGE_KEY = new URLSearchParams(location.search).get('test') === '1' ? 'mythos.test.progress.v1' : 'mythos.progress.v1';

const BADGES = {
  "week-started": {
    label: "Week Started",
    icon: "▶",
    description: "Open the first Greek Heroes lesson."
  },
  "first-reading": {
    label: "First Reading",
    icon: "✓",
    description: "Complete one lesson."
  },
  "critical-reader": {
    label: "Critical Reader",
    icon: "◆",
    description: "Answer every question correctly in a lesson."
  },
  "source-scout": {
    label: "Source Scout",
    icon: "⌕",
    description: "Open two cited source passages."
  },
  "hero-scholar": {
    label: "Hero Scholar",
    icon: "★",
    description: "Reach secure mastery for this lesson’s outcomes."
  },
  "daily-returner": {
    label: "Daily Returner",
    icon: "↻",
    description: "Learn on two separate days."
  },
  "helpful-critic": {
    label: "Helpful Critic",
    icon: "✎",
    description: "Send lesson feedback."
  }
};

const MASTERY_LABELS = {
  unseen: "Not seen",
  seen: "Seen",
  learning: "Learning",
  secure: "Secure",
  mastered: "Mastered"
};

const app = document.querySelector("#app");
const appShell = document.querySelector("#appShell");
const topbarStatus = document.querySelector("#topbarStatus");
const sourceDialog = document.querySelector("#sourceDialog");
const deepDiveDialog = document.querySelector("#deepDiveDialog");
const topicDialog = document.querySelector("#topicDialog");
const pantheonLogo = document.querySelector("#pantheonLogo");
const weekLabel = document.querySelector("#weekLabel");

let week;
let manifest;
let artRecords = new Map();
let learningMap;
let learningMaps = new Map();
let sharedMap;
let topicLibrary = new Map();
let recordLibrary = new Map();
let contentIndex;
let registry;
let pantheonConfig;
let lessons = new Map();
let lessonLibrary = new Map();
let lesson;
let activeArc;
let activeArcWeek;
let runtimeNotice;
let retrievalIndex;
let progress = loadProgress();
let runtime = createRuntime();
let displayedDay = localDate();
let refreshingCalendar = false;

function createRuntime() {
  return {
    view: "home",
    activeLessonId: null,
    cardIndex: 0,
    quizIndex: 0,
    answers: {},
    resultsFinalized: false,
    reviewQuestions: [],
    reviewIndex: 0,
    reviewMode: "practice",
    topicId: null,
    assistantQuery: "",
    assistantResults: [],
    assistantError: null,
    assistantSeed: "",
    assistantResponse: null,
    traditionFilter: "all",
    feedback: {
      rating: null,
      tags: new Set(),
      text: "",
      submitted: false
    }
  };
}

function defaultProgress() {
  return {
    schemaVersion: 1,
    lessons: {},
    outcomes: {},
    badges: {},
    sourceOpens: {},
    arcChoice: null,
    arcPlans: {},
    arcHistory: [],
    weeks: {},
    activePantheon: "greek",
    activityDates: [],
    streak: {
      current: 0,
      best: 0,
      lastActiveDate: null
    },
    events: [],
    feedback: []
  };
}

function loadProgress() {
  try {
    const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
    return { ...defaultProgress(), ...(stored || {}) };
  } catch {
    return defaultProgress();
  }
}

function saveProgress() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
}

function localDate(date = new Date()) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function previousLocalDate(dateString) {
  const [year, month, day] = dateString.split("-").map(Number);
  const date = new Date(year, month - 1, day);
  date.setDate(date.getDate() - 1);
  return localDate(date);
}

function recordActivity() {
  const today = localDate();
  if (progress.streak.lastActiveDate !== today) {
    progress.streak.current =
      progress.streak.lastActiveDate === previousLocalDate(today)
        ? progress.streak.current + 1
        : 1;
    progress.streak.best = Math.max(progress.streak.best, progress.streak.current);
    progress.streak.lastActiveDate = today;
  }

  if (!progress.activityDates.includes(today)) {
    progress.activityDates.push(today);
  }
}

function recordEvent(type, details = {}) {
  recordActivity();
  progress.events.push({ type, at: new Date().toISOString(), ...details });
}

function lessonState(target = lesson) {
  if (!target) return null;
  if (!progress.lessons[target.id]) {
    progress.lessons[target.id] = {
      contentVersion: target.version,
      startedAt: null,
      completedAt: null,
      cardViews: {},
      questions: {},
      nextReviewAt: null,
      feedbackIds: []
    };
  }
  return progress.lessons[target.id];
}

function ensureOutcome(id) {
  if (!progress.outcomes[id]) {
    progress.outcomes[id] = {
      seen: false,
      correctDates: [],
      incorrectDates: [],
      mastery: "unseen",
      updatedAt: null
    };
  }
  return progress.outcomes[id];
}

function updateMastery(outcome) {
  const correctDays = outcome.correctDates.length;
  outcome.mastery =
    correctDays >= 3
      ? "mastered"
      : correctDays >= 2
        ? "secure"
        : correctDays >= 1
          ? "learning"
          : outcome.seen
            ? "seen"
            : "unseen";
  outcome.updatedAt = new Date().toISOString();
}

function markOutcomeSeen(id) {
  const outcome = ensureOutcome(id);
  outcome.seen = true;
  updateMastery(outcome);
}

function markOutcomeAttempt(id, correct) {
  const outcome = ensureOutcome(id);
  const today = localDate();
  outcome.seen = true;
  const dateList = correct ? outcome.correctDates : outcome.incorrectDates;
  if (!dateList.includes(today)) {
    dateList.push(today);
  }
  updateMastery(outcome);
}

function unlockBadge(id) {
  if (progress.badges[id]) return false;
  progress.badges[id] = { unlockedAt: new Date().toISOString() };
  return true;
}

function refreshBadges(target = lesson) {
  if (!target) return;
  const state = lessonState(target);
  if (Object.keys(state.cardViews).length > 0) unlockBadge("week-started");
  if (state.completedAt) unlockBadge("first-reading");
  if (Object.keys(progress.sourceOpens).length >= 2) unlockBadge("source-scout");
  if (progress.activityDates.length >= 2) unlockBadge("daily-returner");
  if (progress.feedback.some((item) => item.lessonId === target.id)) {
    unlockBadge("helpful-critic");
  }
  if (target.quiz.every((question) => state.questions[question.id]?.correct === true)) {
    unlockBadge("critical-reader");
  }
  if (
    target.learningObjectives.every((objective) =>
      ["secure", "mastered"].includes(progress.outcomes[objective.id]?.mastery)
    )
  ) {
    unlockBadge("hero-scholar");
  }
}

function recordCardView(card, target = lesson) {
  const state = lessonState(target);
  state.startedAt ||= new Date().toISOString();
  state.cardViews[card.id] = new Date().toISOString();
  card.objectiveIds.forEach(markOutcomeSeen);
  recordEvent("card-view", { lessonId: target.id, cardId: card.id });
  refreshBadges(target);
  saveProgress();
}

function recordSourceOpen(refId, target = lesson) {
  progress.sourceOpens[refId] = (progress.sourceOpens[refId] || 0) + 1;
  recordEvent("source-open", { lessonId: target?.id || null, sourceRefId: refId });
  refreshBadges(target);
  saveProgress();
}

function recordAnswer(question, choiceId, target = lesson) {
  const state = lessonState(target);
  const questionKey = runtime.view === 'review' && runtime.reviewMode === 'assessment' ? `assessment:${question.id}` : question.id;
  const previous = state.questions[questionKey] || { attempts: 0 };
  const correct = choiceId === question.answerId;
  const answeredAt = new Date().toISOString();

  state.questions[questionKey] = {
    attempts: previous.attempts + 1,
    lastChoiceId: choiceId,
    correct,
    answeredAt
  };

  const runState = currentWeekState(target.weekId);
  if (runState) {
    const entry = runState.lessons[target.id] ||= { completedAt: null, questions: {} };
    if ((entry.contentVersion || 1) < target.version) {
      entry.completedAt = null;
      entry.questions = {};
    }
    entry.contentVersion = target.version;
    entry.questions[questionKey] = { ...state.questions[questionKey] };
  }
  question.objectiveIds.forEach((objectiveId) => {
    markOutcomeAttempt(objectiveId, correct);
  });

  recordEvent("quiz-answer", {
    lessonId: target.id,
    questionId: question.id,
    choiceId,
    correct,
    mode: runtime.view === "review" ? "review" : "lesson"
  });
  refreshBadges(target);
  saveProgress();
}

function completeLesson(target = lesson) {
  const state = lessonState(target);
  state.completedAt ||= new Date().toISOString();
  const runState = currentWeekState(target.weekId);
  if (runState) {
    const entry = runState.lessons[target.id] ||= { completedAt: null, questions: {} };
    entry.contentVersion = target.version;
    entry.completedAt ||= new Date().toISOString();
  }
  state.contentVersion = target.version;
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  state.nextReviewAt ||= tomorrow.toISOString();
  recordEvent("lesson-complete", { lessonId: target.id });
  refreshBadges(target);
  saveProgress();
}

function submitFeedback() {
  if (runtime.feedback.submitted) return;
  const target = activeLesson();
  const text = (document.querySelector("#feedbackText")?.value || runtime.feedback.text).trim();
  const rating = runtime.feedback.rating;
  const tags = [...runtime.feedback.tags];

  if (!rating && !text && tags.length === 0) {
    return;
  }

  const item = {
    id: `fb-${Date.now()}`,
    lessonId: target.id,
    contentVersion: target.version,
    rating,
    tags,
    text,
    createdAt: new Date().toISOString()
  };
  progress.feedback.push(item);
  lessonState(target).feedbackIds.push(item.id);
  recordEvent("lesson-feedback", { lessonId: target.id, rating, tags });
  runtime.feedback.submitted = true;
  refreshBadges(target);
  saveProgress();
}

async function loadContent() {
  const [registryResponse, artResponse, indexResponse, sharedMapResponse] = await Promise.all([
    fetch(REGISTRY_URL),
    fetch(ART_URL),
    fetch(INDEX_URL),
    fetch(SHARED_MAP_URL)
  ]);
  if (!registryResponse.ok || !artResponse.ok || !indexResponse.ok || !sharedMapResponse.ok) {
    throw new Error("Could not load the pantheon registry, art catalog, or content index.");
  }
  registry = await registryResponse.json();
  contentIndex = await indexResponse.json();
  sharedMap = await sharedMapResponse.json();
  pantheonConfig = registry.pantheons[progress.activePantheon] || registry.pantheons.greek;
  const artCatalog = await artResponse.json();
  artRecords = new Map(artCatalog.records.map((item) => [item.id, item]));

  ensureArcPlan();
  activeArc = allArcChoices().find((arc) => arc.id === progress.arcChoice) || null;
  activeArcWeek = activeArc ? selectActiveArcWeek(activeArc) : null;
  const weekPath = activeArcWeek?.weekPath || pantheonConfig.paths.activeWeek;
  const [weekResponse, manifestResponse, mapResponse] = await Promise.all([
    fetch(`./${weekPath}`),
    fetch(`./${pantheonConfig.paths.corpusManifest}`),
    fetch(`./${pantheonConfig.paths.learningMap}`)
  ]);
  if (!weekResponse.ok || !manifestResponse.ok || !mapResponse.ok) {
    throw new Error("Could not load the active pantheon content.");
  }
  week = await weekResponse.json();
  manifest = await manifestResponse.json();
  learningMap = await mapResponse.json();
  artRecords = new Map(artCatalog.records.map((item) => [item.id, item]));

  const activePantheons = Object.values(registry.pantheons).filter((item) => item.status === "active" && item.paths?.learningMap && item.paths?.corpusManifest);
  const libraries = await Promise.all(activePantheons.map(async (item) => {
    const [mapRes, manifestRes] = await Promise.all([
      fetch(`./${item.paths.learningMap}`),
      fetch(`./${item.paths.corpusManifest}`)
    ]);
    return { id: item.id, map: await mapRes.json(), manifest: await manifestRes.json() };
  }));
  learningMaps = new Map(libraries.map((item) => [item.id, item.map]));
  learningMaps.set("shared", sharedMap);
  topicLibrary = new Map();
  recordLibrary = new Map();
  [...libraries, { id: "shared", map: sharedMap, manifest: { records: [] } }].forEach((item) => {
    Object.entries(item.map.topics || {}).forEach(([id, topic]) => {
      topicLibrary.set(id, { ...topic, pantheon: item.id });
    });
    item.manifest.records.forEach((record) => {
      const indexed = contentIndex.sources?.find((source) => source.id === record.id);
      recordLibrary.set(record.id, {
        ...record,
        available: indexed?.available !== false,
        pantheon: item.id,
        corpusPath: `content/corpus/${item.id}/${record.localPath}`
      });
    });
  });

  const lessonResponses = await Promise.all(
    week.days
      .filter((day) => day.lessonPath)
      .map(async (day) => {
        const response = await fetch(`./${day.lessonPath}`);
        if (!response.ok) throw new Error(`Could not load ${day.lessonPath}`);
        return response.json();
      })
  );

  lessons = new Map(lessonResponses.map((item) => [item.id, item]));
  const historical = await Promise.all((contentIndex.lessons || [])
    .filter((item) => item.path && progress.lessons[item.id]?.completedAt && !lessons.has(item.id))
    .map(async (item) => {
      const response = await fetch(`./${item.path}`);
      if (!response.ok) throw new Error(`Could not load completed lesson ${item.id}`);
      return response.json();
    }));
  lessonLibrary = new Map([...historical, ...lessonResponses].map((item) => [item.id, item]));
  [...lessonLibrary.values()].forEach((item) => validateLesson(item, manifest));
  ensureWeekStarted();
  lesson = chooseTodayLesson();
  runtime.activeLessonId = lesson?.id || null;
  renderBrand();
}

function localDateFromIso(isoDate) {
  return isoDate ? localDate(new Date(isoDate)) : null;
}

function nextLocalDate(dateString) {
  const date = new Date(`${dateString}T00:00:00`);
  date.setDate(date.getDate() + 1);
  return localDate(date);
}

function daysBetween(startDate, endDate = localDate()) {
  return calendarDays(startDate, endDate);
}

function currentWeekState(weekId = week?.id) {
  const plan = progress.arcPlans[progress.arcChoice];
  return plan?.weeks.some((entry) => entry.weekId === weekId) ? runWeek(plan, weekId) : null;
}

function lessonCompleted(target) {
  const entry = currentWeekState(target?.weekId)?.lessons[target?.id];
  return entry && (entry.contentVersion || 1) >= target.version ? entry.completedAt : null;
}

function ensureWeekStarted(targetWeek = week) {
  if (!targetWeek) return;
  const state = currentWeekState(targetWeek.id);
  if (state && !state.startedAt) {
    state.startedAt = new Date().toISOString();
    saveProgress();
  }
}

function weekStartedOn(targetWeek = week) {
  return localDateFromIso(currentWeekState(targetWeek?.id)?.startedAt) || localDate();
}

function isDayUnlocked(day) {
  const state = currentWeekState();
  if (!state?.startedAt) return day.day === 1;
  return day.day <= daysBetween(localDateFromIso(state.startedAt)) + 1;
}

function isLessonUnlocked(target) {
  const day = week.days.find((item) => item.lessonId === target?.id);
  return day ? isDayUnlocked(day) : false;
}

function chooseTodayLesson() {
  const available = week.days.filter((day) => day.lessonId && lessons.has(day.lessonId));
  const unlocked = available.filter(isDayUnlocked);
  const unfinished = unlocked.find((day) => !lessonCompleted(lessons.get(day.lessonId)));
  const preview = available.find((day) => !isDayUnlocked(day));
  const selected = unfinished || preview || available[available.length - 1];
  return selected ? lessons.get(selected.lessonId) : undefined;
}

function validateLesson(data, corpusManifest) {
  const sourceIds = new Set(Object.keys(data.sourceReferences || {}));
  const objectiveIds = new Set(data.learningObjectives.map((item) => item.id));
  const manifestRecords = recordLibrary.size ? recordLibrary : new Map(corpusManifest.records.map((item) => [item.id, item]));

  for (const block of data.narrativeBlocks) {
    assert(
      block.sourceRefIds.every((id) => sourceIds.has(id)),
      `${block.id} references an unknown source.`
    );
    assert(
      block.objectiveIds.every((id) => objectiveIds.has(id)),
      `${block.id} references an unknown objective.`
    );
  }

  for (const question of data.quiz) {
    assert(
      question.choices.some((choice) => choice.id === question.answerId),
      `${question.id} has an invalid answer ID.`
    );
    assert(
      question.sourceRefIds.every((id) => sourceIds.has(id)),
      `${question.id} references an unknown source.`
    );
    assert(
      question.objectiveIds.every((id) => objectiveIds.has(id)),
      `${question.id} references an unknown objective.`
    );
  }

  for (const [id, source] of Object.entries(data.sourceReferences)) {
    const record = manifestRecords.get(source.recordId);
    assert(record, `${id} references missing manifest record ${source.recordId}.`);
    const expectedPath = record.corpusPath || `content/corpus/${data.pantheon}/${record.localPath}`;
    assert(
      source.localPath === expectedPath,
      `${id} local path does not match the corpus manifest.`
    );
  }
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function activeLesson() {
  return lessons.get(runtime.activeLessonId) || lesson;
}

function availableLessons() {
  return week.days
    .filter((day) => day.lessonId && lessons.has(day.lessonId))
    .map((day) => lessons.get(day.lessonId));
}

function weekAssessmentState(weekId = week?.id) {
  const state = currentWeekState(weekId)?.assessment;
  const bank = progress.arcPlans[progress.arcChoice]?.weeks.find((entry) => entry.weekId === weekId)?.assessment;
  return state?.contentKey === assessmentKey(bank) ? state : null;
}

function isWeekComplete() {
  return availableLessons().length > 0 && availableLessons().every(lessonCompleted);
}

function getWeekAssessmentQuestions() {
  // Assessment prompts are authored separately, not recycled daily answers.
  return (week.assessment?.questions || []).map((item) => ({
    lesson: lessons.get(item.lessonId), question: item.question, wasCorrect: false, priority: 100
  })).filter((item) => item.lesson && lessonCompleted(item.lesson));
}

function getReviewQuestions() {
  const masteryRank = { unseen: 4, seen: 3, learning: 2, secure: 1, mastered: 0 };
  return [...lessonLibrary.values()]
    .filter((item) => lessonState(item).completedAt)
    .flatMap((item) =>
      item.quiz.map((question) => ({
        lesson: item,
        question,
        wasCorrect: lessonState(item).questions[question.id]?.correct === true,
        priority:
          (lessonState(item).questions[question.id]?.correct === true ? 0 : 100) +
          question.objectiveIds.reduce((sum, id) => sum + (masteryRank[progress.outcomes[id]?.mastery || "unseen"] * 10), 0) +
          (lessonState(item).nextReviewAt && new Date(lessonState(item).nextReviewAt) <= new Date() ? 15 : 0) +
          topicAffinity(`${item.title} ${item.tags.join(" ")}`) * 5
      }))
    )
    .sort((a, b) => b.priority - a.priority);
}

function renderBrand() {
  weekLabel.textContent = `${week.title} · Week ${activeArcWeek?.week || 1} of 8`;
  pantheonLogo.innerHTML = logoSvg(week.visual?.logo || week.pantheon);
}

function logoSvg(key) {
  if (key === "greek-bolt" || key === "greek") {
    return `
      <svg viewBox="0 0 48 48" role="img" aria-label="Greek pantheon">
        <defs>
          <linearGradient id="greekGold" x1="0" x2="1" y1="0" y2="1">
            <stop offset="0" stop-color="#ffe08a" />
            <stop offset="0.55" stop-color="#d8a419" />
            <stop offset="1" stop-color="#9c6b00" />
          </linearGradient>
        </defs>
        <circle cx="24" cy="24" r="22" fill="url(#greekGold)" />
        <path d="M29 6 17 27h8l-4 15 13-23h-8z" fill="#241503" />
      </svg>
    `;
  }
  if (key === "norse-hammer" || key === "norse") {
    return `<svg viewBox="0 0 48 48" role="img" aria-label="Norse pantheon">
      <circle cx="24" cy="24" r="22" fill="#7dd3fc" />
      <path d="M17 8h15l4 10h-8l8 15H20l-4-10h8z" fill="#0f3044" />
      <path d="M19 24h11v16H19z" fill="#0f3044" opacity="0.9" />
    </svg>`;
  }
  if (key === "egyptian-ankh" || key === "egyptian") {
    return `<svg viewBox="0 0 48 48" role="img" aria-label="Egyptian pantheon">
      <circle cx="24" cy="24" r="22" fill="#1d4ed8" />
      <circle cx="24" cy="15" r="6" fill="none" stroke="#facc15" stroke-width="4" />
      <path d="M24 20v20M14 25h20" stroke="#facc15" stroke-width="4" stroke-linecap="round" />
    </svg>`;
  }
  if (key === "celtic-knot" || key === "celtic") {
    return `<svg viewBox="0 0 48 48" role="img" aria-label="Celtic pantheon">
      <circle cx="24" cy="24" r="22" fill="#047857" />
      <path d="M24 10c8 4 8 12 0 16s-16 0-8 12c-8-4-8-12 0-16s16 0 8-12z" fill="none" stroke="#d1fae5" stroke-width="3" stroke-linejoin="round" />
    </svg>`;
  }
  if (key === "slavic-fire" || key === "slavic") {
    return `<svg viewBox="0 0 48 48" role="img" aria-label="Slavic pantheon">
      <circle cx="24" cy="24" r="22" fill="#7f1d1d" />
      <path d="M25 8c6 7-2 9 4 15 5 5-1 14-7 15-7-7 2-9-2-13-4-5 1-12 5-17z" fill="#fdba74" />
    </svg>`;
  }
  if (key === "japanese-torii" || key === "japanese") {
    return `<svg viewBox="0 0 48 48" role="img" aria-label="Japanese pantheon">
      <circle cx="24" cy="24" r="22" fill="#be123c" />
      <path d="M12 15h24M15 11h18M16 15v24M32 15v24M14 25h20" stroke="#fff1f2" stroke-width="3" stroke-linecap="round" />
    </svg>`;
  }
  if (key === "chinese-dragon" || key === "chinese") {
    return `<svg viewBox="0 0 48 48" role="img" aria-label="Chinese pantheon">
      <circle cx="24" cy="24" r="22" fill="#0f766e" />
      <path d="M13 29c7-15 18-16 22-8 3 6-3 10-8 9 5 3 10 1 12-3-2 10-18 14-26 2z" fill="#a7f3d0" />
      <circle cx="31" cy="18" r="2" fill="#064e3b" />
    </svg>`;
  }
  if (key === "meso-serpent" || key === "mesoamerican") {
    return `<svg viewBox="0 0 48 48" role="img" aria-label="Mesoamerican pantheon">
      <circle cx="24" cy="24" r="22" fill="#7c2d12" />
      <path d="M12 29 18 17l6 9 6-14 6 18-6 8-6-10-6 8z" fill="#fbbf24" />
      <circle cx="33" cy="18" r="2" fill="#451a03" />
    </svg>`;
  }
  if (key === "mesopotamian-star" || key === "mesopotamian") {
    return `<svg viewBox="0 0 48 48" role="img" aria-label="Mesopotamian pantheon">
      <circle cx="24" cy="24" r="22" fill="#b45309" />
      <path d="M24 8l3 12 11-3-9 7 9 7-11-3-3 12-3-12-11 3 9-7-9-7 11 3z" fill="#fef3c7" />
    </svg>`;
  }
  if (key === "indian-lotus" || key === "indian") {
    return `<svg viewBox="0 0 48 48" role="img" aria-label="Indian pantheon">
      <circle cx="24" cy="24" r="22" fill="#9a3412" />
      <path d="M24 35c-4-4-4-12 0-18 4 6 4 14 0 18zm0 0c-8 0-13-4-14-10 5-1 11 1 14 10zm0 0c8 0 13-4 14-10-5-1-11 1-14 10z" fill="#fde68a" />
    </svg>`;
  }
  if (key === "polynesian-wave" || key === "polynesian") {
    return `<svg viewBox="0 0 48 48" role="img" aria-label="Polynesian pantheon">
      <circle cx="24" cy="24" r="22" fill="#0369a1" />
      <path d="M11 30c8 0 9-13 20-10 8 2 4 13-4 11 7-7-4-10-10-2-3 5-4 8-6 1z" fill="#bae6fd" />
      <path d="M12 36c7 3 17 3 24-2" stroke="#bae6fd" stroke-width="3" stroke-linecap="round" />
    </svg>`;
  }
  if (key === "shared-war" || key === "shared") {
    return `<svg viewBox="0 0 48 48" role="img" aria-label="Shared pantheon theme">
      <circle cx="24" cy="24" r="22" fill="#475569" />
      <path d="M16 34 30 10h5L21 34zM12 14h16l-2 6H15z" fill="#f8fafc" />
      <circle cx="34" cy="34" r="5" fill="#14b8a6" />
    </svg>`;
  }
  if (key === "roman-laurel" || key === "roman") {
    return `<svg viewBox="0 0 48 48" role="img" aria-label="Roman pantheon">
      <circle cx="24" cy="24" r="22" fill="#581c87" />
      <path d="M18 35c-5-7-3-16 3-22M30 35c5-7 3-16-3-22" fill="none" stroke="#fde68a" stroke-width="3" stroke-linecap="round" />
      <path d="M20 31c-4-2-6-4-7-8M28 31c4-2 6-4 7-8M21 23c-3-2-5-4-5-8M27 23c3-2 5-4 5-8" stroke="#fde68a" stroke-width="2" stroke-linecap="round" />
    </svg>`;
  }
  return `
    <svg viewBox="0 0 48 48" role="img" aria-label="Mythos">
      <circle cx="24" cy="24" r="22" fill="#8b5cf6" />
      <path d="M14 32V16l10 10 10-10v16" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
    </svg>
  `;
}

function render() {
  const active = activeLesson();
  appShell.dataset.theme = active?.themeMode === "pantheon" ? active.pantheon : "neutral";
  appShell.dataset.quizTheme =
    ["quiz", "review"].includes(runtime.view) && active?.themeMode === "neutral"
      ? "neutral"
      : "known";

  if (runtime.view === "home") renderHome();
  if (runtime.view === "cards") renderCard();
  if (runtime.view === "quiz") renderQuiz();
  if (runtime.view === "scratch") renderScratch();
  if (runtime.view === "review") renderReview();
  if (runtime.view === "review-complete") renderReviewComplete();
  if (runtime.view === "topic") renderTopic();
  if (runtime.view === "complete") renderComplete();
  if (runtime.view === "assistant") renderAssistant();
  renderTopbar();
  app.focus({ preventScroll: true });
}

function renderTopbar() {
  const active = activeLesson();
  if (!active) {
    topbarStatus.textContent = "";
    return;
  }

  if (runtime.view === "review" || runtime.view === "review-complete") {
    topbarStatus.textContent = `${runtime.reviewIndex + 1}/${runtime.reviewQuestions.length} review`;
    return;
  }
  if (runtime.view === "scratch") {
    topbarStatus.textContent = "Scratch result";
    return;
  }

  const state = lessonState(active);
  const correct = active.quiz.filter((question) => state.questions[question.id]?.correct).length;
  topbarStatus.textContent = state.completedAt
    ? `✓ Complete · ${correct}/${active.quiz.length}`
    : `${Object.keys(state.cardViews).length}/${active.narrativeBlocks.length} cards`;
}

function renderHome() {
  if (displayedDay !== localDate() && !refreshingCalendar) {
    refreshCalendar();
    return;
  }
  const today = chooseTodayLesson();
  lesson = today;
  runtime.activeLessonId = today?.id || null;
  const state = { ...lessonState(today), completedAt: lessonCompleted(today) };
  const todayUnlocked = isLessonUnlocked(today);
  const completedLessons = availableLessons().filter(lessonCompleted).length;
  const reviewCount = getReviewQuestions().length;
  const stats = overallStats();

  app.innerHTML = `
    <section class="hero-card" aria-labelledby="todayTitle">
      <p class="hero-kicker">Today · ${escapeHtml(today.estimatedMinutes)} min · ${escapeHtml(week.pantheon)}</p>
      <h1 id="todayTitle">${escapeHtml(today.title)}</h1>
      <p class="subtitle">${escapeHtml(today.subtitle)}. Big cards, short reading, source-backed checks.</p>

      <div class="stat-grid" aria-label="Current lesson progress">
        <div class="stat-card"><h2>Read</h2><strong>${Object.keys(state.cardViews).length}/${today.narrativeBlocks.length}</strong></div>
        <div class="stat-card"><h2>Correct</h2><strong>${correctCount(today)}/${today.quiz.length}</strong></div>
        <div class="stat-card"><h2>Mastery</h2><strong>${masterySummaryText(today)}</strong></div>
      </div>

      <div class="bottom-actions" style="margin-top: 1rem;">
        <button class="secondary-button" type="button" data-action="open-first-source">Sources</button>
        <button class="primary-button" type="button" data-action="start-lesson" data-lesson-id="${escapeHtml(today.id)}" ${todayUnlocked ? "" : "disabled"}>
          ${todayUnlocked ? (state.completedAt ? "Replay lesson" : state.startedAt ? "Continue" : "Start today") : "Unlocks at midnight"}
        </button>
      </div>
    </section>

    <div class="dashboard-grid">
      <section class="dashboard-card" aria-labelledby="reviewTitle">
        <p class="eyebrow">${isWeekComplete() && week.assessment ? "Weekly assessment" : "Memory practice"}</p>
        <h2 id="reviewTitle">${isWeekComplete() && week.assessment ? escapeHtml(week.assessment.title) : "Build on what you’ve learned"}</h2>
        <p>${isWeekComplete() && week.assessment ? escapeHtml(week.assessment.prompt) : reviewCount ? `${reviewCount} source-backed question${reviewCount === 1 ? "" : "s"} ready.` : "Finish today’s lesson to unlock practice questions."}</p>
        <button class="primary-button full-width" type="button" data-action="${isWeekComplete() && week.assessment ? "start-week-assessment" : "start-review"}" ${(isWeekComplete() && week.assessment ? getWeekAssessmentQuestions().length : reviewCount) ? "" : "disabled"}>${isWeekComplete() && week.assessment ? (weekAssessmentState()?.completedAt ? "Retake assessment" : "Start assessment") : "Start practice"}</button>
        ${isWeekComplete() && week.assessment ? `<button class="secondary-button full-width" type="button" data-action="start-review" ${reviewCount ? '' : 'disabled'}>Memory practice</button>` : ''}
      </section>

      <section class="dashboard-card" aria-labelledby="assistantTitle">
        <p class="eyebrow">Corpus research</p>
        <h2 id="assistantTitle">Ask the local sources</h2>
        <p>Search the local myth corpus with cited passages. This is corpus-only; unsupported questions say so.</p>
        <button class="secondary-button full-width" type="button" data-action="open-assistant">Open researcher</button>
      </section>

      <section class="dashboard-card" aria-labelledby="statsTitle">
        <p class="eyebrow">Learning stats</p>
        <h2 id="statsTitle">Your trail</h2>
        <dl class="stats-list">
          <div><dt>Lessons</dt><dd>${completedLessons}/${week.days.length}</dd></div>
          <div><dt>Accuracy</dt><dd>${stats.accuracy}%</dd></div>
          <div><dt>Cards read</dt><dd>${stats.cards}</dd></div>
          <div><dt>Sources</dt><dd>${stats.sources}</dd></div>
          <div><dt>Topics</dt><dd>${stats.topics}</dd></div>
          <div><dt>Secure+</dt><dd>${stats.secure}</dd></div>
          <div><dt>Practice</dt><dd>${stats.practice}</dd></div>
          <div><dt>Streak</dt><dd>${progress.streak.current}d</dd></div>
        </dl>
      </section>
    </div>

    <section class="week-card" aria-labelledby="weekTitle">
      <div class="week-card-header">
        <div>
          <p class="eyebrow">This week</p>
          <h2 id="weekTitle">${escapeHtml(week.title)}</h2>
        </div>
        <strong>${completedLessons}/${week.days.length}</strong>
      </div>
      <div class="progress-track"><div class="progress-fill" style="width:${(completedLessons / week.days.length) * 100}%"></div></div>
      <div class="week-days">
        ${week.days.map((day) => renderWeekDay(day)).join("")}
      </div>
    </section>

    ${renderArcSection()}

    ${renderPantheonSection()}

    <section class="dashboard-card badge-panel" aria-label="Badges">
      <p class="eyebrow">Badges</p>
      <div class="badge-shelf">${renderBadgeShelf()}</div>
    </section>
  `;
}

function correctCount(target) {
  const state = lessonState(target);
  return target.quiz.filter((question) => state.questions[question.id]?.correct).length;
}

function overallStats() {
  const questionStates = availableLessons().flatMap((item) => Object.values(lessonState(item).questions));
  const correct = questionStates.filter((item) => item.correct).length;
  return {
    questions: questionStates.length,
    correct,
    accuracy: questionStates.length ? Math.round((correct / questionStates.length) * 100) : 0,
    cards: availableLessons().reduce((sum, item) => sum + Object.keys(lessonState(item).cardViews).length, 0),
    sources: Object.values(progress.sourceOpens).reduce((sum, count) => sum + count, 0),
    topics: new Set(progress.events.filter((event) => event.type === "topic-open").map((event) => event.topicId)).size,
    secure: Object.values(progress.outcomes).filter((item) => ["secure", "mastered"].includes(item.mastery)).length,
    practice: progress.events.filter((event) => event.type === "review-complete").length
  };
}

function renderWeekDay(day) {
  const target = day.lessonId ? lessons.get(day.lessonId) : null;
  if (!target) {
    return `
      <div class="week-day planned" aria-label="Day ${day.day}, planned">
        <span class="day-number">${day.day}</span>
        <span><strong>${escapeHtml(day.title)}</strong><small>Coming soon</small></span>
      </div>
    `;
  }

  const state = { ...lessonState(target), completedAt: lessonCompleted(target) };
  const unlocked = isDayUnlocked(day);
  const status = !unlocked ? "Unlocks at midnight" : state.completedAt ? "Complete" : state.startedAt ? "In progress" : "Available";
  return `
    <button class="week-day" type="button" data-action="select-lesson" data-day="${day.day}" data-lesson-id="${escapeHtml(target.id)}" aria-label="Day ${day.day}: ${escapeHtml(day.title)}" ${unlocked ? "" : "disabled"}>
      <span class="day-number">${day.day}</span>
      <span><strong>${escapeHtml(day.title)}</strong><small>${status}</small></span>
      <span class="day-status">${state.completedAt ? "✓" : unlocked ? "›" : "•"}</span>
    </button>
  `;
}

function masterySummaryText(target = lesson) {
  const levels = target.learningObjectives.map(
    (objective) => progress.outcomes[objective.id]?.mastery || "unseen"
  );
  const best = levels.includes("mastered")
    ? "Mastered"
    : levels.includes("secure")
      ? "Secure"
      : levels.includes("learning")
        ? "Learning"
        : levels.includes("seen")
          ? "Seen"
          : "New";
  return best;
}

function renderBadgeShelf() {
  return Object.entries(BADGES)
    .map(([id, badge]) => {
      const unlocked = Boolean(progress.badges[id]);
      return `<span class="badge-chip ${unlocked ? "unlocked" : ""}" title="${escapeHtml(badge.description)}">
        <span aria-hidden="true">${badge.icon}</span>${escapeHtml(badge.label)}${unlocked ? "" : " · locked"}
      </span>`;
    })
    .join("");
}

function renderCard() {
  const target = activeLesson();
  const card = target.narrativeBlocks[runtime.cardIndex];
  recordCardView(card, target);
  const isFirst = runtime.cardIndex === 0;
  const isLast = runtime.cardIndex === target.narrativeBlocks.length - 1;
  const progressPercent = ((runtime.cardIndex + 1) / target.narrativeBlocks.length) * 100;

  app.innerHTML = `
    <article class="lesson-card" aria-labelledby="cardTitle">
      <div class="card-media-bar" aria-hidden="true"></div>
      <div class="lesson-card-body">
        <div class="card-topline">
          <span class="kind-chip">${escapeHtml(card.kind)}</span>
          <span class="progress-count">Card ${runtime.cardIndex + 1} of ${target.narrativeBlocks.length}</span>
        </div>
        <h1 id="cardTitle">${escapeHtml(card.title)}</h1>
        <p class="body-copy">${escapeHtml(card.body)}</p>
        <div class="source-list" aria-label="Cited sources">
          ${renderSourceButtons(card.sourceRefIds, target)}
        </div>
        <div class="card-spacer"></div>
        <div class="progress-track" aria-hidden="true"><div class="progress-fill" style="width:${progressPercent}%"></div></div>
        <div class="bottom-actions">
          <button class="secondary-button" type="button" data-action="previous-card" ${isFirst ? "disabled" : ""}>Back</button>
          <button class="primary-button" type="button" data-action="next-card">${isLast ? "Start quiz" : "Next"}</button>
        </div>
      </div>
    </article>
  `;
  attachSwipe(isLast);
}

function attachSwipe(isLast) {
  const element = app.querySelector(".lesson-card");
  let startX = null;
  element.addEventListener("touchstart", (event) => {
    startX = event.changedTouches[0].clientX;
  }, { passive: true });
  element.addEventListener("touchend", (event) => {
    if (startX === null) return;
    const delta = event.changedTouches[0].clientX - startX;
    if (delta < -56) navigateCard(1, isLast);
    if (delta > 56) navigateCard(-1, isLast);
    startX = null;
  }, { passive: true });
}

function renderSourceButtons(refIds, target) {
  return refIds
    .map((id) => {
      const source = target.sourceReferences[id];
      return `<button class="source-button" type="button" data-action="open-source" data-source-id="${escapeHtml(id)}" data-lesson-id="${escapeHtml(target.id)}">
        ${escapeHtml(source.work)} · ${escapeHtml(source.locator)}
      </button>`;
    })
    .join("");
}

function renderRecordButtons(recordIds) {
  const records = recordLibrary;
  return recordIds
    .map((id) => records.get(id))
    .filter(Boolean)
    .map((record) => `<button class="source-button" type="button" data-action="open-record" data-record-id="${escapeHtml(record.id)}" ${record.available ? "" : "disabled"} aria-disabled="${record.available ? "false" : "true"}">
      ${escapeHtml(record.title)}${record.available ? "" : " · local-only source not included"}
    </button>`)
    .join("");
}

function renderQuiz() {
  const target = activeLesson();
  const question = target.quiz[runtime.quizIndex];
  const answer = runtime.answers[question.id];
  app.innerHTML = renderQuestionCard({
    kind: "Quiz",
    context: target,
    question,
    answer,
    index: runtime.quizIndex,
    total: target.quiz.length,
    backAction: "back-to-cards",
    nextAction: "next-question",
    nextLabel: runtime.quizIndex === target.quiz.length - 1 ? "Scratch results" : "Next question",
    deferFeedback: true
  });
}

function renderReview() {
  const item = runtime.reviewQuestions[runtime.reviewIndex];
  const answerKey = reviewAnswerKey(item);
  const answer = runtime.answers[answerKey];
  app.innerHTML = renderQuestionCard({
    kind: `${runtime.reviewMode === "assessment" ? "Weekly assessment" : "Review"} · ${item.lesson.title}`,
    context: item.lesson,
    question: item.question,
    answer,
    index: runtime.reviewIndex,
    total: runtime.reviewQuestions.length,
    backAction: "home",
    backLabel: "Home",
    nextAction: "next-review",
    nextLabel: runtime.reviewIndex === runtime.reviewQuestions.length - 1 ? "Finish review" : "Next review"
  });
}

function reviewAnswerKey(item) {
  return `${item.lesson.id}:${item.question.id}`;
}

function renderQuestionCard({ kind, context, question, answer, index, total, backAction, backLabel = "Cards", nextAction, nextLabel, deferFeedback = false }) {
  const progressPercent = ((index + 1) / total) * 100;
  return `
    <article class="lesson-card" aria-labelledby="questionPrompt">
      <div class="card-media-bar" aria-hidden="true"></div>
      <div class="lesson-card-body">
        <div class="card-topline">
          <span class="kind-chip">${escapeHtml(kind)}</span>
          <span class="progress-count">Question ${index + 1} of ${total}</span>
        </div>
        <h1 class="quiz-prompt" id="questionPrompt">${escapeHtml(question.prompt)}</h1>
        <div class="choice-list">
          ${question.choices.map((choice, choiceIndex) => renderChoice(question, choice, choiceIndex, answer, deferFeedback)).join("")}
        </div>
        ${answer && !deferFeedback ? renderAnswerFeedback(question, answer, context) : ""}
        <div class="card-spacer"></div>
        <div class="progress-track" aria-hidden="true"><div class="progress-fill" style="width:${progressPercent}%"></div></div>
        <div class="bottom-actions">
          <button class="secondary-button" type="button" data-action="${backAction}">${backLabel}</button>
          <button class="primary-button" type="button" data-action="${nextAction}" ${answer ? "" : "disabled"}>${nextLabel}</button>
        </div>
      </div>
    </article>
  `;
}

function renderChoice(question, choice, index, answer, deferFeedback = false) {
  const selected = answer?.choiceId === choice.id;
  const answered = Boolean(answer);
  const status = deferFeedback
    ? selected ? "selected" : ""
    : answered && choice.id === question.answerId
      ? "correct"
      : answered && selected
        ? "incorrect"
        : "";
  const statusText = status === "correct" ? " · correct" : status === "incorrect" ? " · not quite" : "";
  const action = runtime.view === "review" ? "answer-review" : "answer-question";
  return `
    <button class="choice-button ${status}" type="button" data-action="${action}" data-choice-id="${escapeHtml(choice.id)}" ${answered && !deferFeedback ? "disabled" : ""}>
      <span class="choice-letter" aria-hidden="true">${String.fromCharCode(65 + index)}</span>
      <span>${escapeHtml(choice.text)}<span class="visually-hidden">${statusText}</span></span>
    </button>
  `;
}

function renderAnswerFeedback(question, answer, context) {
  const correct = answer.choiceId === question.answerId;
  return `
    <section class="feedback-panel ${correct ? "correct" : "incorrect"}" aria-live="polite">
      <h2>${correct ? "✓ Correct" : "! Not quite"}</h2>
      <p>${escapeHtml(question.explanation)}</p>
      <div class="source-list">
        ${renderSourceButtons(question.sourceRefIds, context)}
        <button class="prompt-button" type="button" data-action="open-deep-dive" data-question-id="${escapeHtml(question.id)}" data-lesson-id="${escapeHtml(context.id)}">
          Ask more ↗
        </button>
      </div>
    </section>
  `;
}

function renderScratch() {
  const target = activeLesson();
  const score = target.quiz.filter((question) =>
    runtime.answers[question.id]?.choiceId === question.answerId
  ).length;

  app.innerHTML = `
    <section class="result-card scratch-view" aria-labelledby="scratchTitle">
      <p class="hero-kicker">Scratch card</p>
      <h1 id="scratchTitle">Your result is sealed.</h1>
      <p class="subtitle">Scratch the gold foil or use the reveal button to see how you did.</p>
      <div class="scratch-card" id="scratchCard">
        <div class="scratch-result">
          <span>${score}/${target.quiz.length}</span>
          <strong>${score === target.quiz.length ? "Mythic!" : "Result revealed"}</strong>
        </div>
        <canvas id="scratchCanvas" aria-hidden="true"></canvas>
      </div>
      <div class="continue-panel">
        <button class="secondary-button" type="button" data-action="back-to-quiz">Answers</button>
        <button class="primary-button" type="button" data-action="reveal-results">Reveal results</button>
      </div>
      <p class="fine-print">Your answers are saved only when the result is revealed.</p>
    </section>
  `;
  initializeScratchCard();
}

function initializeScratchCard() {
  const card = document.querySelector("#scratchCard");
  const canvas = document.querySelector("#scratchCanvas");
  if (!card || !canvas) return;

  const rect = card.getBoundingClientRect();
  const scale = window.devicePixelRatio || 1;
  canvas.width = Math.max(1, Math.floor(rect.width * scale));
  canvas.height = Math.max(1, Math.floor(rect.height * scale));
  const ctx = canvas.getContext("2d");
  ctx.scale(scale, scale);
  const gradient = ctx.createLinearGradient(0, 0, rect.width, rect.height);
  gradient.addColorStop(0, "#b88900");
  gradient.addColorStop(0.5, "#f4d35e");
  gradient.addColorStop(1, "#7c3aed");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, rect.width, rect.height);
  ctx.fillStyle = "rgba(36, 21, 3, 0.7)";
  ctx.font = "800 18px system-ui";
  ctx.textAlign = "center";
  ctx.fillText("SCRATCH TO REVEAL", rect.width / 2, rect.height / 2);

  let scratching = false;
  const scratch = (event) => {
    const point = canvas.getBoundingClientRect();
    const x = event.clientX - point.left;
    const y = event.clientY - point.top;
    ctx.globalCompositeOperation = "destination-out";
    ctx.beginPath();
    ctx.arc(x, y, 24, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalCompositeOperation = "source-over";
  };
  const checkCleared = () => {
    const pixels = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    let clear = 0;
    for (let index = 3; index < pixels.length; index += 16) {
      if (pixels[index] < 40) clear += 1;
    }
    if (clear / (pixels.length / 16) > 0.34) revealResults();
  };

  canvas.addEventListener("pointerdown", (event) => {
    scratching = true;
    canvas.setPointerCapture(event.pointerId);
    scratch(event);
  });
  canvas.addEventListener("pointermove", (event) => {
    if (!scratching) return;
    scratch(event);
  });
  canvas.addEventListener("pointerup", () => {
    scratching = false;
    checkCleared();
  });
}

function revealResults() {
  if (runtime.resultsFinalized) return;
  const target = activeLesson();
  target.quiz.forEach((question) => {
    const answer = runtime.answers[question.id];
    if (answer) recordAnswer(question, answer.choiceId, target);
  });
  completeLesson(target);
  runtime.resultsFinalized = true;
  runtime.view = "complete";
  render();
}

function renderRewardArt(target) {
  const art = artRecords.get(target.rewardArtId);
  if (!art) return "";
  return `
    <figure class="reward-art">
      <img src="./${escapeHtml(art.localPath)}" alt="${escapeHtml(art.alt)}" loading="lazy">
      <figcaption>
        <strong>${escapeHtml(art.title)}</strong>
        <span>${escapeHtml(art.creator)} · ${escapeHtml(art.date)}</span>
        <a class="text-link" href="${escapeHtml(art.sourceUrl)}" target="_blank" rel="noreferrer">${escapeHtml(art.collection)} · ${escapeHtml(art.license)}</a>
      </figcaption>
    </figure>
  `;
}

function renderQuizBreakdown(target) {
  const state = lessonState(target);
  return `
    <section class="quiz-breakdown" aria-label="Quiz breakdown">
      <p class="eyebrow">Result breakdown</p>
      ${target.quiz.map((question, index) => {
        const result = state.questions[question.id];
        const correct = result?.correct === true;
        return `<details class="breakdown-item" ${index === 0 ? "open" : ""}>
          <summary>${correct ? "✓" : "!"} Question ${index + 1}: ${escapeHtml(question.prompt)}</summary>
          <p>${escapeHtml(question.explanation)}</p>
          <div class="source-list">${renderSourceButtons(question.sourceRefIds, target)}</div>
        </details>`;
      }).join("")}
    </section>
  `;
}

function programmeStats(plan) {
  const ids = new Set(plan.weeks.flatMap((item) => item.lessonIds || []));
  const lessonStates = plan.weeks.flatMap((entry) => Object.values(runWeek(plan, entry.weekId).lessons)).filter((state) => state.completedAt);
  const answers = lessonStates.flatMap((state) => Object.values(state.questions || {}));
  const objectives = new Set((contentIndex.lessons || []).filter((item) => ids.has(item.id)).flatMap((item) => item.objectiveIds || []));
  const weak = [...objectives].filter((id) => !['secure', 'mastered'].includes(progress.outcomes[id]?.mastery));
  return {
    lessons: lessonStates.length,
    accuracy: answers.length ? Math.round((answers.filter((item) => item.correct).length / answers.length) * 100) : 0,
    weakOutcomes: weak.length,
    weakTopics: (contentIndex.lessons || []).filter((item) => ids.has(item.id) && item.objectiveIds?.some((id) => weak.includes(id))).map((item) => item.title)
  };
}

function renderComplete() {
  const target = activeLesson();
  const state = lessonState(target);
  const correct = correctCount(target);
  const reviewCount = getReviewQuestions().length;
  const nextDay = nextAvailableDay(target);

  app.innerHTML = `
    <section class="result-card" aria-labelledby="completeTitle">
      <p class="hero-kicker">Lesson complete</p>
      <h1 id="completeTitle">Nice work.</h1>
      <p class="subtitle">You answered ${correct} of ${target.quiz.length} correctly. Keep going with practice or choose a related topic below.</p>

      ${renderRewardArt(target)}

      <div class="continue-panel">
        <button class="secondary-button" type="button" data-action="home">Home</button>
        ${nextDay ? `<button class="primary-button" type="button" data-action="select-lesson" data-lesson-id="${escapeHtml(nextDay.lessonId)}">Day ${nextDay.day}: ${escapeHtml(nextDay.title)}</button>` : isWeekComplete() && week.assessment ? `<button class="primary-button" type="button" data-action="start-week-assessment">Weekly assessment</button>` : `<button class="primary-button" type="button" data-action="start-review" ${reviewCount ? "" : "disabled"}>Memory practice</button>`}
      </div>

      <ul class="mastery-list" aria-label="Learning outcome mastery">
        ${target.learningObjectives.map((objective) => `
          <li class="mastery-item">
            <span>${escapeHtml(objective.text)}</span>
            <strong class="mastery-level">${escapeHtml(MASTERY_LABELS[progress.outcomes[objective.id]?.mastery || "unseen"])}</strong>
          </li>
        `).join("")}
      </ul>

      ${renderQuizBreakdown(target)}

      <div class="badge-shelf">${renderBadgeShelf()}</div>

      <section class="suggested-panel" aria-labelledby="suggestedTitle">
        <p class="eyebrow">Learn more</p>
        <h2 id="suggestedTitle">Suggested topics</h2>
        <div class="topic-list">
          ${suggestedTopicsFor(target).map((topic) => renderTopicButton(topic)).join("")}
        </div>
      </section>

      <section class="feedback-panel" style="background:#f5f3fb; border:1px solid #e2dcf4;">
        <h2>Rate this lesson</h2>
        <div class="feedback-actions">
          <button class="feedback-rating ${runtime.feedback.rating === "like" ? "selected" : ""}" type="button" data-action="set-rating" data-rating="like">👍 Liked</button>
          <button class="feedback-rating ${runtime.feedback.rating === "dislike" ? "selected" : ""}" type="button" data-action="set-rating" data-rating="dislike">👎 Disliked</button>
        </div>
        <div class="tag-grid" aria-label="Feedback tags">
          ${target.feedbackOptions.map((tag) => `
            <button class="tag-toggle ${runtime.feedback.tags.has(tag) ? "selected" : ""}" type="button" data-action="toggle-feedback-tag" data-tag="${escapeHtml(tag)}">
              ${escapeHtml(tag.replaceAll("-", " "))}
            </button>
          `).join("")}
        </div>
        <textarea id="feedbackText" class="feedback-text" placeholder="What should be clearer, shorter, harder, or more interesting?">${escapeHtml(runtime.feedback.text)}</textarea>
        <div class="bottom-actions" style="margin-top:0.75rem;">
          <button class="secondary-button" type="button" data-action="retake-lesson">Replay lesson</button>
          <button class="primary-button" type="button" data-action="submit-feedback">${runtime.feedback.submitted ? "Feedback saved" : "Send feedback"}</button>
        </div>
        <p class="form-note">Feedback is stored locally with this lesson version and becomes an editorial backlog, not an automatic rewrite.</p>
      </section>
    </section>
  `;
}

function topicAffinity(title) {
  const words = title.toLowerCase().split(/[^a-z]+/);
  const signals = [
    ...progress.feedback.filter((item) => item.rating === "like").flatMap((item) => item.tags),
    ...progress.events.filter((event) => event.type === "topic-open").map((event) => event.topicId || "")
  ].join(" ").toLowerCase();
  return words.reduce((score, word) => score + (word.length > 3 && signals.includes(word) ? 1 : 0), 0);
}

function allArcChoices() {
  return [...(contentIndex.arcChoices || []), ...(contentIndex.arcs || []), ...generatedArcChoices()];
}

function arcWeekTitle(item) {
  return typeof item === "string" ? item : item.theme;
}

function weekModules() {
  return (contentIndex.weeks || []).filter((item) => item.path && item.lessonIds?.length);
}

function moduleScore(arc, module, usedPantheons) {
  const text = `${arc.title} ${arc.description || ""} ${(arc.weeks || []).map(arcWeekTitle).join(" ")}`.toLowerCase();
  const moduleText = `${module.title} ${module.pantheon} ${(module.themes || []).join(" ")}`.toLowerCase();
  const overlap = text.split(/[^a-z0-9]+/).filter((word) => word.length > 4 && moduleText.includes(word)).length;
  return overlap * 4 + topicAffinity(moduleText) + (usedPantheons.has(module.pantheon) ? 0 : 2) + (module.pantheon === arc.pantheon ? 1 : 0);
}

function arcWeekModules(arc) {
  const modules = weekModules();
  const preferred = arc.weekPath ? modules.find((item) => item.path === arc.weekPath) : modules.find((item) => item.pantheon === arc.pantheon);
  const used = new Set(preferred ? [preferred.id] : []);
  const usedPantheons = new Set(preferred ? [preferred.pantheon] : []);
  const rest = modules.filter((item) => !used.has(item.id))
    .sort((a, b) => moduleScore(arc, b, usedPantheons) - moduleScore(arc, a, usedPantheons))
    .filter((item) => { used.add(item.id); usedPantheons.add(item.pantheon); return true; });
  return [...(preferred ? [preferred] : []), ...rest].slice(0, 8);
}

function createArcPlan(arc) {
  const explicitModules = (arc.programmeWeeks || []).map((entry) => weekModules().find((module) => module.id === entry.weekId) || entry);
  const modules = explicitModules.length ? explicitModules : arcWeekModules(arc);
  return {
    arcId: arc.id,
    runId: crypto.randomUUID(),
    progressVersion: 2,
    weekStates: {},
    createdAt: new Date().toISOString(),
    status: "active",
    generatedFrom: {
      topicOpens: progress.events.filter((event) => event.type === "topic-open").length,
      likedTags: progress.feedback.filter((item) => item.rating === "like").flatMap((item) => item.tags)
    },
    weeks: (arc.weeks || []).slice(0, 8).map((theme, index) => {
      const module = modules[index];
      const explicit = arc.programmeWeeks?.[index];
      return {
        week: index + 1,
        title: explicit?.theme || arcWeekTitle(theme) || module?.title || `Week ${index + 1}`,
        weekId: module?.weekId || module?.id,
        weekPath: module?.path || module?.weekPath,
        pantheonId: module?.pantheon,
        lessonIds: module?.lessonIds || [],
        lessonVersions: Object.fromEntries((module?.lessonIds || []).map((id) => [id, contentIndex.lessons.find((item) => item.id === id)?.version || 1])),
        // The authored week file is canonical for its assessment bank; manifests only select modules.
        assessment: module?.assessment || explicit?.assessment || null,
        status: index === 0 ? "active" : "planned",
        unlocksOn: null,
        completedOn: null
      };
    })
  };
}

function planWeekCompletion(entry, plan) {
  return completionDate(entry, plan);
}

function syncArcPlan(plan) {
  migratePlan(plan, progress);
  plan.weeks.forEach((entry, index) => {
    const completedOn = planWeekCompletion(entry, plan);
    entry.completedOn = completedOn;
    if (completedOn) {
      entry.status = "complete";
      return;
    }
    const previous = plan.weeks[index - 1];
    const ready = index === 0 || (previous?.completedOn && localDate() > previous.completedOn);
    entry.status = ready ? "active" : "planned";
    entry.unlocksOn = !ready && previous?.completedOn ? nextLocalDate(previous.completedOn) : null;
  });
  plan.status = plan.weeks.every((entry) => entry.status === "complete") ? "complete" : "active";
  if (plan.status === "complete" && !progress.arcHistory.some((item) => item.arcId === plan.arcId)) {
    progress.arcHistory.push({ arcId: plan.arcId, completedAt: new Date().toISOString() });
    recordEvent("arc-complete", { arcId: plan.arcId });
    saveProgress();
  }
}

function activePlanWeek(plan) {
  return plan.weeks.find((entry) => entry.status === "active") || null;
}

function selectActiveArcWeek(arc) {
  const plan = progress.arcPlans[arc.id];
  syncArcPlan(plan);
  return activePlanWeek(plan) || [...plan.weeks].reverse().find((entry) => entry.status === "complete") || plan.weeks[0];
}

function starterArc() {
  const done = completedArcIds();
  return allArcChoices().find((item) => item.pantheon === progress.activePantheon && arcIsUnlocked(item, done))
    || allArcChoices().find((item) => arcIsUnlocked(item, done));
}

function ensureArcPlan() {
  if (!progress.arcChoice) {
    const starter = starterArc();
    progress.arcChoice = starter?.id || null;
  }
  const arc = allArcChoices().find((item) => item.id === progress.arcChoice);
  const plan = arc && progress.arcPlans[arc.id];
  const explicitWeeks = arc?.programmeWeeks || [];
  const staleExplicitPlan = Boolean(
    plan && explicitWeeks.length && (plan.weeks.length !== explicitWeeks.length || plan.weeks.some((entry, index) =>
      entry.weekId !== explicitWeeks[index]?.weekId ||
      entry.weekPath !== explicitWeeks[index]?.weekPath
    ))
  );
  if (plan) migratePlan(plan, progress);
  if (arc && (!plan || !plan.weeks?.[0]?.weekPath || staleExplicitPlan)) {
    const replacement = createArcPlan(arc);
    progress.arcPlans[arc.id] = plan ? { ...replacement, ...plan, weeks: replacement.weeks } : replacement;
  }
  if (arc) {
    const current = progress.arcPlans[arc.id];
    migratePlan(current, progress);
    current.weeks.forEach((entry, index) => {
      entry.assessment = weekModules().find((item) => item.id === entry.weekId)?.assessment || explicitWeeks[index]?.assessment || null;
      entry.lessonVersions = Object.fromEntries((entry.lessonIds || []).map((id) => [id, contentIndex.lessons.find((item) => item.id === id)?.version || 1]));
    });
    saveProgress();
  }
}

function completedArcIds() {
  return new Set(progress.arcHistory.map((item) => item.arcId));
}

function generatedArcChoices() {
  if (!contentIndex || completedArcIds().size < (contentIndex.arcChoices?.length || 0) + (contentIndex.arcs?.length || 0)) return [];
  const themes = [
    ["arc.generated.tricksters", "New Threads: Tricksters and Transformations", "A generated curriculum following clever figures, shapeshifters, and changes of form."],
    ["arc.generated.boundaries", "New Threads: Boundaries and Otherworlds", "A generated curriculum following death, journeys, and dangerous crossings."],
    ["arc.generated.order", "New Threads: Duty and Cosmic Order", "A generated curriculum following law, kingship, fate, and balance."]
  ];
  const generation = Math.floor([...completedArcIds()].filter((id) => id.startsWith('arc.generated.')).length / themes.length) + 1;
  return themes.map(([id, title, description]) => ({ id: `${id}.run-${generation}`, title: `${title} · revision set ${generation}`, description: `${description} Reuses existing modules; this is revision, not newly authored content.`, scope: "generated", status: "active", weeks: ["Origins", "Heroes", "Gods", "Cunning", "Journeys", "Death", "Renewal", "Synthesis"] }));
}

function arcIsUnlocked(arc, done = completedArcIds()) {
  if (!arc) return false;
  const required = arc.prerequisiteArcIds || [];
  const minimum = arc.minimumCompletedArcs || 0;
  return done.size >= minimum && required.every((id) => done.has(id));
}

function arcUnlockText(arc, done = completedArcIds()) {
  if (!arc) return "Programme unavailable";
  const missing = (arc.prerequisiteArcIds || []).filter((id) => !done.has(id))
    .map((id) => allArcChoices().find((item) => item.id === id)?.title || id);
  const remaining = Math.max(0, (arc.minimumCompletedArcs || 0) - done.size);
  const parts = [];
  if (missing.length) parts.push(`Complete ${missing.join(" and ")} first`);
  if (remaining) parts.push(`Complete ${remaining} more programme${remaining === 1 ? "" : "s"} first`);
  return parts.join(" · ");
}

function recommendedArcChoices() {
  const done = completedArcIds();
  const previous = allArcChoices().find((item) => item.id === progress.arcChoice);
  const pool = allArcChoices().filter((item) => item.id !== progress.arcChoice && !done.has(item.id) && arcIsUnlocked(item, done));
  const scored = pool.map((arc) => ({
    arc,
    score: topicAffinity(`${arc.title} ${arc.description || ""} ${(arc.weeks || []).map(arcWeekTitle).join(" ")}`)
      + (arc.scope === "cross-pantheon" || arc.scope === "generated" ? 3 : 0)
      + (previous?.pantheon && arc.pantheon && arc.pantheon !== previous.pantheon ? 1 : 0)
  })).sort((a, b) => b.score - a.score);
  return scored.slice(0, 3).map((item) => item.arc);
}

function arcChoiceIsDue() {
  const arc = allArcChoices().find((item) => item.id === progress.arcChoice);
  const plan = arc && progress.arcPlans[arc.id];
  if (!arc || !plan) return true;
  syncArcPlan(plan);
  return plan.status === "complete" && plan.weeks.at(-1).completedOn < localDate();
}

function renderPantheonSection() {
  const filters = ["all", "pantheon", "myth-cycle", "folklore", "regional-tradition", "living-tradition"];
  const selected = runtime.traditionFilter || "all";
  const items = Object.values(registry.pantheons).filter((item) => selected === "all" || item.coverageType === selected);
  const filterButtons = filters.map((filter) => `<button class="filter-chip ${filter === selected ? "active" : ""}" type="button" data-action="set-tradition-filter" data-filter="${filter}">${filter === "all" ? "All" : filter.replace("-", " ")}</button>`).join("");
  const rows = items.map((item) => {
    const active = item.id === pantheonConfig.id;
    const available = item.status === "active";
    const lessonCount = contentIndex.lessons?.filter((lessonItem) => lessonItem.pantheon === item.id).length || 0;
    const sourceCount = contentIndex.sources?.filter((source) => source.pantheon === item.id).length || 0;
    const pantheonArc = allArcChoices().find((arc) => arc.pantheon === item.id);
    const locked = available && pantheonArc && !arcIsUnlocked(pantheonArc);
    const statusText = !available ? "Planned" : locked ? `Programme locked · ${arcUnlockText(pantheonArc)}` : active ? "Active tradition" : "Available";
    return `<button class="week-day" type="button" data-action="choose-pantheon" data-pantheon-id="${escapeHtml(item.id)}" ${available ? "" : "disabled"} ${active ? 'aria-current="true"' : ""}>
      <span class="day-number">${active ? "✓" : locked ? "•" : "+"}</span>
      <span><strong>${escapeHtml(item.name)}</strong><small>${statusText} · ${escapeHtml(item.coverageType || "tradition")} · ${lessonCount} lessons · ${sourceCount} sources</small></span>
      <span class="day-status">${active ? "●" : locked ? "•" : "›"}</span>
    </button>`;
  }).join("");
  return `<section class="week-card"><p class="eyebrow">Tradition library</p><div class="filter-row">${filterButtons}</div><div class="week-days">${rows}</div></section>`;
}
function renderArcSection() {
  const chosen = allArcChoices().find((arc) => arc.id === progress.arcChoice);
  if (!chosen) return "";
  const gateNotice = runtimeNotice ? `<p class="status-line">${escapeHtml(runtimeNotice)}</p>` : "";
  const plan = progress.arcPlans[chosen.id] || (progress.arcPlans[chosen.id] = createArcPlan(chosen));
  syncArcPlan(plan);
  if (arcChoiceIsDue()) {
    const stats = programmeStats(plan);
    const recommendations = recommendedArcChoices();
    const recommendationText = recommendations.length ? `${recommendations.length} unlocked option${recommendations.length === 1 ? '' : 's'} selected from eligible programmes.` : 'No further eligible programmes are available yet. You can continue Memory practice while new material is authored.';
    const weakText = stats.weakTopics.length ? `Topics to revisit: ${stats.weakTopics.slice(0, 5).join(', ')}.` : 'No weak topics recorded in this programme.';
    const choices = recommendations.map((arc)=>`<button class="topic-button" type="button" data-action="choose-arc" data-arc-id="${escapeHtml(arc.id)}"><strong>${escapeHtml(arc.title)}</strong><span>${escapeHtml(arc.description || "")}</span></button>`).join("");
    const locked = allArcChoices().filter((arc) => !completedArcIds().has(arc.id) && !arcIsUnlocked(arc))
      .slice(0, 3)
      .map((arc) => `<div class="prompt-button"><strong>${escapeHtml(arc.title)}</strong><span>${escapeHtml(arcUnlockText(arc))}</span></div>`).join("");
    return `<section class="week-card"><p class="eyebrow">Programme complete</p><h2>${escapeHtml(chosen.title)}</h2><p class="status-line">Your eight-module run is complete. ${escapeHtml(recommendationText)} ${escapeHtml(weakText)}</p><div class="stat-grid" aria-label="Programme results"><div class="stat-card"><h2>Weeks</h2><strong>${plan.weeks.filter((item)=>item.status==="complete").length}/8</strong></div><div class="stat-card"><h2>Lessons</h2><strong>${stats.lessons}</strong></div><div class="stat-card"><h2>Recall</h2><strong>${stats.accuracy}%</strong></div><div class="stat-card"><h2>Review</h2><strong>${stats.weakOutcomes}</strong></div></div><div class="topic-list">${choices}</div>${locked ? `<p class="eyebrow">Coming next</p><div class="topic-list">${locked}</div>` : ""}</section>`;
  }
  const current = plan.weeks.find((item) => item.status === "active") || plan.weeks.at(-1);
  const next = plan.weeks.find((item) => item.status === "planned" && item.unlocksOn);
  const completeCount = plan.weeks.filter((item) => item.status === "complete").length;
  return `<section class="week-card"><div class="week-card-header"><div><p class="eyebrow">Current programme</p><h2>${escapeHtml(chosen.title)}</h2></div><strong>${Math.min(completeCount + 1, 8)}/8</strong></div>${gateNotice}<p class="status-line">${escapeHtml(chosen.description)}</p><div class="progress-track"><div class="progress-fill" style="width:${(completeCount / plan.weeks.length) * 100}%"></div></div><p class="status-line">Week ${current.week}: ${escapeHtml(current.title)}${next ? ` · Next week unlocks ${escapeHtml(next.unlocksOn)}` : ""}</p></section>`;
}

function renderTopic() {
  const topic = topicLibrary.get(runtime.topicId);
  if (!topic) return renderHome();
  recordEvent("topic-open", { topicId: runtime.topicId });
  saveProgress();
  const cards = topic.cards || [{ title: "Overview", body: topic.body, recordIds: topic.recordIds }];
  app.innerHTML = `<section class="result-card"><p class="hero-kicker">Rabbit hole</p><h1>${escapeHtml(topic.title)}</h1><p class="subtitle">Follow a source-linked reading path, then choose where to go next.</p>${cards.map((card,index)=>`<article class="rabbit-card"><p class="eyebrow">Read ${index+1}/${cards.length}</p><h2>${escapeHtml(card.title)}</h2><p>${escapeHtml(card.body)}</p><div class="source-list">${renderRecordButtons(card.recordIds || topic.recordIds)}</div></article>`).join("")}<section class="suggested-panel"><p class="eyebrow">Go deeper</p><div class="topic-list">${topic.nextTopicIds.map((id)=>renderTopicButton({id,title:topicLibrary.get(id)?.title || id,description:`${pantheonName(topicLibrary.get(id)?.pantheon)} · Keep following this thread.`})).join("")}</div></section><div class="continue-panel"><button class="secondary-button" data-action="home" type="button">Home</button><button class="primary-button" data-action="start-review" type="button">Memory practice</button></div></section>`;
}

function nextAvailableDay(target) {
  const currentDay = week.days.find((day) => day.lessonId === target.id)?.day || 0;
  return week.days.find((day) => day.day > currentDay && day.lessonId && lessons.has(day.lessonId) && isDayUnlocked(day));
}

function suggestedTopicsFor(target) {
  const seen = new Set();
  const local = week.suggestedTopics || [];
  const global = [...topicLibrary.entries()].map(([id, item]) => ({
    id,
    title: item.title,
    description: item.body,
    score: topicAffinity(`${item.title} ${item.body}`)
  })).filter((item) => !local.some((topic) => topic.id === item.id))
    .sort((a, b) => b.score - a.score).slice(0, 3);
  return [...local, ...global].filter((topic) => {
    if (seen.has(topic.id)) return false;
    seen.add(topic.id);
    return true;
  });
}

function renderTopicButton(topic) {
  return `
    <button class="topic-button" type="button" data-action="open-topic" data-topic-id="${escapeHtml(topic.id)}">
      <strong>${escapeHtml(topic.title)}</strong>
      <span>${escapeHtml(topic.description)}</span>
    </button>
  `;
}

function renderReviewComplete() {
  const total = runtime.reviewQuestions.length;
  const correct = runtime.reviewQuestions.filter((item) => {
    const answer = runtime.answers[reviewAnswerKey(item)];
    return answer?.choiceId === item.question.answerId;
  }).length;

  app.innerHTML = `
    <section class="result-card" aria-labelledby="reviewCompleteTitle">
      <p class="hero-kicker">${runtime.reviewMode === "assessment" ? "Weekly assessment" : "Practice complete"}</p>
      <h1 id="reviewCompleteTitle">${correct}/${total} correct</h1>
      <p class="subtitle">${runtime.reviewMode === "assessment" ? "The module is complete once every day and the assessment are done. The next programme week unlocks tomorrow." : "Practice uses questions from every completed lesson. Incorrect topics are now marked for later practice."}</p>
      <div class="continue-panel">
        <button class="secondary-button" type="button" data-action="home">Home</button>
        <button class="primary-button" type="button" data-action="${runtime.reviewMode === "assessment" ? "start-week-assessment" : "start-review"}">${runtime.reviewMode === "assessment" ? "Retake assessment" : "Practice again"}</button>
      </div>
    </section>
  `;
}


async function ensureRetrieval(pantheonId) {
  const target = pantheonId || "shared";
  if (retrievalIndex?.loaded?.has(target)) return retrievalIndex;
  const response = await fetch(RETRIEVAL_URL);
  if (!response.ok) throw new Error("The local retrieval index has not been generated. Run python -B tools/content_pipeline.py to build it.");
  const manifest = await response.json();
  if (!retrievalIndex) {
    const byId = new Map((manifest.sources || []).map((source) => [source.id, source]));
    retrievalIndex = { sources: manifest.sources || [], byId, chunks: [], loaded: new Set() };
  }
  const wanted = target === "shared" ? (manifest.files || []) : (manifest.files || []).filter((entry) => entry.pantheon === target);
  for (const entry of wanted) {
    if (retrievalIndex.loaded.has(entry.pantheon)) continue;
    const file = await fetch(`./${entry.path}`);
    if (!file.ok) continue;
    const payload = await file.json();
    for (const chunk of payload.chunks || []) {
      retrievalIndex.chunks.push({
        evidenceType: "source-text",
        // terms are recomputed from text; the generated files dropped them
        // because they doubled every payload.
        terms: (chunk.text.toLowerCase().match(/[a-z0-9][a-z0-9'-]+/g) || []),
        ...retrievalIndex.byId.get(chunk.recordId),
        ...chunk,
      });
    }
    retrievalIndex.loaded.add(entry.pantheon);
  }
  retrievalIndex.loaded.add(target);
  return retrievalIndex;
}

function assistantTokens(query) {
  const stop = new Set(["the","and","what","who","why","how","is","are","was","were","of","in","to","a","an","on","for","did","does","about","tell","me"]);
  return (query.toLowerCase().match(/[a-z0-9][a-z0-9'-]+/g) || []).filter((item) => !stop.has(item));
}

function searchRetrieval(query) {
  if (!retrievalIndex) return { error: "The local retrieval index is still loading; try again in a moment.", results: [] };
  const tokens = assistantTokens(query);
  if (!tokens.length) return { error: "Enter a question with a searchable topic, name, or theme.", results: [] };
  const results = retrievalIndex.chunks.filter((chunk) => chunk.evidenceType !== 'editorial-note' && (pantheonConfig?.id === 'shared' || chunk.pantheon === pantheonConfig?.id)).map((chunk) => {
    const terms = new Set(chunk.terms);
    const text = chunk.text.toLowerCase();
    const score = tokens.reduce((sum, token) => sum + (terms.has(token) ? 2 : 0) + (text.includes(token) ? 1 : 0), 0)
      + (chunk.title.toLowerCase().includes(tokens.join(" ")) ? 4 : 0);
    return { chunk, score };
  }).filter((item) => item.score > 0).sort((a,b)=>b.score-a.score).slice(0,6);
  if (!results.length) return { error: "Not covered by the local corpus yet. Try a named figure, theme, or tradition already in the library.", results: [] };
  return { error: null, results };
}

function renderAssistant() {
  const response = runtime.assistantResponse;
  app.innerHTML = `<section class="result-card" aria-labelledby="assistantTitle"><p class="hero-kicker">Corpus-only researcher</p><h1 id="assistantTitle">Ask the local sources</h1><p class="subtitle">Search the selected tradition’s local sources. A configured model can select verbatim quotations, not synthesize a verified answer. Passage relevance and interpretation still require judgement.</p><label class="assistant-label" for="assistantQuery">Question</label><textarea id="assistantQuery" class="assistant-input" placeholder="Example: How does Gilgamesh confront death?">${escapeHtml(runtime.assistantQuery)}</textarea><div class="bottom-actions"><button class="secondary-button" type="button" data-action="home">Home</button><button class="primary-button" type="button" data-action="run-assistant">Ask</button></div>${runtime.assistantError ? `<p class="status-line">${escapeHtml(runtime.assistantError)}</p>` : ""}${response ? `<article class="rabbit-card"><p class="eyebrow">${escapeHtml(response.mode)} · ${escapeHtml(response.coverage)}</p><h2>Source evidence</h2><p>${escapeHtml(response.answer)}</p>${response.citations?.length ? `<div class="tag-grid">${response.citations.map((item)=>`<span class="tag-chip">${escapeHtml(item.claim)} · ${escapeHtml(item.chunkId)}</span>`).join("")}</div>`:""}</article>`:""}${runtime.assistantResults.length ? `<section class="assistant-results" aria-label="Retrieved source passages">${runtime.assistantResults.map(({chunk,score},index)=>`<article class="rabbit-card"><p class="eyebrow">Evidence ${index+1} · ${escapeHtml(pantheonName(chunk.pantheon))} · ${escapeHtml(chunk.sourceType || "source")}${score?` · score ${score}`:""}</p><h2>${escapeHtml(chunk.locator)}</h2><p>${escapeHtml(chunk.text)}</p><div class="source-list"><button class="source-button assistant-citation" type="button" data-action="open-record" data-record-id="${escapeHtml(chunk.recordId)}">Open cited source: ${escapeHtml(chunk.title)}</button></div></article>`).join("")}</section>` : ""}</section>`;
  document.querySelector("#assistantQuery")?.focus();
}

function navigateCard(direction, isLast = runtime.cardIndex === activeLesson().narrativeBlocks.length - 1) {
  const next = runtime.cardIndex + direction;
  if (next < 0) return;
  if (next >= activeLesson().narrativeBlocks.length) {
    runtime.view = "quiz";
    runtime.quizIndex = 0;
  } else if (direction > 0 && isLast) {
    runtime.view = "quiz";
    runtime.quizIndex = 0;
  } else {
    runtime.cardIndex = next;
  }
  render();
}

function startLesson(lessonId) {
  const target = lessons.get(lessonId) || lesson;
  if (!isLessonUnlocked(target)) return renderHome();
  lesson = target;
  runtime = createRuntime();
  runtime.activeLessonId = target.id;
  runtime.view = "cards";
  runtime.cardIndex = 0;
  render();
}

function startReview() {
  runtime.reviewMode = "practice";
  runtime.reviewQuestions = getReviewQuestions();
  if (!runtime.reviewQuestions.length) return;
  runtime.view = "review";
  runtime.reviewIndex = 0;
  runtime.answers = {};
  recordEvent("review-start", { questionCount: runtime.reviewQuestions.length });
  saveProgress();
  render();
}

function startWeekAssessment() {
  if (!isWeekComplete() || !week.assessment) return;
  runtime.reviewMode = "assessment";
  runtime.reviewQuestions = getWeekAssessmentQuestions();
  if (!runtime.reviewQuestions.length) return;
  runtime.reviewIndex = 0;
  runtime.answers = {};
  runtime.view = "review";
  recordEvent("week-assessment-start", { weekId: week.id, questionCount: runtime.reviewQuestions.length });
  saveProgress();
  render();
}

function openSource(refId, lessonId) {
  const context = lessonLibrary.get(lessonId) || activeLesson();
  const source = context?.sourceReferences[refId];
  if (!source) return;
  recordSourceOpen(refId, context);
  showSourceDialog({
    title: `${source.work} · ${source.locator}`,
    excerpt: source.excerpt,
    evidenceType: source.evidenceType,
    evidenceQuote: source.evidenceQuote,
    meta: [
      ["Author", source.author],
      ["Translator", source.translator],
      ["Source type", recordLibrary.get(source.recordId)?.sourceType],
      ["Source ID", source.sourceId],
      ["Record", source.recordId],
      ["Rights", recordLibrary.get(source.recordId)?.rightsStatus],
      ["Note", source.note]
    ],
    localPath: source.localPath
  });
  renderTopbar();
}

function pantheonName(id) {
  return registry?.pantheons?.[id]?.name || id || "Shared";
}

function openRecord(recordId) {
  const record = recordLibrary.get(recordId);
  if (!record || !record.available) return;
  recordSourceOpen(recordId, activeLesson());
  showSourceDialog({
    title: record.title,
    excerpt: "Open the local source file to inspect the cited work and provenance.",
    meta: [
      ["Ancient author", record.ancientAuthors?.join(", ")],
      ["Author", record.authors?.join(", ")],
      ["Translator", record.translator],
      ["Source type", record.sourceType],
      ["Source IDs", record.sourceIds?.join(", ")],
      ["Record", record.id],
      ["Rights", record.rightsStatus]
    ],
    localPath: record.corpusPath
  });
}

function showSourceDialog({ title, excerpt, evidenceType, evidenceQuote, meta, localPath }) {
  document.querySelector("#sourceTitle").textContent = title;
  document.querySelector('#sourceEvidenceLabel').textContent = evidenceType === 'quotation' ? 'Source quotation (translated where applicable)' : evidenceType === 'paraphrase' ? 'Lesson author’s paraphrase — not a quotation' : 'Unverified source summary — inspect the local text';
  document.querySelector("#sourceExcerpt").textContent = excerpt;
  const quote = document.querySelector('#sourceEvidenceQuote');
  quote.hidden = !evidenceQuote;
  quote.textContent = evidenceQuote ? `Supporting quotation: ${evidenceQuote}` : '';
  document.querySelector("#sourceMeta").innerHTML = meta
    .filter(([, value]) => value)
    .map(([key, value]) => `<div><dt>${escapeHtml(key)}</dt><dd>${escapeHtml(value)}</dd></div>`)
    .join("");
  document.querySelector("#sourceLocalLink").href = `./${localPath}`;
  sourceDialog.showModal();
}

function openDeepDive(questionId, lessonId) {
  const context = lessonLibrary.get(lessonId) || activeLesson();
  const reviewItem = runtime.view === 'review' ? runtime.reviewQuestions[runtime.reviewIndex] : null;
  const question = reviewItem?.lesson.id === lessonId && reviewItem.question.id === questionId ? reviewItem.question : context?.quiz.find((item) => item.id === questionId);
  if (!question) return;
  const deepDive = question.deepDive || {
    prompt: `Explore: ${question.prompt}`,
    suggestedQuestions: ['Which words in the cited passage support the answer?', 'What changes if we distinguish the source narrative from the lesson’s interpretation?'],
    sourceRefIds: question.sourceRefIds
  };
  document.querySelector("#deepDiveTitle").textContent = deepDive.prompt;
  runtime.assistantSeed = question.prompt;
  document.querySelector("#deepDiveIntro").textContent = "Use these prompts with the cited passages, or ask the local corpus researcher.";
  document.querySelector("#deepDiveQuestions").innerHTML = deepDive.suggestedQuestions
    .map((prompt) => `<div class="prompt-button" role="note">${escapeHtml(prompt)}</div>`)
    .join("");
  document.querySelector("#deepDiveSources").innerHTML = renderSourceButtons(deepDive.sourceRefIds, context);
  deepDiveDialog.showModal();
}

function openTopic(topicId) {
  runtime.topicId = topicId;
  runtime.view = "topic";
  render();
}

function handleAction(action, target) {
  if (action === "home") {
    runtime = createRuntime();
    runtime.activeLessonId = lesson?.id || null;
    render();
  }
  if (action === "start-lesson" || action === "select-lesson") {
    startLesson(target.dataset.lessonId);
  }
  if (action === "start-review") {
    startReview();
  }
  if (action === "start-week-assessment") {
    startWeekAssessment();
  }
  if (action === "previous-card") {
    navigateCard(-1);
  }
  if (action === "next-card") {
    navigateCard(1);
  }
  if (action === "back-to-cards") {
    runtime.view = "cards";
    runtime.cardIndex = activeLesson().narrativeBlocks.length - 1;
    render();
  }
  if (action === "answer-question") {
    const context = activeLesson();
    const question = context.quiz[runtime.quizIndex];
    const choiceId = target.dataset.choiceId;
    runtime.answers[question.id] = { choiceId, at: new Date().toISOString() };
    render();
  }
  if (action === "answer-review") {
    const item = runtime.reviewQuestions[runtime.reviewIndex];
    const choiceId = target.dataset.choiceId;
    runtime.answers[reviewAnswerKey(item)] = { choiceId, at: new Date().toISOString() };
    recordAnswer(item.question, choiceId, item.lesson);
    render();
  }
  if (action === "next-question") {
    const context = activeLesson();
    const isLast = runtime.quizIndex === context.quiz.length - 1;
    if (isLast) {
      runtime.view = "scratch";
    } else {
      runtime.quizIndex += 1;
    }
    render();
  }
  if (action === "back-to-quiz") {
    runtime.view = "quiz";
    runtime.quizIndex = activeLesson().quiz.length - 1;
    render();
  }
  if (action === "reveal-results") {
    revealResults();
  }
  if (action === "next-review") {
    const isLast = runtime.reviewIndex === runtime.reviewQuestions.length - 1;
    if (isLast) {
      const correct = runtime.reviewQuestions.filter((item) =>
        runtime.answers[reviewAnswerKey(item)]?.choiceId === item.question.answerId
      ).length;
      if (runtime.reviewMode === "assessment") {
        const state = currentWeekState();
        finishAssessment(state, correct, runtime.reviewQuestions.length, new Date().toISOString(), assessmentKey(week.assessment));
        recordEvent("week-assessment-complete", { weekId: week.id, correct, total: runtime.reviewQuestions.length });
        if (progress.arcPlans[progress.arcChoice]) syncArcPlan(progress.arcPlans[progress.arcChoice]);
      } else {
        recordEvent("review-complete", { questionCount: runtime.reviewQuestions.length });
      }
      saveProgress();
      runtime.view = "review-complete";
    } else {
      runtime.reviewIndex += 1;
    }
    render();
  }
  if (action === "retake-lesson") {
    startLesson(runtime.activeLessonId);
  }
  if (action === "open-source") {
    if (deepDiveDialog.open) deepDiveDialog.close();
    if (topicDialog.open) topicDialog.close();
    openSource(target.dataset.sourceId, target.dataset.lessonId);
  }
  if (action === "open-first-source") {
    openSource(Object.keys(lesson.sourceReferences)[0], lesson.id);
  }
  if (action === "open-deep-dive") {
    openDeepDive(target.dataset.questionId, target.dataset.lessonId);
  }
  if (action === "choose-arc") {
    const arc = allArcChoices().find((item) => item.id === target.dataset.arcId);
    if (!arcIsUnlocked(arc)) {
      runtimeNotice = arcUnlockText(arc);
      renderHome();
      return;
    }
    runtimeNotice = null;
    progress.arcChoice = target.dataset.arcId;
    if (arc?.pantheon && progress.activePantheon !== arc.pantheon) {
      progress.activePantheon = arc.pantheon;
    }
    progress.arcPlans[arc.id] = createArcPlan(arc);
    recordEvent("arc-choice", { arcId: progress.arcChoice, generated: arc?.scope === "generated" });
    saveProgress();
    loadContent().then(render);
  }
  if (action === "choose-pantheon") {
    const item = registry.pantheons[target.dataset.pantheonId];
    if (!item || item.status !== "active" || !item.paths?.activeWeek) return;
    const pantheonArc = allArcChoices().find((arc) => arc.pantheon === item.id);
    if (pantheonArc && arcIsUnlocked(pantheonArc)) {
      runtimeNotice = null;
      progress.activePantheon = item.id;
      progress.arcChoice = pantheonArc.id;
      progress.arcPlans[pantheonArc.id] ||= createArcPlan(pantheonArc);
    } else if (pantheonArc) {
      runtimeNotice = `${item.name} programme locked: ${arcUnlockText(pantheonArc)}`;
      recordEvent("pantheon-choice", { pantheonId: item.id, lockedArcId: pantheonArc.id });
      saveProgress();
      renderHome();
      return;
    }
    recordEvent("pantheon-choice", { pantheonId: item.id, arcId: progress.arcChoice });
    saveProgress();
    loadContent().then(render);
  }
  if (action === "open-topic") {
    openTopic(target.dataset.topicId);
  }
  if (action === "open-record") {
    openRecord(target.dataset.recordId);
  }
  if (action === "set-tradition-filter") {
    runtime.traditionFilter = target.dataset.filter;
    render();
  }
  if (action === "open-assistant" || action === "assistant-from-deep-dive") {
    if (deepDiveDialog.open) deepDiveDialog.close();
    runtime.assistantQuery = runtime.assistantSeed || runtime.assistantQuery;
    runtime.view = "assistant";
    runtime.assistantError = null;
    render();
    ensureRetrieval(pantheonConfig?.id).catch((error) => {
      runtime.assistantError = error.message;
      render();
    });
  }
  if (action === "run-assistant") {
    runtime.assistantQuery = document.querySelector("#assistantQuery")?.value.trim() || "";
    runtime.assistantError = null;
    runtime.assistantResponse = null;
    fetch("./api/assistant", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: runtime.assistantQuery, tradition: pantheonConfig?.id, lessonId: runtime.activeLessonId })
    }).then(async (response) => {
      if (!response.ok) throw new Error(`Assistant API unavailable (${response.status}).`);
      const result = await response.json();
      runtime.assistantResponse = result;
      runtime.assistantResults = (result.evidence || []).map((chunk) => ({ chunk, score: null }));
      runtime.assistantError = result.warning || null;
      recordEvent("assistant-query", { query: runtime.assistantQuery, resultCount: result.evidence?.length || 0, mode: result.mode });
      saveProgress();
      render();
    }).catch(() => {
      ensureRetrieval().then(() => {
        const found = searchRetrieval(runtime.assistantQuery);
        runtime.assistantResults = found.results;
        runtime.assistantError = found.error;
        recordEvent("assistant-query", { query: runtime.assistantQuery, resultCount: found.results.length, mode: "local-retrieval" });
        saveProgress();
        render();
      }).catch((error) => { runtime.assistantError = error.message; render(); });
    });
    render();
  }

  if (action === "set-rating") {
    runtime.feedback.rating = target.dataset.rating;
    runtime.feedback.submitted = false;
    render();
  }
  if (action === "toggle-feedback-tag") {
    const tag = target.dataset.tag;
    runtime.feedback.tags.has(tag)
      ? runtime.feedback.tags.delete(tag)
      : runtime.feedback.tags.add(tag);
    runtime.feedback.submitted = false;
    render();
  }
  if (action === "submit-feedback") {
    submitFeedback();
    render();
  }
}

document.addEventListener("click", (event) => {
  const target = event.target.closest("[data-action]");
  if (!target) return;
  handleAction(target.dataset.action, target);
});

document.addEventListener("input", (event) => {
  if (event.target.id === "feedbackText") {
    runtime.feedback.text = event.target.value;
    runtime.feedback.submitted = false;
  }
});

document.querySelector("#homeButton").addEventListener("click", () => {
  if (!lesson) return;
  runtime = createRuntime();
  runtime.activeLessonId = lesson.id;
  render();
});

document.querySelector("#closeSourceDialog").addEventListener("click", () => sourceDialog.close());
document.querySelector("#closeDeepDiveDialog").addEventListener("click", () => deepDiveDialog.close());
document.querySelector("#closeTopicDialog").addEventListener("click", () => topicDialog.close());

async function refreshCalendar() {
  // Never interrupt an in-flight lesson. Resume scheduling when the learner returns Home.
  if (refreshingCalendar || runtime.view !== 'home' || displayedDay === localDate()) return;
  refreshingCalendar = true;
  try {
    await loadContent();
    displayedDay = localDate();
    render();
  } catch (error) {
    runtimeNotice = `Could not refresh the new day: ${error.message}`;
    render();
  } finally {
    refreshingCalendar = false;
  }
}

function scheduleMidnight() {
  const next = new Date();
  next.setHours(24, 0, 0, 50);
  setTimeout(() => { refreshCalendar(); scheduleMidnight(); }, Math.max(100, next.getTime() - Date.now()));
}
window.addEventListener('focus', refreshCalendar);
document.addEventListener('visibilitychange', () => { if (!document.hidden) refreshCalendar(); });
setInterval(refreshCalendar, 30000);
scheduleMidnight();

loadContent()
  .then(render)
  .catch((error) => {
    console.error(error);
    app.innerHTML = `
      <section class="result-card">
        <p class="hero-kicker">Prototype error</p>
        <h1>Lesson unavailable.</h1>
        <p class="subtitle">${escapeHtml(error.message)}</p>
        <p class="status-line">Serve this folder over HTTP, for example: <code>python -m http.server 4873</code>, then open <code>http://localhost:4173/</code>.</p>
      </section>
    `;
  });
