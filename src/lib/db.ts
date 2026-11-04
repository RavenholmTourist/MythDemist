const DB_NAME = 'sor4-survival-tracker'
const STORE = 'kv'

let dbPromise: Promise<IDBDatabase> | null = null

function openDb(): Promise<IDBDatabase> {
  // One shared connection for the app's lifetime — closing it per-transaction
  // leaves later calls with a closing connection.
  dbPromise ??= new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1)
    req.onupgradeneeded = () => req.result.createObjectStore(STORE)
    req.onsuccess = () => {
      req.result.onversionchange = () => req.result.close()
      resolve(req.result)
    }
    req.onerror = () => reject(req.error)
  })
  return dbPromise
}

async function tx<T>(mode: IDBTransactionMode, fn: (s: IDBObjectStore) => IDBRequest<T>): Promise<T> {
  const db = await openDb()
  return new Promise((resolve, reject) => {
    const t = db.transaction(STORE, mode)
    const req = fn(t.objectStore(STORE))
    req.onsuccess = () => resolve(req.result)
    req.onerror = () => reject(req.error)
    t.onerror = () => reject(t.error)
  })
}

export const dbGet = <T>(key: string) => tx<T | undefined>('readonly', (s) => s.get(key))
export const dbSet = (key: string, value: unknown) => tx('readwrite', (s) => s.put(value, key))
export const dbDel = (key: string) => tx('readwrite', (s) => s.delete(key))

export const DB_KEYS = {
  coopRuns: 'runs:coop',
  soloRuns: 'runs:solo',
  players: 'players',
  portraits: 'portraits',
} as const

// Ask the browser not to evict stored data under storage pressure.
if (typeof navigator !== 'undefined') void navigator.storage?.persist?.()
