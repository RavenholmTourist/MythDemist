import { useEffect, useMemo, useState, type CSSProperties } from 'react'
import { CHARACTERS, getCharacter, isGameBoundary } from '../characters'
import type { RunStore } from '../lib/useRunStore'
import { formatNumber, levelColor, pickRandom, sumTimes } from '../lib/time'
import type { CoopRun, Player } from '../types'
import { initial as playerInitial, pairKey, pairLabel, pairingKey, runPairing, total, winner } from '../lib/coop'
import { CoopStats } from './CoopStats'
import { MatrixFrame } from './MatrixFrame'
import { CoopRunForm, coopDraftOf, type CoopDraft } from './CoopRunForm'
import { Portrait } from './Portrait'
import { CharacterFace, ScratchCard } from './ScratchCard'
import { Progress, SegmentedControl, StatCard } from './Stats'

type CellMode = 'level' | 'score' | 'time'
const key = pairKey
const PAIRING_KEY = 'sor4.pairing'

function loadPairing(): [string, string] | null {
  try {
    const v = JSON.parse(localStorage.getItem(PAIRING_KEY) ?? 'null')
    return Array.isArray(v) && v.length === 2 && typeof v[0] === 'string' && typeof v[1] === 'string'
      ? [v[0], v[1]]
      : null
  } catch {
    return null
  }
}

export function CoopView({ store, players }: { store: RunStore<CoopRun>; players: Player[] }) {
  const { runs, saving, mutate } = store
  const [mode, setMode] = useState<CellMode>('level')
  const [form, setForm] = useState<CoopDraft | null>(null)
  const [suggestion, setSuggestion] = useState<{ a: string; b: string } | null>(null)
  const [hover, setHover] = useState<{ a: string; b: string } | null>(null)
  const [revealed, setRevealed] = useState({ a: false, b: false })
  const [rollId, setRollId] = useState(0)
  const [pairIds, setPairIds] = useState<[string, string]>(() => loadPairing() ?? ['', ''])
  const fullyRevealed = revealed.a && revealed.b

  const [aId, bId] = pairIds
  const playerA = players.find((p) => p.id === aId)
  const playerB = players.find((p) => p.id === bId)
  const pairingValid = players.length >= 2 && playerA && playerB && aId !== bId

  useEffect(() => {
    if (players.length >= 2 && !pairingValid)
      setPairIds([players[0].id, players[1].id])
  }, [players, pairingValid])

  const setPairing = (next: [string, string]) => {
    setPairIds(next)
    localStorage.setItem(PAIRING_KEY, JSON.stringify(next))
  }
  // Picking the same player for both slots swaps them instead of clashing.
  const pickA = (id: string) => setPairing(id === bId ? [id, aId] : [id, bId])
  const pickB = (id: string) => setPairing(id === aId ? [id, bId] : [aId, id])

  const pairRuns = useMemo(
    () => runs.filter((r) => runPairing(r) === pairingKey(aId, bId)),
    [runs, aId, bId],
  )
  const byPair = useMemo(
    () => new Map(pairRuns.map((r) => [key(r.players[0].char, r.players[1].char), r])),
    [pairRuns],
  )
  const wins = useMemo(() => {
    const w = { a: 0, b: 0, tie: 0 }
    pairRuns.forEach((r) => {
      const wn = winner(r)
      w[wn === 'tie' ? 'tie' : wn === 0 ? 'a' : 'b']++
    })
    return w
  }, [pairRuns])
  const best = useMemo(() => [...pairRuns].sort((x, y) => total(y) - total(x)).slice(0, 5), [pairRuns])

  function roll() {
    const open = CHARACTERS.flatMap((t) =>
      CHARACTERS.filter((c) => !byPair.has(key(t.id, c.id))).map((c) => ({ a: t.id, b: c.id })),
    )
    setSuggestion(pickRandom(open))
    setRevealed({ a: false, b: false })
    setRollId((n) => n + 1)
  }

  async function save(run: CoopRun, isNew: boolean) {
    await mutate((all) => (isNew ? [...all, run] : all.map((r) => (r.id === run.id ? run : r))))
    if (suggestion && suggestion.a === run.players[0].char && suggestion.b === run.players[1].char)
      setSuggestion(null)
  }

  async function remove(id: string) {
    await mutate((all) => all.filter((r) => r.id !== id))
  }

  if (players.length < 2) {
    return (
      <section className="view">
        <div className="panel">
          <h3>Two players needed</h3>
          <p className="muted">Add at least two players in Settings to track co-op runs.</p>
        </div>
      </section>
    )
  }
  if (!pairingValid) return null // effect above will pick a valid pairing

  const allDone = pairRuns.length >= CHARACTERS.length ** 2

  return (
    <section
      className="view"
      style={{ '--pa': playerA.color, '--pb': playerB.color } as CSSProperties}
    >
      <div className="pairing-bar">
        <span className="pairing-label">Pairing</span>
        <select className="player-pick" value={aId} onChange={(e) => pickA(e.target.value)} style={{ color: playerA.color }}>
          {players.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
        <button className="icon-btn" title="Swap sides" aria-label="Swap sides" onClick={() => setPairing([bId, aId])}>
          ⇄
        </button>
        <select className="player-pick" value={bId} onChange={(e) => pickB(e.target.value)} style={{ color: playerB.color }}>
          {players.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
        <span className="muted pairing-note">runs, matrix &amp; stats are tracked per pairing</span>
      </div>

      <div className="dashboard">
        <div className="scoreboard">
          <div className={`score-side a ${wins.a > wins.b ? 'leading' : ''}`}>
            <span className="score-name">{playerA.name}</span>
            <span className="score-num">{wins.a}</span>
          </div>
          <div className="score-vs">
            <span>WINS</span>
            {wins.tie > 0 && <small>{wins.tie} tie{wins.tie > 1 ? 's' : ''}</small>}
          </div>
          <div className={`score-side b ${wins.b > wins.a ? 'leading' : ''}`}>
            <span className="score-num">{wins.b}</span>
            <span className="score-name">{playerB.name}</span>
          </div>
        </div>
        <div className="randomizer">
          <div className="randomizer-head">
            <h3>Next random pairing</h3>
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
                  key={`a${rollId}`}
                  title={playerA.name}
                  accent="var(--pa)"
                  revealed={revealed.a}
                  onReveal={() => setRevealed((r) => ({ ...r, a: true }))}
                >
                  <CharacterFace {...getCharacter(suggestion.a)} />
                </ScratchCard>
                <span className="scratch-vs">VS</span>
                <ScratchCard
                  key={`b${rollId}`}
                  title={playerB.name}
                  accent="var(--pb)"
                  revealed={revealed.b}
                  locked={!revealed.a}
                  lockedHint={`${playerA.name} first`}
                  onReveal={() => setRevealed((r) => ({ ...r, b: true }))}
                >
                  <CharacterFace {...getCharacter(suggestion.b)} />
                </ScratchCard>
              </div>
              {fullyRevealed ? (
                <button className="btn" onClick={() => setForm({ charA: suggestion.a, charB: suggestion.b })}>
                  Log this run
                </button>
              ) : (
                <p className="muted scratch-hint">
                  Scratch or tap {revealed.a ? `${playerB.name}'s` : `${playerA.name}'s`} card to reveal
                </p>
              )}
            </div>
          ) : (
            <p className="muted">Roll for an unplayed pairing, then scratch to reveal each character.</p>
          )}
        </div>
      </div>

      <div className="stat-row">
        <StatCard label="Progress" value={<Progress done={pairRuns.length} total={CHARACTERS.length ** 2} />} />
        <StatCard label="Time played" value={sumTimes(pairRuns.map((r) => r.time))} />
        <StatCard
          label="Highest level"
          value={pairRuns.length ? Math.max(...pairRuns.map((r) => r.level)) : '-'}
          sub={best[0] && `Best total ${formatNumber(total(best[0]))}`}
        />
      </div>

      <MatrixFrame
        toolbar={
          <>
            <h3>
              <span className="pa-text">{playerA.name}</span> ↓ vs <span className="pb-text">{playerB.name}</span> →
            </h3>
            <SegmentedControl
              value={mode}
              onChange={setMode}
              options={[
                { value: 'level', label: 'Level' },
                { value: 'score', label: 'Total score' },
                { value: 'time', label: 'Time' },
              ]}
            />
            <button className="btn primary" onClick={() => setForm({})}>
              + Log run
            </button>
          </>
        }
      >
        <table className="matrix coop" data-mode={mode} onMouseLeave={() => setHover(null)}>
          <thead>
            <tr>
              <th className="corner">
                <span className="pa-text">{playerInitial(playerA.name)}</span> \{' '}
                <span className="pb-text">{playerInitial(playerB.name)}</span>
              </th>
              {CHARACTERS.map((c, ci) => (
                <th
                  key={c.id}
                  className={`col-head ${isGameBoundary(ci) ? 'boundary' : ''} ${hover?.b === c.id ? 'hl' : ''}`}
                >
                  <Portrait id={c.id} size={34} />
                  <span className="col-label">
                    <span className={`game-tag game-${c.game.toLowerCase()}`}>{c.game}</span>
                    {c.name}
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {CHARACTERS.map((t, ri) => (
              <tr key={t.id} className={isGameBoundary(ri) ? 'boundary' : ''}>
                <th className={`row-head ${hover?.a === t.id ? 'hl' : ''}`}>
                  <Portrait id={t.id} size={30} showName />
                </th>
                {CHARACTERS.map((c, ci) => {
                  const run = byPair.get(key(t.id, c.id))
                  const w = run ? winner(run) : null
                  const isSuggested = fullyRevealed && suggestion?.a === t.id && suggestion?.b === c.id
                  const cls = [
                    'cell',
                    run ? 'played' : 'open',
                    isGameBoundary(ci) ? 'boundary' : '',
                    isSuggested ? 'suggested' : '',
                    hover && (hover.a === t.id || hover.b === c.id) ? 'crosshair' : '',
                  ].join(' ')
                  return (
                    <td key={c.id} className={cls}>
                      <button
                        style={run ? { background: levelColor(run.level) } : undefined}
                        onMouseEnter={() => setHover({ a: t.id, b: c.id })}
                        onClick={() => setForm(run ? coopDraftOf(run) : { charA: t.id, charB: c.id })}
                        title={
                          run
                            ? `${pairLabel(t.id, c.id)}\nLvl ${run.level} · ${run.time}\n${playerA.name} ${formatNumber(run.players[0].score)} · ${playerB.name} ${formatNumber(run.players[1].score)}\nTotal ${formatNumber(total(run))}`
                            : `${pairLabel(t.id, c.id)}\nNot played yet - click to log`
                        }
                      >
                        {run ? (
                          <>
                            <span className="cell-main">
                              {mode === 'level'
                                ? run.level
                                : mode === 'score'
                                  ? `${Math.round(total(run) / 1000)}k`
                                  : run.time.replace(/^00:/, '')}
                            </span>
                            <span className={`winner-dot ${w === 'tie' ? 'tie' : w === 0 ? 'a' : 'b'}`}>
                              {w === 'tie' ? '=' : playerInitial((w === 0 ? playerA : playerB).name)}
                            </span>
                          </>
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

      <CoopStats runs={pairRuns} a={playerA} b={playerB} onOpen={(r) => setForm(coopDraftOf(r))} />

      {form && (
        <CoopRunForm
          key={form.id ?? 'new'}
          runs={pairRuns}
          a={playerA}
          b={playerB}
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
