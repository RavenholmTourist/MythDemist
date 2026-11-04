import { getCharacter } from '../characters'
import type { CoopRun } from '../types'

/** 0 = row player (slot A), 1 = column player (slot B). */
export type Side = 0 | 1
export type Winner = Side | 'tie'

export const pairKey = (a: string, b: string) => `${a}|${b}`
export const pairingKey = (aId: string, bId: string) => `${aId}|${bId}`
export const runPairing = (r: CoopRun) => pairingKey(r.players[0].playerId, r.players[1].playerId)
export const total = (r: CoopRun) => r.players[0].score + r.players[1].score
export const winner = (r: CoopRun): Winner =>
  r.players[0].score > r.players[1].score ? 0 : r.players[1].score > r.players[0].score ? 1 : 'tie'
export const pairLabel = (a: string, b: string) => `${getCharacter(a).label} + ${getCharacter(b).label}`
export const initial = (name: string) => (name.trim()[0] ?? '?').toUpperCase()
