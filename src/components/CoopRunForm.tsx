import { useState, type FormEvent } from 'react'
import { getCharacter } from '../characters'
import { normalizeTime } from '../lib/time'
import type { CoopRun, Player } from '../types'
import { CharacterSelect } from './CharacterSelect'
import { Modal } from './Modal'
import { toScore, validateStats, validScore } from '../lib/validation'
import { LevelTimeInputs } from './RunFields'

/** Flat form state for a co-op run; player ids come from the viewed pairing. */
export interface CoopDraft {
  id?: string
  loggedAt?: string
  charA?: string
  charB?: string
  scoreA?: number
  scoreB?: number
  level?: number
  time?: string
}

export const coopDraftOf = (r: CoopRun): CoopDraft => ({
  id: r.id,
  loggedAt: r.loggedAt,
  charA: r.players[0].char,
  charB: r.players[1].char,
  scoreA: r.players[0].score,
  scoreB: r.players[1].score,
  level: r.level,
  time: r.time,
})

interface Props {
  runs: CoopRun[] // already filtered to the current pairing
  a: Player
  b: Player
  initial: CoopDraft
  saving: boolean
  onSave: (run: CoopRun, isNew: boolean) => Promise<void>
  onDelete?: (id: string) => Promise<void>
  onClose: () => void
}

export function CoopRunForm({ runs, a, b, initial, saving, onSave, onDelete, onClose }: Props) {
  const editing = Boolean(initial.id)
  const [charA, setCharA] = useState(initial.charA ?? '')
  const [charB, setCharB] = useState(initial.charB ?? '')
  const [stats, setStats] = useState({ level: String(initial.level ?? ''), time: initial.time ?? '' })
  const [scoreA, setScoreA] = useState(String(initial.scoreA ?? ''))
  const [scoreB, setScoreB] = useState(String(initial.scoreB ?? ''))
  const [error, setError] = useState<string | null>(null)

  const clash = runs.find(
    (r) => r.players[0].char === charA && r.players[1].char === charB && r.id !== initial.id,
  )

  async function submit(e: FormEvent) {
    e.preventDefault()
    const problem =
      (!charA || !charB ? 'Pick both characters.' : null) ??
      (clash ? 'That pairing is already logged.' : null) ??
      validateStats(stats) ??
      (!validScore(scoreA) || !validScore(scoreB) ? 'Scores must be whole numbers.' : null)
    if (problem) return setError(problem)
    try {
      await onSave(
        {
          id: initial.id ?? crypto.randomUUID(),
          loggedAt: initial.loggedAt ?? new Date().toISOString().slice(0, 19),
          players: [
            { playerId: a.id, char: charA, score: toScore(scoreA) },
            { playerId: b.id, char: charB, score: toScore(scoreB) },
          ],
          level: Number(stats.level),
          time: normalizeTime(stats.time)!,
        },
        !editing,
      )
      onClose()
    } catch (err) {
      setError((err as Error).message)
    }
  }

  return (
    <Modal title={editing ? 'Edit co-op run' : 'Log co-op run'} onClose={onClose}>
      <form className="run-form" onSubmit={submit}>
        <label>
          {a.name}&rsquo;s character
          <CharacterSelect value={charA} onChange={setCharA} />
        </label>
        <label>
          {b.name}&rsquo;s character
          <CharacterSelect value={charB} onChange={setCharB} />
        </label>
        {clash && (
          <p className="form-warning">
            {getCharacter(charA).label} + {getCharacter(charB).label} is already logged (Lvl {clash.level}).
          </p>
        )}
        <LevelTimeInputs fields={stats} onChange={setStats} />
        <label>
          {a.name}&rsquo;s score
          <input inputMode="numeric" value={scoreA} onChange={(e) => setScoreA(e.target.value)} required />
        </label>
        <label>
          {b.name}&rsquo;s score
          <input inputMode="numeric" value={scoreB} onChange={(e) => setScoreB(e.target.value)} required />
        </label>
        {error && <p className="form-error">{error}</p>}
        <div className="form-actions">
          {editing && onDelete && (
            <button
              type="button"
              className="btn danger"
              disabled={saving}
              onClick={async () => {
                if (!confirm('Delete this run?')) return
                try {
                  await onDelete(initial.id!)
                  onClose()
                } catch (err) {
                  setError((err as Error).message)
                }
              }}
            >
              Delete
            </button>
          )}
          <span className="spacer" />
          <button type="button" className="btn ghost" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" className="btn primary" disabled={saving}>
            {saving ? 'Saving…' : 'Save run'}
          </button>
        </div>
      </form>
    </Modal>
  )
}
