from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .models import RateSheet


ROOT = Path(__file__).resolve().parent.parent
# Approved black-and-gold artwork.  It already contains every label, icon,
# notice and contact detail; the bot only replaces daily values.
TEMPLATE = ROOT / "assets" / "longsheng-mobile-template.jpg"
# GitHub's web uploader places a selected image directly in the service root.
# Support that location too, so the same revision works with the upload flow.
if not TEMPLATE.exists():
    TEMPLATE = ROOT / "longsheng-mobile-template.jpg"
OUTPUT_SIZE = (1024, 1536)

FONT_CANDIDATES = (
    ROOT / "assets" / "NotoSansCJKsc-Bold.otf",
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
    Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
)


def _font(size: int) -> ImageFont.FreeTypeFont:
    for candidate in FONT_CANDIDATES:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size, index=0)
    return ImageFont.load_default()


def _centered_text(draw: ImageDraw.ImageDraw, text: str, y: int, font: ImageFont.FreeTypeFont) -> None:
    box = draw.textbbox((0, 0), text, font=font, stroke_width=1)
    x = (OUTPUT_SIZE[0] - (box[2] - box[0])) // 2
    draw.text((x, y), text, font=font, fill="#fff0b0", stroke_width=1, stroke_fill="#3d2100")


def _rate(
    image: Image.Image,
    draw: ImageDraw.ImageDraw,
    y: int,
    value: str,
    *,
    text_x: int = 100,
    cover_x: int = 65,
    cover_width: int = 200,
    texture_x: int = 242,
) -> None:
    """Replace only a number field; all approved surrounding artwork remains."""
    # Reuse a clean sliver of the original panel texture rather than painting a
    # flat box over it. This preserves the black/gold artwork around the rate.
    texture = image.crop((texture_x, y, texture_x + 4, y + 58)).resize(
        (cover_width, 58), Image.Resampling.BILINEAR
    )
    image.paste(texture, (cover_x, y))
    draw.text(
        (text_x, y - 2),
        value,
        font=_font(48),
        fill="#ffe374",
        stroke_width=1,
        stroke_fill="#705000",
    )


def render_poster(sheet: RateSheet, output_path: Path) -> Path:
    """Render the approved mobile poster and update only the daily values."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.open(TEMPLATE).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Date plaque.
    draw.rectangle((384, 491, 640, 528), fill="#0b0907")
    _centered_text(draw, sheet.date, 492, _font(30))

    # Blue panel: USDT → MYR bank transfer.
    _rate(image, draw, 651, sheet.local_rate)
    _rate(image, draw, 723, sheet.foreign_tng_rate)

    # Green panel: USDT → MYR cash.
    _rate(image, draw, 962, sheet.cash_rates[0], texture_x=240)
    _rate(image, draw, 1024, sheet.cash_rates[1], texture_x=240)
    _rate(image, draw, 1086, sheet.cash_rates[2], texture_x=240)

    # Red panel: USDT → RMB.
    _rate(
        image, draw, 1252, sheet.rmb_rates[0], text_x=115, cover_x=80, cover_width=170, texture_x=244
    )
    _rate(
        image, draw, 1314, sheet.rmb_rates[1], text_x=115, cover_x=80, cover_width=170, texture_x=244
    )

    image.save(output_path, format="PNG", optimize=True)
    return output_path
