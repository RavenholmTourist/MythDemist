import { useRef, useState } from 'react'
import { CHARACTERS } from '../characters'
import { usePortraits } from '../lib/portraits'
import { MAX_PLAYERS, PLAYER_COLORS, type PlayersStore } from '../lib/usePlayers'
import type { RunStore } from '../lib/useRunStore'
import type { CoopRun, LegacyCoopRun, LegacySoloRun, Player, SoloRun, TrackerBackup } from '../types'
import { CharacterSelect } from './CharacterSelect'
import { Modal } from './Modal'
import { PlayerFields, type PlayerDraft } from './PlayerFields'
import { Portrait } from './Portrait'

interface Props {
  playersStore: PlayersStore
  coop: RunStore<CoopRun>
  solo: RunStore<SoloRun>
}

type PendingImport =
  | { kind: 'backup'; data: TrackerBackup }
  | { kind: 'legacy-bundle'; coop: LegacyCoopRun[]; solo: LegacySoloRun[] }
  | { kind: 'legacy-coop'; runs: LegacyCoopRun[] }
  | { kind: 'legacy-solo'; runs: LegacySoloRun[] }

function mergeById<T extends { id: string }>(existing: T[], incoming: T[]): { merged: T[]; added: number } {
  const seen = new Set(existing.map((r) => r.id))
  const fresh = incoming.filter((r) => !seen.has(r.id))
  return { merged: [...existing, ...fresh], added: fresh.length }
}

function PlayerSelect({ players, value, onChange }: { players: Player[]; value: string; onChange: (id: string) => void }) {
  return (
    <select value={value} onChange={(e) => onChange(e.target.value)}>
      {players.map((p) => (
        <option key={p.id} value={p.id}>
          {p.name}
        </option>
      ))}
    </select>
  )
}

export function SettingsView({ playersStore, coop, solo }: Props) {
  const { players, save, saveAll, remove } = playersStore
  const { overrides, setOverride, removeOverride } = usePortraits()
  const [editing, setEditing] = useState<PlayerDraft & { id?: string } | null>(null)
  const [overrideChar, setOverrideChar] = useState('')
  const [status, setStatus] = useState<string | null>(null)
  const [pending, setPending] = useState<PendingImport | null>(null)
  const [mapA, setMapA] = useState('')
  const [mapB, setMapB] = useState('')
  const [mapSolo, setMapSolo] = useState('')
  const fileInput = useRef<HTMLInputElement>(null)
  const portraitInput = useRef<HTMLInputElement>(null)

  const list = players ?? []
  const coopRuns = coop.runs
  const soloRuns = solo.runs

  const refsOf = (id: string) =>
    coopRuns.filter((r) => r.players.some((s) => s.playerId === id)).length +
    soloRuns.filter((r) => r.playerId === id).length

  function exportData() {
    const backup: TrackerBackup = {
      app: 'sor4-survival-tracker',
      version: 2,
      exportedAt: new Date().toISOString(),
      players: list,
      coop: coopRuns,
      solo: soloRuns,
    }
    const blob = new Blob([JSON.stringify(backup, null, 2)], { type: 'application/json' })
    const a = document.createElement('a')
    a.href = URL.createObjectURL(blob)
    a.download = `sor4-tracker-backup-${new Date().toISOString().slice(0, 10)}.json`
    a.click()
    URL.revokeObjectURL(a.href)
  }

  async function importFile(file: File) {
    setStatus(null)
    try {
      const parsed = JSON.parse(await file.text())
      if (parsed?.app === 'sor4-survival-tracker') {
        setPending({ kind: 'backup', data: parsed as TrackerBackup })
      } else if (parsed && !Array.isArray(parsed) && Array.isArray(parsed.coop)) {
        // Old app's "Export JSON" shape: {coop: [...], solo: [...]}
        setMapA(list[0]?.id ?? '')
        setMapB(list[1]?.id ?? list[0]?.id ?? '')
        setMapSolo(list[0]?.id ?? '')
        setPending({
          kind: 'legacy-bundle',
          coop: parsed.coop as LegacyCoopRun[],
          solo: (Array.isArray(parsed.solo) ? parsed.solo : []) as LegacySoloRun[],
        })
      } else if (Array.isArray(parsed) && parsed.length && parsed[0].thomas !== undefined) {
        setMapA(list[0]?.id ?? '')
        setMapB(list[1]?.id ?? list[0]?.id ?? '')
        setPending({ kind: 'legacy-coop', runs: parsed as LegacyCoopRun[] })
      } else if (Array.isArray(parsed) && parsed.length && parsed[0].character !== undefined) {
        setMapA(list[0]?.id ?? '')
        setPending({ kind: 'legacy-solo', runs: parsed as LegacySoloRun[] })
      } else {
        setStatus('Unrecognised file — expected a tracker backup or legacy runs JSON.')
      }
    } catch {
      setStatus('Could not read that file — is it valid JSON?')
    }
  }

  async function confirmImport() {
    if (!pending) return
    try {
      if (pending.kind === 'backup') {
        const d = pending.data
        await saveAll(d.players)
        await coop.setAll(d.coop)
        await solo.setAll(d.solo)
        setStatus(`Restored ${d.players.length} players, ${d.coop.length} co-op runs, ${d.solo.length} solo runs.`)
      } else if (pending.kind === 'legacy-bundle') {
        if (pending.coop.length && mapA === mapB) return setStatus('Pick two different players for the co-op mapping.')
        const coopMapped: CoopRun[] = pending.coop.map((r) => ({
          id: r.id,
          loggedAt: r.loggedAt,
          players: [
            { playerId: mapA, char: r.thomas, score: r.thomasScore },
            { playerId: mapB, char: r.craig, score: r.craigScore },
          ],
          level: r.level,
          time: r.time,
        }))
        const soloMapped: SoloRun[] = pending.solo.map((r) => ({ ...r, playerId: mapSolo }))
        const c = mergeById(coopRuns, coopMapped)
        const s = mergeById(soloRuns, soloMapped)
        await coop.setAll(c.merged)
        await solo.setAll(s.merged)
        setStatus(`Imported ${c.added} co-op and ${s.added} solo runs.`)
      } else if (pending.kind === 'legacy-coop') {
        if (mapA === mapB) return setStatus('Pick two different players for the mapping.')
        const mapped: CoopRun[] = pending.runs.map((r) => ({
          id: r.id,
          loggedAt: r.loggedAt,
          players: [
            { playerId: mapA, char: r.thomas, score: r.thomasScore },
            { playerId: mapB, char: r.craig, score: r.craigScore },
          ],
          level: r.level,
          time: r.time,
        }))
        const { merged, added } = mergeById(coopRuns, mapped)
        await coop.setAll(merged)
        setStatus(`Imported ${added} of ${pending.runs.length} legacy co-op runs (${pending.runs.length - added} already existed).`)
      } else {
        const mapped: SoloRun[] = pending.runs.map((r) => ({ ...r, playerId: mapA }))
        const { merged, added } = mergeById(soloRuns, mapped)
        await solo.setAll(merged)
        setStatus(`Imported ${added} of ${pending.runs.length} legacy solo runs (${pending.runs.length - added} already existed).`)
      }
      setPending(null)
    } catch (e) {
      setStatus((e as Error).message)
    }
  }

  async function eraseAll() {
    if (!confirm('Erase ALL players and runs stored on this device? This cannot be undone.')) return
    if (!confirm('Really sure? Export a backup first if you might want this data later.')) return
    await coop.setAll([])
    await solo.setAll([])
    await saveAll([])
    await Promise.all(Object.keys(overrides).map((id) => removeOverride(id)))
    setStatus('All data erased.')
  }

  async function savePlayer() {
    if (!editing?.name.trim()) return
    const dupe = list.some((p) => p.name.trim().toLowerCase() === editing.name.trim().toLowerCase() && p.id !== editing.id)
    if (dupe) return setStatus('Another player already has that name.')
    await save({ id: editing.id ?? crypto.randomUUID(), name: editing.name.trim(), color: editing.color })
    setEditing(null)
  }

  return (
    <section className="view settings">
      <div className="panel">
        <h3>Players</h3>
        <p className="muted">Up to {MAX_PLAYERS} players. Runs are tracked per player and per co-op pairing.</p>
        <div className="player-rows">
          {list.map((p) => {
            const refs = refsOf(p.id)
            return (
              <div key={p.id} className="player-row">
                <span className="player-dot" style={{ background: p.color }} />
                <span className="grow">{p.name}</span>
                {refs > 0 && <span className="muted">{refs} run{refs === 1 ? '' : 's'}</span>}
                <button className="btn ghost small" onClick={() => setEditing({ id: p.id, name: p.name, color: p.color })}>
                  Edit
                </button>
                <button
                  className="btn danger small"
                  disabled={refs > 0}
                  title={refs > 0 ? `Used by ${refs} runs — delete them first` : 'Delete player'}
                  onClick={() => void remove(p.id)}
                >
                  Delete
                </button>
              </div>
            )
          })}
        </div>
        {list.length < MAX_PLAYERS && (
          <button className="btn" onClick={() => setEditing({ name: '', color: PLAYER_COLORS[list.length % PLAYER_COLORS.length] })}>
            + Add player
          </button>
        )}
      </div>

      <div className="panel">
        <h3>Character portraits</h3>
        <p className="muted">
          Replace a character's portrait with your own image — stored on this device. Missing images show a
          coloured letter tile automatically.
        </p>
        <div className="import-map">
          <CharacterSelect value={overrideChar} onChange={setOverrideChar} />
          <input
            ref={portraitInput}
            type="file"
            accept="image/*"
            hidden
            onChange={async (e) => {
              const f = e.target.files?.[0]
              if (f && overrideChar) await setOverride(overrideChar, f)
              e.target.value = ''
            }}
          />
          <button className="btn" disabled={!overrideChar} onClick={() => portraitInput.current?.click()}>
            Upload image
          </button>
        </div>
        {Object.keys(overrides).length > 0 && (
          <div className="override-list">
            {Object.keys(overrides).map((id) => (
              <div key={id} className="player-row">
                <Portrait id={id} size={28} />
                <span className="grow">{CHARACTERS.find((c) => c.id === id)?.label}</span>
                <button className="btn ghost small" onClick={() => void removeOverride(id)}>
                  Remove
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="panel">
        <h3>Backup &amp; restore</h3>
        <p className="muted">
          All data lives in this browser's storage. Export regularly — clearing browser data erases everything.
          Legacy files from the old two-player tracker can be imported too.
        </p>
        <div className="form-actions" style={{ marginTop: 0 }}>
          <button className="btn" onClick={exportData}>
            Export JSON
          </button>
          <button className="btn" onClick={() => fileInput.current?.click()}>
            Import JSON
          </button>
          <input
            ref={fileInput}
            type="file"
            accept="application/json,.json"
            hidden
            onChange={(e) => {
              const f = e.target.files?.[0]
              if (f) void importFile(f)
              e.target.value = ''
            }}
          />
          <span className="spacer" />
          <button className="btn danger" onClick={() => void eraseAll()}>
            Erase all data
          </button>
        </div>
        {status && <p className="muted">{status}</p>}
      </div>

      <p className="credits muted">
        Character art from the{' '}
        <a href="https://streetsofrage.fandom.com/wiki/Streets_of_Rage_Wiki" target="_blank" rel="noreferrer">
          Streets of Rage Wiki
        </a>
        . Streets of Rage © SEGA. Streets of Rage 4 © Dotemu, Lizardcube, Guard Crush Games. Fan-made, non-commercial.
      </p>

      {editing && (
        <Modal title={editing.id ? 'Edit player' : 'Add player'} onClose={() => setEditing(null)}>
          <PlayerFields value={editing} onChange={(v) => setEditing({ ...editing, ...v })} autoFocus />
          <div className="form-actions">
            <span className="spacer" />
            <button className="btn ghost" onClick={() => setEditing(null)}>
              Cancel
            </button>
            <button className="btn primary" disabled={!editing.name.trim()} onClick={() => void savePlayer()}>
              Save player
            </button>
          </div>
        </Modal>
      )}

      {pending?.kind === 'backup' && (
        <Modal title="Restore backup" onClose={() => setPending(null)}>
          <p className="muted">
            This backup contains {pending.data.players.length} players, {pending.data.coop.length} co-op runs and{' '}
            {pending.data.solo.length} solo runs (exported{' '}
            {new Date(pending.data.exportedAt).toLocaleDateString('en-GB')}).
          </p>
          <p className="form-warning">Restoring replaces ALL current players and runs.</p>
          <div className="form-actions">
            <span className="spacer" />
            <button className="btn ghost" onClick={() => setPending(null)}>
              Cancel
            </button>
            <button className="btn danger" onClick={() => void confirmImport()}>
              Replace everything
            </button>
          </div>
        </Modal>
      )}

      {pending?.kind === 'legacy-bundle' && (
        <Modal title="Import legacy backup" onClose={() => setPending(null)}>
          <p className="muted">
            This file is from the old two-player tracker ({pending.coop.length} co-op, {pending.solo.length} solo
            runs). Map its players:
          </p>
          <div className="import-map">
            <label>
              Thomas (rows)
              <PlayerSelect players={list} value={mapA} onChange={setMapA} />
            </label>
            <label>
              Craig (columns)
              <PlayerSelect players={list} value={mapB} onChange={setMapB} />
            </label>
            <label>
              Solo runs
              <PlayerSelect players={list} value={mapSolo} onChange={setMapSolo} />
            </label>
          </div>
          <div className="form-actions">
            <span className="spacer" />
            <button className="btn ghost" onClick={() => setPending(null)}>
              Cancel
            </button>
            <button
              className="btn primary"
              disabled={!mapA || !mapSolo || (!!pending.coop.length && mapA === mapB)}
              onClick={() => void confirmImport()}
            >
              Import runs
            </button>
          </div>
        </Modal>
      )}

      {pending?.kind === 'legacy-coop' && (
        <Modal title="Import legacy co-op runs" onClose={() => setPending(null)}>
          <p className="muted">
            This file is from the old two-player tracker ({pending.runs.length} runs). Map its players:
          </p>
          <div className="import-map">
            <label>
              Thomas (rows)
              <PlayerSelect players={list} value={mapA} onChange={setMapA} />
            </label>
            <label>
              Craig (columns)
              <PlayerSelect players={list} value={mapB} onChange={setMapB} />
            </label>
          </div>
          <div className="form-actions">
            <span className="spacer" />
            <button className="btn ghost" onClick={() => setPending(null)}>
              Cancel
            </button>
            <button className="btn primary" disabled={!mapA || !mapB || mapA === mapB} onClick={() => void confirmImport()}>
              Import runs
            </button>
          </div>
        </Modal>
      )}

      {pending?.kind === 'legacy-solo' && (
        <Modal title="Import legacy solo runs" onClose={() => setPending(null)}>
          <p className="muted">
            This file is from the old two-player tracker ({pending.runs.length} runs). Assign them to:
          </p>
          <div className="import-map">
            <label>
              Player
              <PlayerSelect players={list} value={mapA} onChange={setMapA} />
            </label>
          </div>
          <div className="form-actions">
            <span className="spacer" />
            <button className="btn ghost" onClick={() => setPending(null)}>
              Cancel
            </button>
            <button className="btn primary" disabled={!mapA} onClick={() => void confirmImport()}>
              Import runs
            </button>
          </div>
        </Modal>
      )}
    </section>
  )
}
