// Calendar math uses date components, never elapsed local-midnight hours (DST days are not 24h).
export function calendarDays(start, end) {
  const ordinal = (value) => Date.UTC(...value.split("-").map((n, i) => Number(n) - (i === 1 ? 1 : 0))) / 86400000;
  return Math.max(0, ordinal(end) - ordinal(start));
}

export function localDay(iso) {
  const date = new Date(iso);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
}

export function runWeek(plan, weekId) {
  plan.weekStates ||= {};
  return plan.weekStates[weekId] ||= { startedAt: null, lessons: {}, assessment: null };
}

export function completionDate(entry, plan) {
  const state = runWeek(plan, entry.weekId);
  if (!entry.lessonIds?.length) return null;
  const dates = entry.lessonIds.map((id) => state.lessons[id]?.completedAt);
  if (dates.some((date) => !date || !Number.isFinite(Date.parse(date)) || Date.parse(date) < Date.parse(plan.createdAt))) return null;
  if (entry.lessonIds.some((id) => (state.lessons[id]?.contentVersion || 1) < (entry.lessonVersions?.[id] || 1))) return null;
  if (entry.assessment) {
    if (!state.assessment?.completedAt || Date.parse(state.assessment.completedAt) < Date.parse(plan.createdAt)) return null;
    if (entry.assessment.questions && state.assessment.contentKey !== assessmentKey(entry.assessment)) return null;
    dates.push(state.assessment.completedAt);
  }
  return dates.map(localDay).sort().at(-1);
}

export function assessmentKey(assessment) {
  // This is a version key, not a cryptographic integrity check.
  const text = JSON.stringify(assessment?.questions || []);
  let hash = 2166136261;
  for (const char of text) hash = Math.imul(hash ^ char.charCodeAt(0), 16777619);
  return (hash >>> 0).toString(16);
}

export function finishAssessment(state, correct, total, now, contentKey = null) {
  // Retakes are practice; they must never move the first completion/unlock date.
  const old = state.assessment?.contentKey === contentKey ? state.assessment : null;
  state.assessment = {
    completedAt: old?.completedAt || now,
    attempts: (old?.attempts || 0) + 1,
    correct, total, contentKey, lastAttemptAt: now,
    history: [...(old?.history || []), { at: now, correct, total }]
  };
  return state.assessment;
}

export function migratePlan(plan, progress) {
  if (plan.progressVersion === 2) return;
  plan.runId ||= `legacy:${plan.arcId}:${plan.createdAt}`;
  plan.weekStates = {};
  const since = Date.parse(plan.createdAt);
  // Preserve only evidence from this run. Global module state is not proof of a fresh completion.
  for (const entry of plan.weeks) {
    const state = runWeek(plan, entry.weekId);
    const old = progress.weeks[entry.weekId];
    if (old?.startedAt && Date.parse(old.startedAt) >= since) state.startedAt = old.startedAt;
    for (const id of entry.lessonIds || []) {
      const lesson = progress.lessons[id];
      if (lesson?.completedAt && Date.parse(lesson.completedAt) >= since) {
        state.lessons[id] = { completedAt: lesson.completedAt, contentVersion: lesson.contentVersion, questions: { ...lesson.questions } };
      }
    }
    if (old?.assessment?.completedAt && Date.parse(old.assessment.completedAt) >= since && entry.lessonIds.every((id) => state.lessons[id])) {
      state.assessment = { ...old.assessment, history: [] };
    }
  }
  plan.progressVersion = 2;
}
