"""Build uniform, transparent portrait review assets from selected cutouts."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "art-src" / "review-cutouts"
DEST = ROOT / "art-src" / "final-review"

CANVAS = 256
MAX_SUBJECT = 228
BASELINE_GAP = 14
NUMBER_SIZE = 120  # 2.5x the original 48px marker
NUMBER_COLORS = {
    "sor1": "#ff6b6b",
    "sor2": "#5ec8ff",
    "sor3": "#8be36b",
    "sor4": "#ffcc00",
}

# Preserve pixel edges for the game-sprite profiles; use smooth scaling for
# painted illustrations. Roo and Zan are the SoR3 painted-art exceptions.
PALETTE_ART = {"sor3-roo", "sor3-zan"}


def font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/impact.ttf"),
        Path("C:/Windows/Fonts/ariblk.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def normalize(source_path: Path) -> Image.Image:
    source = Image.open(source_path).convert("RGBA")
    if source_path.stem == "sor2-skate":
        # The game sprite has the same pale-green background in the gap
        # between Skate's legs; clear matching pixels there as well as outside.
        pixels = source.load()
        bg = pixels[0, 0][:3]
        for y in range(source.height):
            for x in range(source.width):
                r, g, b, _ = pixels[x, y]
                if max(abs(r - bg[0]), abs(g - bg[1]), abs(b - bg[2])) <= 24:
                    pixels[x, y] = (r, g, b, 0)
    bbox = source.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError(f"{source_path.name} is fully transparent")
    subject = source.crop(bbox)

    scale = min(MAX_SUBJECT / subject.width, MAX_SUBJECT / subject.height)
    size = (max(1, round(subject.width * scale)), max(1, round(subject.height * scale)))
    resampling = Image.Resampling.LANCZOS if source_path.stem in PALETTE_ART or source_path.stem.startswith("sor4-") else Image.Resampling.NEAREST
    subject = subject.resize(size, resampling)

    canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    x = (CANVAS - subject.width) // 2
    y = CANVAS - BASELINE_GAP - subject.height
    canvas.alpha_composite(subject, (x, y))

    game = source_path.stem.split("-", 1)[0]
    number = game[-1]
    draw = ImageDraw.Draw(canvas)
    typeface = font(NUMBER_SIZE)
    bounds = draw.textbbox((0, 0), number, font=typeface, stroke_width=3)
    tx = 8 - bounds[0]
    ty = CANVAS - BASELINE_GAP - bounds[3]
    draw.text(
        (tx, ty),
        number,
        font=typeface,
        fill=NUMBER_COLORS[game],
        stroke_width=3,
        stroke_fill=(12, 12, 16, 245),
    )
    return canvas


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    files = sorted(SOURCE.glob("*.png"))
    if len(files) != 21:
        raise SystemExit(f"Expected 21 selected cutouts in {SOURCE}, found {len(files)}")

    for path in files:
        out = normalize(path)
        target = DEST / path.name
        out.save(target, optimize=True)
        print(f"{path.name}: {Image.open(path).size} -> {out.size} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
