import { createContext, useCallback, useContext, useEffect, useRef, useState, type ReactNode } from 'react'
import { dbGet, dbSet, DB_KEYS } from './db'

interface PortraitsStore {
  /** Character id -> object URL for a user-uploaded portrait override. */
  overrides: Record<string, string>
  setOverride: (charId: string, blob: Blob) => Promise<void>
  removeOverride: (charId: string) => Promise<void>
}

const PortraitsContext = createContext<PortraitsStore>({ overrides: {}, setOverride: async () => {}, removeOverride: async () => {} })

export function usePortraits() {
  return useContext(PortraitsContext)
}

export function PortraitsProvider({ children }: { children: ReactNode }) {
  const [overrides, setOverrides] = useState<Record<string, string>>({})
  const urls = useRef<Record<string, string>>({})

  useEffect(() => {
    dbGet<Record<string, Blob>>(DB_KEYS.portraits)
      .then((stored) => {
        const next: Record<string, string> = {}
        for (const [id, blob] of Object.entries(stored ?? {})) next[id] = URL.createObjectURL(blob)
        urls.current = next
        setOverrides(next)
      })
      .catch(() => {})
    const owned = urls.current
    return () => Object.values(owned).forEach((u) => URL.revokeObjectURL(u))
  }, [])

  const setOverride = useCallback(async (charId: string, blob: Blob) => {
    const stored = (await dbGet<Record<string, Blob>>(DB_KEYS.portraits)) ?? {}
    await dbSet(DB_KEYS.portraits, { ...stored, [charId]: blob })
    setOverrides((cur) => {
      if (cur[charId]) URL.revokeObjectURL(cur[charId])
      const url = URL.createObjectURL(blob)
      urls.current = { ...urls.current, [charId]: url }
      return { ...cur, [charId]: url }
    })
  }, [])

  const removeOverride = useCallback(async (charId: string) => {
    const stored = (await dbGet<Record<string, Blob>>(DB_KEYS.portraits)) ?? {}
    delete stored[charId]
    await dbSet(DB_KEYS.portraits, stored)
    setOverrides((cur) => {
      if (cur[charId]) URL.revokeObjectURL(cur[charId])
      const next = { ...cur }
      delete next[charId]
      urls.current = next
      return next
    })
  }, [])

  return <PortraitsContext.Provider value={{ overrides, setOverride, removeOverride }}>{children}</PortraitsContext.Provider>
}
