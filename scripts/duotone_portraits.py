"""Generate stylized duotone character portraits.

Reads the wiki-sourced portraits from public/img/portraits/ and writes
consistent monochrome versions to public/img/portraits-duo/ (one colour per
game, centre-framed, SoR label underneath). Originals are never modified —
to roll back, point `portrait` in src/characters.ts back at portraits/.

Usage: python scripts/duotone_portraits.py
Requires: Pillow
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "public" / "img" / "portraits"
DST = ROOT / "public" / "img" / "portraits-duo"

SIZE = 192  # output is square
CROP = 0.88  # keep central 88% for tighter framing
LABEL_H = 30
FONT = "C:/Windows/Fonts/impact.ttf"

# Per-game colour (locked with owner): SoR1 red, SoR2 blue, SoR3 green, SoR4 yellow
GAMES = {
    "sor1": (255, 107, 107),
    "sor2": (94, 200, 255),
    "sor3": (139, 227, 107),
    "sor4": (255, 204, 0),
}

DARK = (12, 12, 16)
LIGHT = (240, 240, 246)


def duotone(path: Path, game: str, color: tuple[int, int, int]) -> Image.Image:
    img = Image.open(path).convert("L")
    side = min(img.size)
    crop = int(side * CROP)
    left = (img.width - crop) // 2
    top = (img.height - crop) // 2
    img = img.crop((left, top, left + crop, top + crop)).resize((SIZE, SIZE), Image.LANCZOS)
    duo = ImageOps.colorize(img, black=DARK, mid=color, white=LIGHT)

    draw = ImageDraw.Draw(duo, "RGBA")
    draw.rectangle((0, SIZE - LABEL_H, SIZE, SIZE), fill=(12, 12, 16, 200))
    font = ImageFont.truetype(FONT, 22)
    text = game.upper()
    tw = draw.textlength(text, font=font)
    draw.text(((SIZE - tw) / 2, SIZE - LABEL_H + 4), text, font=font, fill=color)
    return duo


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    for path in sorted(SRC.glob("*.png")):
        game = path.name.split("-")[0]
        if game not in GAMES:
            print(f"skip {path.name} (unknown game)")
            continue
        out = duotone(path, game, GAMES[game])
        out.save(DST / path.name)
        print(f"{path.name} -> duo")


if __name__ == "__main__":
    main()
