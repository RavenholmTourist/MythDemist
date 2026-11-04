import { useCallback, useEffect, useState } from 'react'
import type { Player } from '../types'
import { dbGet, dbSet, DB_KEYS } from './db'

export const MAX_PLAYERS = 4

/** Suggested colours; first two carry over the original Thomas/Craig palette. */
export const PLAYER_COLORS = [
  '#a970ff',
  '#3fa9f5',
  '#8be36b',
  '#ffcc00',
  '#ff6b6b',
  '#ff9f43',
  '#e06be3',
  '#5ee8d1',
]

export const UNKNOWN_PLAYER: Player = { id: '?', name: '?', color: '#666677' }

export interface PlayersStore {
  players: Player[] | null // null while loading
  error: string | null
  save: (p: Player) => Promise<void>
  saveAll: (list: Player[]) => Promise<void>
  remove: (id: string) => Promise<void>
  get: (id: string) => Player
}

export function usePlayers(): PlayersStore {
  const [players, setPlayers] = useState<Player[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    dbGet<Player[]>(DB_KEYS.players)
      .then((p) => setPlayers(p ?? []))
      .catch((e) => setError((e as Error).message))
  }, [])

  const persist = useCallback(async (next: Player[]) => {
    await dbSet(DB_KEYS.players, next)
    setPlayers(next)
  }, [])

  const save = useCallback(
    async (p: Player) => {
      const cur = (await dbGet<Player[]>(DB_KEYS.players)) ?? []
      const next = cur.some((x) => x.id === p.id) ? cur.map((x) => (x.id === p.id ? p : x)) : [...cur, p]
      await persist(next)
    },
    [persist],
  )

  const saveAll = useCallback((list: Player[]) => persist(list), [persist])

  const remove = useCallback(
    async (id: string) => {
      const cur = (await dbGet<Player[]>(DB_KEYS.players)) ?? []
      await persist(cur.filter((p) => p.id !== id))
    },
    [persist],
  )

  const get = useCallback((id: string) => players?.find((p) => p.id === id) ?? UNKNOWN_PLAYER, [players])

  return { players, error, save, saveAll, remove, get }
}
