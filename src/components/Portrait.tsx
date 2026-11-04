import { useEffect, useRef, useState, type MouseEvent, type PointerEvent } from 'react'
import { createPortal } from 'react-dom'
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

export function Portrait({ id, size = 40, showName = false, className = '' }: Props) {
  const c = getCharacter(id)
  const { overrides } = usePortraits()
  const srcs = [overrides[id], c.portrait, c.portraitAlt].filter(Boolean) as string[]
  const [stage, setStage] = useState(0)
  const [enlarged, setEnlarged] = useState(false)
  const holdTimer = useRef<ReturnType<typeof setTimeout> | null>(null)
  const holdOrigin = useRef<{ x: number; y: number } | null>(null)
  const held = useRef(false)
  const suppressClick = useRef(false)

  useEffect(
    () => () => {
      if (holdTimer.current) clearTimeout(holdTimer.current)
    },
    [],
  )

  function cancelHold() {
    if (holdTimer.current) clearTimeout(holdTimer.current)
    holdTimer.current = null
  }

  function onPointerDown(e: PointerEvent<HTMLSpanElement>) {
    if (e.pointerType === 'mouse' && e.button !== 0) return
    holdOrigin.current = { x: e.clientX, y: e.clientY }
    e.currentTarget.setPointerCapture(e.pointerId)
    holdTimer.current = setTimeout(() => {
      held.current = true
      suppressClick.current = true
      setEnlarged(true)
    }, 400)
  }

  function onPointerMove(e: PointerEvent<HTMLSpanElement>) {
    const origin = holdOrigin.current
    if (origin && Math.hypot(e.clientX - origin.x, e.clientY - origin.y) > 12) {
      cancelHold()
      holdOrigin.current = null
    }
  }

  function onPointerUp() {
    cancelHold()
    holdOrigin.current = null
    if (held.current) {
      held.current = false
      setEnlarged(false)
    }
  }

  function onClick(e: MouseEvent<HTMLSpanElement>) {
    if (!suppressClick.current) return
    suppressClick.current = false
    e.preventDefault()
    e.stopPropagation()
  }

  const currentSrc = srcs[stage]
  return (
    <span
      className="portrait"
      title={`${c.label} — press and hold to enlarge`}
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={onPointerUp}
      onPointerCancel={() => {
        onPointerUp()
        suppressClick.current = false
      }}
      onClick={onClick}
      onContextMenu={(e) => e.preventDefault()}
    >
      {stage >= srcs.length ? (
        <PortraitFallback id={id} size={size} className={className} />
      ) : (
        <img
          src={currentSrc}
          alt={c.label}
          width={size}
          height={size}
          loading="lazy"
          className={className}
          onError={() => setStage((s) => s + 1)}
        />
      )}
      {showName && (
        <span className="portrait-name">
          <span className={`game-tag game-${c.game.toLowerCase()}`}>{c.game}</span> {c.name}
        </span>
      )}
      {enlarged &&
        createPortal(
          <div className="portrait-hold-preview" aria-hidden="true">
            {stage >= srcs.length ? (
              <PortraitFallback id={id} size={320} />
            ) : (
              <img src={currentSrc} alt="" />
            )}
          </div>,
          document.body,
        )}
    </span>
  )
}
