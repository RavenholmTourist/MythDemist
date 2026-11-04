import { useState } from 'react'
import type { Player } from '../types'
import { MAX_PLAYERS, PLAYER_COLORS } from '../lib/usePlayers'
import { Modal } from './Modal'
import { PlayerFields, type PlayerDraft } from './PlayerFields'

interface Props {
  onSave: (players: Player[]) => Promise<void>
  onClose: () => void
}

const blank = (i: number): PlayerDraft => ({ name: '', color: PLAYER_COLORS[i % PLAYER_COLORS.length] })

export function Onboarding({ onSave, onClose }: Props) {
  const [drafts, setDrafts] = useState<PlayerDraft[]>([blank(0), blank(1)])
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const valid = drafts.filter((d) => d.name.trim())
  const names = new Set(valid.map((d) => d.name.trim().toLowerCase()))
  const dupe = names.size !== valid.length

  async function save() {
    if (!valid.length) return setError('Add at least one player.')
    if (dupe) return setError('Player names must be unique.')
    setSaving(true)
    try {
      await onSave(valid.map((d) => ({ id: crypto.randomUUID(), name: d.name.trim(), color: d.color })))
      onClose()
    } catch (e) {
      setError((e as Error).message)
      setSaving(false)
    }
  }

  return (
    <Modal title="Set up your players" onClose={onClose}>
      <p className="muted">
        Who's tracking runs here? Add 1–{MAX_PLAYERS} players — co-op needs at least two. You can change this
        later in Settings.
      </p>
      <div className="player-rows">
        {drafts.map((d, i) => (
          <PlayerFields
            key={i}
            value={d}
            autoFocus={i === 0}
            onChange={(v) => setDrafts(drafts.map((x, j) => (j === i ? v : x)))}
            onRemove={drafts.length > 1 ? () => setDrafts(drafts.filter((_, j) => j !== i)) : undefined}
          />
        ))}
      </div>
      {drafts.length < MAX_PLAYERS && (
        <button className="btn ghost small" onClick={() => setDrafts([...drafts, blank(drafts.length)])}>
          + Add another player
        </button>
      )}
      {error && <p className="form-error">{error}</p>}
      <div className="form-actions">
        <span className="spacer" />
        <button className="btn primary" disabled={saving || !valid.length || dupe} onClick={save}>
          {saving ? 'Saving…' : 'Start tracking'}
        </button>
      </div>
    </Modal>
  )
}
