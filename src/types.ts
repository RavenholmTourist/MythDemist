export type MoveVariant = 'default' | 'alternate'

export interface Player {
  id: string
  name: string
  color: string
}

export interface CoopSide {
  playerId: string
  char: string
  score: number
}

export interface CoopRun {
  id: string
  loggedAt: string
  /** players[0] = row player, players[1] = column player. Order matters. */
  players: [CoopSide, CoopSide]
  level: number
  time: string
}

export interface SoloRun {
  id: string
  loggedAt: string
  playerId: string
  character: string
  blitz: MoveVariant
  star: MoveVariant
  level: number
  time: string
  score: number
}

/** Shapes from the legacy two-player git_game app, for import only. */
export interface LegacyCoopRun {
  id: string
  loggedAt: string
  thomas: string
  craig: string
  thomasScore: number
  craigScore: number
  level: number
  time: string
}

export type LegacySoloRun = Omit<SoloRun, 'playerId'>

export interface TrackerBackup {
  app: 'sor4-survival-tracker'
  version: 2
  exportedAt: string
  players: Player[]
  coop: CoopRun[]
  solo: SoloRun[]
}
