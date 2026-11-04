import { useCallback, useEffect, useState } from 'react'
import { dbGet, dbSet, DB_KEYS } from './db'

export interface RunStore<T> {
  runs: T[]
  loading: boolean
  saving: boolean
  error: string | null
  reload: () => Promise<void>
  setAll: (runs: T[]) => Promise<void>
  mutate: (fn: (runs: T[]) => T[]) => Promise<void>
}

const keyFor = (kind: 'coop' | 'solo') => (kind === 'coop' ? DB_KEYS.coopRuns : DB_KEYS.soloRuns)

export function useRunStore<T>(kind: 'coop' | 'solo'): RunStore<T> {
  const key = keyFor(kind)
  const [runs, setRuns] = useState<T[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const reload = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      setRuns((await dbGet<T[]>(key)) ?? [])
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }, [key])

  useEffect(() => {
    void reload()
  }, [reload])

  const setAll = useCallback(
    async (next: T[]) => {
      setSaving(true)
      setError(null)
      try {
        await dbSet(key, next)
        setRuns(next)
      } catch (e) {
        setError((e as Error).message)
        throw e
      } finally {
        setSaving(false)
      }
    },
    [key],
  )

  const mutate = useCallback(
    async (fn: (runs: T[]) => T[]) => {
      setSaving(true)
      setError(null)
      try {
        const next = fn((await dbGet<T[]>(key)) ?? [])
        await dbSet(key, next)
        setRuns(next)
      } catch (e) {
        setError((e as Error).message)
        throw e
      } finally {
        setSaving(false)
      }
    },
    [key],
  )

  return { runs, loading, saving, error, reload, setAll, mutate }
}
