from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .models import RateSheet


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "assets" / "longsheng-template.png"
OUTPUT_SIZE = (1882, 3344)

REGULAR_FONT_CANDIDATES = (
    ROOT / "assets" / "NotoSansCJKsc-Regular.otf",
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
)
BOLD_FONT_CANDIDATES = (
    ROOT / "assets" / "NotoSansCJKsc-Bold.otf",
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
    Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = BOLD_FONT_CANDIDATES if bold else REGULAR_FONT_CANDIDATES
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size, index=0)
    return ImageFont.load_default()


def _center(
    draw: ImageDraw.ImageDraw,
    y: int,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: str,
    *,
    stroke_width: int = 1,
    stroke_fill: str = "#130b02",
) -> None:
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    x = (OUTPUT_SIZE[0] - (box[2] - box[0])) // 2
    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)


def _row(draw: ImageDraw.ImageDraw, y: int, rate: str, label: str, *, label_size: int = 37) -> None:
    draw.rounded_rectangle(
        (92, y, 1790, y + 76),
        radius=18,
        fill="#080d19",
        outline="#d8a72c",
        width=3,
    )
    draw.text((126, y + 9), rate, font=_font(52, True), fill="#ffdc65", stroke_width=1, stroke_fill="#8a5a09")
    draw.text((446, y + 17), label, font=_font(label_size, True), fill="#ffffff")


def _note(draw: ImageDraw.ImageDraw, y: int, text: str, *, fill: str = "#f8f2de", size: int = 26) -> None:
    draw.text((118, y), text, font=_font(size), fill=fill)


def render_poster(sheet: RateSheet, output_path: Path) -> Path:
    """Render one crisp, fixed-layout 龙盛 poster with programmatic rate text."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.open(TEMPLATE).convert("RGB").resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(image)
    gold = "#ffe17a"

    # Header plaque. The Dragon/KL image itself remains untouched.
    _center(draw, 970, "龙盛换汇", _font(54, True), gold, stroke_width=2)
    _center(draw, 1034, "LONG SHENG EXCHANGE", _font(29, True), "#fff0aa")

    # Blue: USDT to MYR transfer.
    _center(draw, 1153, "每日汇率更新", _font(39, True), gold)
    _center(draw, 1201, sheet.date, _font(32, True), "#ffffff")
    _center(draw, 1251, "USDT → 马币转账", _font(43, True), gold)
    _row(draw, 1321, sheet.local_rate, "本地人户口")
    _row(draw, 1412, sheet.foreign_tng_rate, "外国人户口/TNG")
    _note(draw, 1512, "▲ 不转 Wise、JP Morgan、BigPay、Bank of China")
    _note(draw, 1552, "▲ 单笔最低金额：RM1,000")
    _note(draw, 1592, "▲ 律师、开发商及车商户口，请另询汇率")

    # Green: MYR cash.
    _center(draw, 1789, "USDT → 马币现金", _font(43, True), gold)
    _note(draw, 1845, "汇率实时更新，交易前请提前锁价", fill="#fff0aa", size=27)
    _row(draw, 1898, sheet.cash_rates[0], "5万以下")
    _row(draw, 1988, sheet.cash_rates[1], "5-15万")
    _row(draw, 2078, sheet.cash_rates[2], "15万或以上")
    _note(draw, 2184, "马币现金 RM30,000 或以上｜吉隆坡免费派送")
    _note(draw, 2224, "▲ RM30,000 以下需自取；如需派送，每趟 RM100（吉隆坡）", size=24)

    # Red: USDT to CNY.
    _center(draw, 2390, "USDT → 人民币", _font(43, True), gold)
    _row(draw, 2455, sheet.rmb_rates[0], "支付宝")
    _row(draw, 2545, sheet.rmb_rates[1], "银行卡（私户）")
    _note(draw, 2650, "▲ 单笔最低金额：人民币 2,000")
    _note(draw, 2690, "▲ 公对公转账，请另询汇率")

    # Footer.
    _center(draw, 3007, "官方频道  https://t.me/longshengKL", _font(26, True), "#ffffff")
    _center(draw, 3051, "认准客服  @LSxiaofu  @vyvyfish", _font(28, True), gold)
    _center(draw, 3120, "安全 · 快捷 · 诚信", _font(32, True), gold)

    image.save(output_path, format="PNG", optimize=True)
    return output_path
