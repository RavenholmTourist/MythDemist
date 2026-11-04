import { useState } from 'react'
import { getCharacter } from '../characters'
import { usePortraits } from '../lib/portraits'

interface Props {
  id: string
  size?: number
  showName?: boolean
  className?: string
}

/** Letter tile shown when no portrait image exists or it fails to load. */
export function PortraitFallback({ id, size = 40, className = '' }: Props) {
  const c = getCharacter(id)
  return (
    <span
      className={`portrait-fallback game-${c.game.toLowerCase()} ${className}`}
      style={{ width: size, height: size, fontSize: Math.round(size * 0.55) }}
      aria-label={c.label}
      role="img"
    >
      {c.name[0]}
    </span>
  )
}

export function Portrait({ id, size = 40, showName = false }: Props) {
  const c = getCharacter(id)
  const { overrides } = usePortraits()
  const srcs = [overrides[id], c.portrait, c.portraitAlt].filter(Boolean) as string[]
  const [stage, setStage] = useState(0)
  return (
    <span className="portrait" title={c.label}>
      {stage >= srcs.length ? (
        <PortraitFallback id={id} size={size} />
      ) : (
        <img
          src={srcs[stage]}
          alt={c.label}
          width={size}
          height={size}
          loading="lazy"
          onError={() => setStage((s) => s + 1)}
        />
      )}
      {showName && (
        <span className="portrait-name">
          <span className={`game-tag game-${c.game.toLowerCase()}`}>{c.game}</span> {c.name}
        </span>
      )}
    </span>
  )
}
