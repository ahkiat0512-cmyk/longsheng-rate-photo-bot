import json
import mimetypes
import secrets
import urllib.request
from pathlib import Path
from typing import Any


def extract_message(update: dict[str, Any]) -> tuple[int, str] | None:
    message = update.get("message")
    if not isinstance(message, dict):
        return None
    chat = message.get("chat")
    text = message.get("text")
    if not isinstance(chat, dict) or not isinstance(chat.get("id"), int) or not isinstance(text, str):
        return None
    return chat["id"], text


def _multipart(field_name: str, file_path: Path) -> tuple[bytes, str]:
    boundary = f"----Longsheng{secrets.token_hex(16)}"
    mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    head = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field_name}"; filename="{file_path.name}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode()
    body = head + file_path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    return body, boundary


def send_photo(bot_token: str, chat_id: int, image_path: Path) -> None:
    body, boundary = _multipart("photo", image_path)
    endpoint = f"https://api.telegram.org/bot{bot_token}/sendPhoto?chat_id={chat_id}"
    request = urllib.request.Request(
        endpoint,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.loads(response.read())
    if not payload.get("ok"):
        raise RuntimeError(f"Telegram sendPhoto failed: {payload}")


def send_text(bot_token: str, chat_id: int, text: str) -> None:
    body = json.dumps({"chat_id": chat_id, "text": text}).encode()
    endpoint = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    request = urllib.request.Request(
        endpoint,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read())
    if not payload.get("ok"):
        raise RuntimeError(f"Telegram sendMessage failed: {payload}")
