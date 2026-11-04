import { useEffect, useMemo, useState, type CSSProperties } from 'react'
import { CHARACTERS, getCharacter, isGameBoundary } from '../characters'
import type { RunStore } from '../lib/useRunStore'
import { formatNumber, levelColor, pickRandom, sumTimes } from '../lib/time'
import type { MoveVariant, Player, SoloRun } from '../types'
import { MatrixFrame } from './MatrixFrame'
import { Portrait } from './Portrait'
import { SoloStats } from './SoloStats'
import { CharacterFace, ScratchCard } from './ScratchCard'
import { SoloRunForm } from './SoloRunForm'
import { Progress, StatCard } from './Stats'

interface Combo {
  blitz: MoveVariant
  star: MoveVariant
}

const COMBOS: Combo[] = [
  { blitz: 'default', star: 'default' },
  { blitz: 'alternate', star: 'default' },
  { blitz: 'default', star: 'alternate' },
  { blitz: 'alternate', star: 'alternate' },
]

const cap = (v: MoveVariant) => (v === 'default' ? 'Default' : 'Alternate')
const key = (id: string, c: Combo) => `${id}|${c.blitz}|${c.star}`
const comboLabel = (c: Combo) => `${cap(c.blitz)} Blitz / ${cap(c.star)} Star`

const VALID = CHARACTERS.flatMap((ch) =>
  COMBOS.filter((c) => ch.hasAltBlitz || c.blitz === 'default').map((c) => ({ character: ch.id, ...c })),
)

const SOLO_PLAYER_KEY = 'sor4.solo-player'

export function SoloView({ store, players }: { store: RunStore<SoloRun>; players: Player[] }) {
  const { runs, saving, mutate } = store
  const [form, setForm] = useState<Partial<SoloRun> | null>(null)
  const [suggestion, setSuggestion] = useState<({ character: string } & Combo) | null>(null)
  const [revealed, setRevealed] = useState({ character: false, combo: false })
  const [rollId, setRollId] = useState(0)
  const [playerId, setPlayerIdState] = useState<string>(() => localStorage.getItem(SOLO_PLAYER_KEY) ?? '')
  const fullyRevealed = revealed.character && revealed.combo

  const player = players.find((p) => p.id === playerId)

  useEffect(() => {
    if (players.length && !player) setPlayerIdState(players[0].id)
  }, [players, player])

  const setPlayerId = (id: string) => {
    setPlayerIdState(id)
    localStorage.setItem(SOLO_PLAYER_KEY, id)
  }

  const playerRuns = useMemo(() => runs.filter((r) => r.playerId === playerId), [runs, playerId])
  const byKey = useMemo(() => new Map(playerRuns.map((r) => [key(r.character, r), r])), [playerRuns])
  const best = useMemo(() => [...playerRuns].sort((a, b) => b.score - a.score).slice(0, 5), [playerRuns])
  const allDone = VALID.every((v) => byKey.has(key(v.character, v)))

  function roll() {
    setSuggestion(pickRandom(VALID.filter((v) => !byKey.has(key(v.character, v)))))
    setRevealed({ character: false, combo: false })
    setRollId((n) => n + 1)
  }

  async function save(run: SoloRun, isNew: boolean) {
    await mutate((all) => (isNew ? [...all, run] : all.map((r) => (r.id === run.id ? run : r))))
    if (suggestion && key(suggestion.character, suggestion) === key(run.character, run)) setSuggestion(null)
  }

  async function remove(id: string) {
    await mutate((all) => all.filter((r) => r.id !== id))
  }

  if (!players.length) {
    return (
      <section className="view">
        <div className="panel">
          <h3>Add a player</h3>
          <p className="muted">Add a player in Settings to track solo runs.</p>
        </div>
      </section>
    )
  }
  if (!player) return null // effect above will pick a valid player

  return (
    <section className="view" style={{ '--pa': player.color } as CSSProperties}>
      <div className="pairing-bar">
        <span className="pairing-label">Player</span>
        <select className="player-pick" value={playerId} onChange={(e) => setPlayerId(e.target.value)} style={{ color: player.color }}>
          {players.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
        <span className="muted pairing-note">solo progress is tracked per player</span>
      </div>

      <div className="dashboard">
        <div className="stat-stack">
          <StatCard label="Progress" value={<Progress done={playerRuns.length} total={VALID.length} />} />
          <div className="stat-row tight">
            <StatCard label="Time played" value={sumTimes(playerRuns.map((r) => r.time))} />
            <StatCard label="Highest level" value={playerRuns.length ? Math.max(...playerRuns.map((r) => r.level)) : '-'} />
            <StatCard label="Best score" value={best[0] ? formatNumber(best[0].score) : '-'} />
          </div>
        </div>
        <div className="randomizer">
          <div className="randomizer-head">
            <h3>Next random run</h3>
            <button className="btn primary" onClick={roll} disabled={allDone}>
              Roll
            </button>
          </div>
          {allDone ? (
            <p className="muted">Challenge complete!</p>
          ) : suggestion ? (
            <div className="suggestion">
              <div className="scratch-row">
                <ScratchCard
                  key={`ch${rollId}`}
                  title="Character"
                  accent="var(--yellow)"
                  revealed={revealed.character}
                  onReveal={() => setRevealed((r) => ({ ...r, character: true }))}
                >
                  <CharacterFace {...getCharacter(suggestion.character)} />
                </ScratchCard>
                <ScratchCard
                  key={`co${rollId}`}
                  title="Moves"
                  accent="var(--red)"
                  revealed={revealed.combo}
                  locked={!revealed.character}
                  lockedHint="Character first"
                  onReveal={() => setRevealed((r) => ({ ...r, combo: true }))}
                >
                  <span className={`chip big ${suggestion.blitz}`}>{cap(suggestion.blitz)} Blitz</span>
                  <span className={`chip big ${suggestion.star}`}>{cap(suggestion.star)} Star</span>
                </ScratchCard>
              </div>
              {fullyRevealed ? (
                <button className="btn" onClick={() => setForm({ ...suggestion })}>
                  Log this run
                </button>
              ) : (
                <p className="muted scratch-hint">
                  Scratch or tap the {revealed.character ? 'moves' : 'character'} card to reveal
                </p>
              )}
            </div>
          ) : (
            <p className="muted">Roll for an unplayed character + move combo.</p>
          )}
        </div>
      </div>

      <MatrixFrame
        toolbar={
          <>
            <h3>
              <span className="pa-text">{player.name}</span> — Character × Blitz / Star
            </h3>
            <button className="btn primary" onClick={() => setForm({})}>
              + Log run
            </button>
          </>
        }
      >
        <table className="matrix solo">
          <thead>
            <tr>
              <th className="corner">Character</th>
              {COMBOS.map((c) => (
                <th key={key('', c)} className="col-head combo-head">
                  <span className={`chip ${c.blitz}`}>{cap(c.blitz)} Blitz</span>
                  <span className={`chip ${c.star}`}>{cap(c.star)} Star</span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {CHARACTERS.map((ch, ri) => (
              <tr key={ch.id} className={isGameBoundary(ri) ? 'boundary' : ''}>
                <th className="row-head">
                  <Portrait id={ch.id} size={41} showName />
                </th>
                {COMBOS.map((c) => {
                  const blocked = !ch.hasAltBlitz && c.blitz === 'alternate'
                  const run = byKey.get(key(ch.id, c))
                  const isSuggested = fullyRevealed && suggestion && key(suggestion.character, suggestion) === key(ch.id, c)
                  if (blocked)
                    return (
                      <td key={key(ch.id, c)} className="cell blocked" title="SoR1 characters have no Alternate Blitz">
                        <span>N/A</span>
                      </td>
                    )
                  return (
                    <td
                      key={key(ch.id, c)}
                      className={`cell ${run ? 'played' : 'open'} ${isSuggested ? 'suggested' : ''}`}
                    >
                      <button
                        style={run ? { background: levelColor(run.level) } : undefined}
                        onClick={() => setForm(run ?? { character: ch.id, ...c })}
                        title={`${ch.label} | ${comboLabel(c)}`}
                      >
                        {run ? (
                          <span className="solo-cell">
                            <strong>Lvl {run.level}</strong>
                            <span>{run.time}</span>
                            <span>{formatNumber(run.score)}</span>
                          </span>
                        ) : (
                          <span className="cell-plus">+</span>
                        )}
                      </button>
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </MatrixFrame>

      <SoloStats runs={playerRuns} onOpen={setForm} />

      {form && (
        <SoloRunForm
          key={form.id ?? 'new'}
          runs={playerRuns}
          player={player}
          initial={form}
          saving={saving}
          onSave={save}
          onDelete={remove}
          onClose={() => setForm(null)}
        />
      )}
    </section>
  )
}
