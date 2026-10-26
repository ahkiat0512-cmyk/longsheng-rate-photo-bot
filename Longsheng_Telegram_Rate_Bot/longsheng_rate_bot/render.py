from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .models import RateSheet


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "assets" / "longsheng-template.png"
FONT_CANDIDATES = (
    ROOT / "assets" / "NotoSansCJKsc-Regular.otf",
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    for candidate in FONT_CANDIDATES:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size, index=0)
    return ImageFont.load_default()


def _center(draw: ImageDraw.ImageDraw, y: int, text: str, font: ImageFont.FreeTypeFont, fill: str) -> None:
    box = draw.textbbox((0, 0), text, font=font, stroke_width=1)
    x = (2048 - (box[2] - box[0])) // 2
    draw.text((x, y), text, font=font, fill=fill, stroke_width=2, stroke_fill="#140d03")


def _row(
    draw: ImageDraw.ImageDraw,
    y: int,
    rate: str,
    label: str,
    text_size: int = 50,
) -> None:
    draw.rounded_rectangle((110, y, 1938, y + 108), radius=26, fill="#080d19", outline="#d8a72c", width=3)
    draw.text((145, y + 13), rate, font=_font(64, True), fill="#ffdc65", stroke_width=1, stroke_fill="#8a5a09")
    draw.text((480, y + 22), label, font=_font(text_size), fill="#ffffff")


def _note(draw: ImageDraw.ImageDraw, y: int, text: str, fill: str = "#f8f2de") -> None:
    draw.text((130, y), text, font=_font(31), fill=fill)


def render_poster(sheet: RateSheet, output_path: Path) -> Path:
    """Render one stable 2K portrait poster from a parsed RateSheet."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.open(TEMPLATE).convert("RGB").resize((2048, 3072), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(image)

    gold = "#ffe17a"
    _center(draw, 820, "龙盛换汇", _font(98, True), gold)
    _center(draw, 940, "LONG SHENG EXCHANGE", _font(42, True), gold)
    _center(draw, 1035, "每日汇率更新", _font(56, True), gold)
    _center(draw, 1125, sheet.date, _font(48, True), "#ffffff")

    _center(draw, 1180, "USDT ➜ 马币转账", _font(54, True), gold)
    _row(draw, 1275, sheet.local_rate, "本地人户口")
    _row(draw, 1400, sheet.foreign_tng_rate, "外国人户口/TNG")
    _note(draw, 1535, "⚠ 不转 Wise、JP Morgan、BigPay、Bank of China")
    _note(draw, 1590, "⚠ 单笔最低金额：RM1,000")
    _note(draw, 1645, "⚠ 律师、开发商及车商户口，请另询汇率")

    _center(draw, 1765, "USDT ➜ 马币现金", _font(54, True), gold)
    _note(draw, 1840, "汇率实时更新，交易前请提前锁价", "#fff0aa")
    _row(draw, 1900, sheet.cash_rates[0], "5万以下")
    _row(draw, 2025, sheet.cash_rates[1], "5-15万")
    _row(draw, 2150, sheet.cash_rates[2], "15万或以上")
    _note(draw, 2280, "🚗 马币现金 RM30,000 或以上｜吉隆坡免费派送")
    _note(draw, 2335, "⚠ RM30,000 以下需自取；如需派送，每趟 RM100（吉隆坡）")

    _center(draw, 2435, "USDT ➜ 人民币", _font(54, True), gold)
    _row(draw, 2515, sheet.rmb_rates[0], "支付宝")
    _row(draw, 2640, sheet.rmb_rates[1], "银行卡（私户）")
    _note(draw, 2765, "⚠ 单笔最低金额：人民币 2,000")
    _note(draw, 2820, "⚠ 公对公转账，请另询汇率")

    _center(draw, 2895, "官方频道  https://t.me/longshengKL", _font(32), "#ffffff")
    _center(draw, 2950, "认准客服  @LSxiaofu  @vyvyfish", _font(34), gold)
    _center(draw, 3005, "安全 · 快捷 · 诚信", _font(38, True), gold)

    image.save(output_path, format="PNG", optimize=True)
    return output_path
