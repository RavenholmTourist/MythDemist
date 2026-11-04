import type { CoopRun, Player, SoloRun, TrackerBackup } from '../types'

/** Serialize the full app state. Shared by JSON export and (later) Drive sync. */
export function buildBackup(players: Player[], coop: CoopRun[], solo: SoloRun[]): TrackerBackup {
  return {
    app: 'sor4-survival-tracker',
    version: 2,
    exportedAt: new Date().toISOString(),
    players,
    coop,
    solo,
  }
}

/** Validate a parsed JSON value as a TrackerBackup; null if it's not ours. */
export function parseBackup(value: unknown): TrackerBackup | null {
  const v = value as TrackerBackup | null
  if (
    v?.app === 'sor4-survival-tracker' &&
    Array.isArray(v.players) &&
    Array.isArray(v.coop) &&
    Array.isArray(v.solo)
  )
    return v
  return null
}

export function downloadJson(data: unknown, filename: string) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = filename
  a.click()
  URL.revokeObjectURL(a.href)
}
