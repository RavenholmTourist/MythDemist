import { useMemo, useState } from 'react'
import { CHARACTERS, GAMES, getCharacter, type Game } from '../characters'
import { initial as playerInitial, total, winner, type Side, type Winner } from '../lib/coop'
import { formatNumber, formatTime, levelColor, parseTime } from '../lib/time'
import type { CoopRun, Player } from '../types'
import { Portrait } from './Portrait'
import { SegmentedControl } from './Stats'
import type { ReactNode } from 'react'
import { CompareTable, StatsDeck, type StatPanel } from './StatsDeck'

const secs = (r: CoopRun) => parseTime(r.time) ?? 0
const avg = (xs: number[]) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : 0)
const scoreOf = (r: CoopRun, s: Side) => r.players[s].score
const charOf = (r: CoopRun, s: Side) => r.players[s].char
const other = (s: Side): Side => (s === 0 ? 1 : 0)

type Who = 'all' | Side

interface Props {
  runs: CoopRun[]
  a: Player
  b: Player
  onOpen: (r: CoopRun) => void
}

function PortraitBadge({ id, side, pair }: { id: string; side: Side; pair: [Player, Player] }) {
  const cls = side === 0 ? 'a' : 'b'
  return (
    <span className="portrait-badge">
      <Portrait id={id} size={36} />
      <span className={`winner-dot ${cls}`}>{playerInitial(pair[side].name)}</span>
    </span>
  )
}

// Winner on the left; dots show which player each portrait belongs to.
function PairRow({ r, pair, onOpen, right }: { r: CoopRun; pair: [Player, Player]; onOpen: (r: CoopRun) => void; right: ReactNode }) {
  const w = winner(r)
  const first: Side = w === 1 ? 1 : 0
  return (
    <li onClick={() => onOpen(r)}>
      <PortraitBadge id={charOf(r, first)} side={first} pair={pair} />
      <PortraitBadge id={charOf(r, other(first))} side={other(first)} pair={pair} />
      <span className="grow" />
      {right}
    </li>
  )
}

function WinTag({ w, pair }: { w: Winner; pair: [Player, Player] }) {
  return (
    <span className={`winner-dot inline ${w === 'tie' ? 'tie' : w === 0 ? 'a' : 'b'}`}>
      {w === 'tie' ? '=' : playerInitial(pair[w].name)}
    </span>
  )
}

function streaks(runs: CoopRun[]) {
  const ordered = [...runs].sort((a, b) => a.loggedAt.localeCompare(b.loggedAt))
  const longest: [number, number] = [0, 0]
  let cur: { who: Winner; n: number } = { who: 'tie', n: 0 }
  for (const r of ordered) {
    const w = winner(r)
    cur = w === cur.who ? { who: w, n: cur.n + 1 } : { who: w, n: 1 }
    if (w !== 'tie') longest[w] = Math.max(longest[w], cur.n)
  }
  return { longest, current: cur }
}

export function CoopStats({ runs, a, b, onOpen }: Props) {
  const [who, setWho] = useState<Who>('all')
  const panels = useMemo<StatPanel[]>(() => {
    const pair: [Player, Player] = [a, b]
    if (!runs.length) return []
    const byTotal = [...runs].sort((x, y) => total(y) - total(x))
    const byLevel = [...runs].sort((x, y) => y.level - x.level || secs(y) - secs(x))
    const margins = [...runs].sort(
      (x, y) => Math.abs(x.players[0].score - x.players[1].score) - Math.abs(y.players[0].score - y.players[1].score),
    )
    const recent = [...runs].sort((x, y) => y.loggedAt.localeCompare(x.loggedAt)).slice(0, 8)
    const { longest, current } = streaks(runs)

    const playerStats = (s: Side) => {
      const scores = runs.map((r) => scoreOf(r, s))
      const won = runs.filter((r) => winner(r) === s)
      return {
        wins: won.length,
        winPct: (won.length / runs.length) * 100,
        avg: avg(scores),
        best: Math.max(...scores),
        totalPts: scores.reduce((acc, v) => acc + v, 0),
        margin: won.length ? avg(won.map((r) => Math.abs(r.players[0].score - r.players[1].score))) : null,
        longest: longest[s],
      }
    }
    const t = playerStats(0)
    const c = playerStats(1)
    const h2h = (x: number, y: number): 'a' | 'b' | null => (x > y ? 'a' : y > x ? 'b' : null)

    const individual = runs
      .flatMap((r) => ([0, 1] as Side[]).map((s) => ({ r, s, char: charOf(r, s), score: scoreOf(r, s) })))
      .sort((x, y) => y.score - x.score)

    const charStats = (p: Who) =>
      CHARACTERS.map((ch) => {
        const entries = runs.flatMap((r) => {
          const out: { level: number; score: number }[] = []
          if ((p === 'all' || p === 0) && r.players[0].char === ch.id) out.push({ level: r.level, score: r.players[0].score })
          if ((p === 'all' || p === 1) && r.players[1].char === ch.id) out.push({ level: r.level, score: r.players[1].score })
          return out
        })
        return { ch, n: entries.length, avgLevel: avg(entries.map((e) => e.level)), avgScore: avg(entries.map((e) => e.score)) }
      })
        .filter((x) => x.n > 0)
        .sort((x, y) => y.avgLevel - x.avgLevel)

    const gameGrid = (tg: Game, cg: Game) => {
      const cell = runs.filter((r) => getCharacter(r.players[0].char).game === tg && getCharacter(r.players[1].char).game === cg)
      return { n: cell.length, avgLevel: avg(cell.map((r) => r.level)) }
    }

    const multiNames = [...new Set(CHARACTERS.map((ch) => ch.name))].filter(
      (n) => CHARACTERS.filter((ch) => ch.name === n).length > 1,
    )
    const latestOf = (name: string) => CHARACTERS.find((ch) => ch.name === name)!.id
    const nameGrid = (tn: string, cn: string) => {
      const cell = runs.filter((r) => getCharacter(r.players[0].char).name === tn && getCharacter(r.players[1].char).name === cn)
      return { n: cell.length, avgLevel: avg(cell.map((r) => r.level)) }
    }

    const times = runs.map(secs)
    const longestRun = runs[times.indexOf(Math.max(...times))]
    const shortestRun = runs[times.indexOf(Math.min(...times))]

    const playerName = (s: Side) => <span className={s === 0 ? 'pa-text' : 'pb-text'}>{pair[s].name}</span>

    return [
      {
        id: 'h2h',
        label: 'Head to head',
        render: () => (
          <>
            <CompareTable
              left={playerName(0)}
              right={playerName(1)}
              rows={[
                ['Wins', t.wins, c.wins, h2h(t.wins, c.wins)],
                ['Win rate', `${Math.round(t.winPct)}%`, `${Math.round(c.winPct)}%`, h2h(t.winPct, c.winPct)],
                ['Average score', formatNumber(Math.round(t.avg)), formatNumber(Math.round(c.avg)), h2h(t.avg, c.avg)],
                ['Best score', formatNumber(t.best), formatNumber(c.best), h2h(t.best, c.best)],
                ['Total points', formatNumber(t.totalPts), formatNumber(c.totalPts), h2h(t.totalPts, c.totalPts)],
                [
                  'Avg winning margin',
                  t.margin === null ? '-' : formatNumber(Math.round(t.margin)),
                  c.margin === null ? '-' : formatNumber(Math.round(c.margin)),
                  t.margin === null || c.margin === null ? null : h2h(t.margin, c.margin),
                ],
                ['Longest win streak', t.longest, c.longest, h2h(t.longest, c.longest)],
              ]}
            />
            {current.who !== 'tie' && (
              <p className="deck-note">
                Current streak: {playerName(current.who)} has won {current.n} in a row
              </p>
            )}
          </>
        ),
      },
      {
        id: 'pairs',
        label: 'Best pairs',
        render: () => (
          <ol className="top-list">
            {byTotal.slice(0, 6).map((r) => (
              <PairRow key={r.id} r={r} pair={pair} onOpen={onOpen} right={<><span className="muted">Lvl {r.level}</span><strong>{formatNumber(total(r))}</strong></>} />
            ))}
          </ol>
        ),
      },
      {
        id: 'deepest',
        label: 'Deepest runs',
        render: () => (
          <ol className="top-list">
            {byLevel.slice(0, 6).map((r) => (
              <PairRow key={r.id} r={r} pair={pair} onOpen={onOpen} right={<><span className="muted">{r.time}</span><strong>Lvl {r.level}</strong></>} />
            ))}
          </ol>
        ),
      },
      {
        id: 'high',
        label: 'High scores',
        render: () => (
          <ol className="top-list">
            {individual.slice(0, 8).map(({ r, s, char, score }) => (
              <li key={`${r.id}-${s}`} onClick={() => onOpen(r)}>
                <PortraitBadge id={char} side={s} pair={pair} />
                <span className="grow">
                  {playerName(s)} <span className="muted">as</span> {getCharacter(char).label}
                </span>
                <span className="muted">Lvl {r.level}</span>
                <strong>{formatNumber(score)}</strong>
              </li>
            ))}
          </ol>
        ),
      },
      {
        id: 'chars',
        label: 'Characters',
        render: () => (
          <>
            <SegmentedControl
              value={String(who)}
              options={[
                { value: 'all', label: 'Combined' },
                { value: '0', label: a.name },
                { value: '1', label: b.name },
              ]}
              onChange={(v) => setWho(v === 'all' ? 'all' : (Number(v) as Side))}
            />
            <p className="deck-note">
              {who === 'all' ? 'Every run featuring each character, by either player.' : `Runs where ${pair[who].name} played each character.`}
            </p>
            <table className="compare-table wide">
              <thead>
                <tr>
                  <th />
                  <th>Runs</th>
                  <th>Avg level</th>
                  <th>Avg score</th>
                </tr>
              </thead>
              <tbody>
                {charStats(who).map((x) => (
                  <tr key={x.ch.id}>
                    <th>
                      <Portrait id={x.ch.id} size={31} /> {x.ch.label}
                    </th>
                    <td>{x.n}</td>
                    <td>{x.avgLevel.toFixed(1)}</td>
                    <td>{formatNumber(Math.round(x.avgScore))}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        ),
      },
      {
        id: 'margins',
        label: 'Close calls',
        render: () => (
          <div className="two-col">
            {[
              { title: 'Closest finishes', list: margins.slice(0, 4) },
              { title: 'Biggest blowouts', list: margins.slice(-4).reverse() },
            ].map(({ title, list }) => (
              <div key={title}>
                <h4>{title}</h4>
                <ol className="top-list">
                  {list.map((r) => (
                    <PairRow
                      key={r.id}
                      r={r}
                      pair={pair}
                      onOpen={onOpen}
                      right={<><WinTag w={winner(r)} pair={pair} /><strong>{formatNumber(Math.abs(r.players[0].score - r.players[1].score))}</strong></>}
                    />
                  ))}
                </ol>
              </div>
            ))}
          </div>
        ),
      },
      {
        id: 'games',
        label: 'Game vs game',
        render: () => (
          <>
            <p className="deck-note">
              Average level by {playerName(0)}'s game (rows) vs {playerName(1)}'s game (columns).
            </p>
            <table className="game-grid">
              <thead>
                <tr>
                  <th />
                  {GAMES.map((g) => (
                    <th key={g}>
                      <span className={`game-tag game-${g.toLowerCase()}`}>{g}</span>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {GAMES.map((tg) => (
                  <tr key={tg}>
                    <th>
                      <span className={`game-tag game-${tg.toLowerCase()}`}>{tg}</span>
                    </th>
                    {GAMES.map((cg) => {
                      const cell = gameGrid(tg, cg)
                      return (
                        <td key={cg} style={cell.n ? { background: levelColor(cell.avgLevel) } : undefined}>
                          {cell.n ? (
                            <>
                              <strong>{cell.avgLevel.toFixed(1)}</strong>
                              <small>{cell.n} {cell.n === 1 ? 'run' : 'runs'}</small>
                            </>
                          ) : (
                            <small className="muted">-</small>
                          )}
                        </td>
                      )
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        ),
      },
      {
        id: 'names',
        label: 'Char vs char',
        render: () => (
          <>
            <p className="deck-note">
              Average level when {playerName(0)} (rows) faces {playerName(1)} (columns), all versions of each
              character combined.
            </p>
            <table className="game-grid">
              <thead>
                <tr>
                  <th />
                  {multiNames.map((n) => (
                    <th key={n}>
                      <Portrait id={latestOf(n)} size={41} />
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {multiNames.map((tn) => (
                  <tr key={tn}>
                    <th>
                      <Portrait id={latestOf(tn)} size={41} />
                    </th>
                    {multiNames.map((cn) => {
                      const cell = nameGrid(tn, cn)
                      return (
                        <td key={cn} style={cell.n ? { background: levelColor(cell.avgLevel) } : undefined}>
                          {cell.n ? (
                            <>
                              <strong>{cell.avgLevel.toFixed(1)}</strong>
                              <small>{cell.n} {cell.n === 1 ? 'run' : 'runs'}</small>
                            </>
                          ) : (
                            <small className="muted">-</small>
                          )}
                        </td>
                      )
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        ),
      },
      {
        id: 'records',
        label: 'Records',
        render: () => (
          <div className="record-grid">
            <div><span className="stat-label">Runs logged</span><strong>{runs.length}</strong></div>
            <div><span className="stat-label">Average level</span><strong>{avg(runs.map((r) => r.level)).toFixed(1)}</strong></div>
            <div><span className="stat-label">Average run time</span><strong>{formatTime(Math.round(avg(times)))}</strong></div>
            <div><span className="stat-label">Average combined</span><strong>{formatNumber(Math.round(avg(runs.map(total))))}</strong></div>
            <div onClick={() => onOpen(longestRun)} className="clickable">
              <span className="stat-label">Longest run</span><strong>{longestRun.time}</strong>
              <small>{getCharacter(longestRun.players[0].char).label} + {getCharacter(longestRun.players[1].char).label}</small>
            </div>
            <div onClick={() => onOpen(shortestRun)} className="clickable">
              <span className="stat-label">Shortest run</span><strong>{shortestRun.time}</strong>
              <small>{getCharacter(shortestRun.players[0].char).label} + {getCharacter(shortestRun.players[1].char).label}</small>
            </div>
          </div>
        ),
      },
      {
        id: 'recent',
        label: 'Recent runs',
        render: () => (
          <ol className="top-list">
            {recent.map((r) => (
              <PairRow
                key={r.id}
                r={r}
                pair={pair}
                onOpen={onOpen}
                right={<><span className="muted">{new Date(r.loggedAt).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })}</span><span className="muted">Lvl {r.level}</span><WinTag w={winner(r)} pair={pair} /></>}
              />
            ))}
          </ol>
        ),
      },
    ]
  }, [runs, onOpen, who, a, b])

  return <StatsDeck panels={panels} />
}
