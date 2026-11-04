import { useEffect, useState } from 'react'
import { CoopView } from './components/CoopView'
import { Onboarding } from './components/Onboarding'
import { SettingsView } from './components/SettingsView'
import { SoloView } from './components/SoloView'
import { usePlayers } from './lib/usePlayers'
import { useRunStore } from './lib/useRunStore'
import type { CoopRun, SoloRun } from './types'

type Tab = 'coop' | 'solo' | 'settings'
const TABS: { id: Tab; label: string }[] = [
  { id: 'coop', label: 'Co-op' },
  { id: 'solo', label: 'Solo Deep' },
  { id: 'settings', label: 'Settings' },
]

function tabFromHash(): Tab {
  const h = window.location.hash.slice(1)
  return TABS.some((t) => t.id === h) ? (h as Tab) : 'coop'
}

export default function App() {
  const playersStore = usePlayers()
  const coop = useRunStore<CoopRun>('coop')
  const solo = useRunStore<SoloRun>('solo')
  const [tab, setTab] = useState<Tab>(tabFromHash)
  const [onboardingDismissed, setOnboardingDismissed] = useState(false)

  const players = playersStore.players ?? []
  const loading = coop.loading || solo.loading || playersStore.players === null
  const saving = coop.saving || solo.saving
  const error = coop.error ?? solo.error ?? playersStore.error
  const showOnboarding = playersStore.players !== null && playersStore.players.length === 0 && !onboardingDismissed

  useEffect(() => {
    const onHash = () => setTab(tabFromHash())
    window.addEventListener('hashchange', onHash)
    return () => window.removeEventListener('hashchange', onHash)
  }, [])

  return (
    <div className="app">
      <header className="hero" style={{ backgroundImage: `url(${import.meta.env.BASE_URL}img/hero.jpg)` }}>
        <div className="hero-inner">
          <img className="logo" src={`${import.meta.env.BASE_URL}img/logo.png`} alt="Streets of Rage 4" />
          <div className="hero-title">
            <h1>Survival Tracker</h1>
            <span className="sync-pill local">
              {saving ? 'Saving…' : loading ? 'Loading…' : '● Saved on this device'}
            </span>
          </div>
        </div>
        <nav className="tabs">
          {TABS.map((t) => (
            <a key={t.id} href={`#${t.id}`} className={tab === t.id ? 'active' : ''}>
              {t.label}
            </a>
          ))}
        </nav>
      </header>
      {error && (
        <div className="banner-error">
          {error}{' '}
          <button className="btn ghost small" onClick={() => void (coop.error ? coop.reload() : solo.reload())}>
            Retry
          </button>
        </div>
      )}
      <main>
        {tab === 'coop' && <CoopView store={coop} players={players} />}
        {tab === 'solo' && <SoloView store={solo} players={players} />}
        {tab === 'settings' && <SettingsView playersStore={playersStore} coop={coop} solo={solo} />}
      </main>
      {showOnboarding && <Onboarding onSave={playersStore.saveAll} onClose={() => setOnboardingDismissed(true)} />}
    </div>
  )
}
