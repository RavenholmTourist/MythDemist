import { PLAYER_COLORS } from '../lib/usePlayers'

export interface PlayerDraft {
  name: string
  color: string
}

interface Props {
  value: PlayerDraft
  onChange: (v: PlayerDraft) => void
  onRemove?: () => void
  autoFocus?: boolean
}

export function PlayerFields({ value, onChange, onRemove, autoFocus }: Props) {
  return (
    <div className="player-fields">
      <input
        placeholder="Player name"
        value={value.name}
        autoFocus={autoFocus}
        maxLength={24}
        onChange={(e) => onChange({ ...value, name: e.target.value })}
      />
      <div className="swatches" role="radiogroup" aria-label="Player colour">
        {PLAYER_COLORS.map((c) => (
          <button
            key={c}
            type="button"
            className={`swatch ${value.color === c ? 'active' : ''}`}
            style={{ background: c }}
            aria-label={`Colour ${c}`}
            onClick={() => onChange({ ...value, color: c })}
          />
        ))}
        <input
          type="color"
          className="swatch custom"
          title="Custom colour"
          value={value.color}
          onChange={(e) => onChange({ ...value, color: e.target.value })}
        />
      </div>
      {onRemove && (
        <button type="button" className="icon-btn" aria-label="Remove player" onClick={onRemove}>
          ✕
        </button>
      )}
    </div>
  )
}
