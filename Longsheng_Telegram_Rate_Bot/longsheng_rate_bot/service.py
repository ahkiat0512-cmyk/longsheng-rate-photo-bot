from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from .config import Settings, is_allowed_chat
from .parser import RateSheetError, parse_rate_sheet
from .render import render_poster


@dataclass(frozen=True)
class ProcessResult:
    kind: str
    message: str | None = None
    image_path: Path | None = None


def process_message(
    chat_id: int,
    text: str | None,
    settings: Settings,
    output_dir: Path,
) -> ProcessResult:
    if not is_allowed_chat(chat_id, settings):
        return ProcessResult(kind="ignored")
    if not text or "马币转账" not in text:
        return ProcessResult(kind="ignored")
    try:
        sheet = parse_rate_sheet(text)
    except RateSheetError as error:
        return ProcessResult(kind="error", message=f"汇率格式不完整：{error}")

    output_dir.mkdir(parents=True, exist_ok=True)
    image_path = render_poster(sheet, output_dir / f"longsheng-{uuid4().hex}.png")
    return ProcessResult(kind="poster", image_path=image_path)
