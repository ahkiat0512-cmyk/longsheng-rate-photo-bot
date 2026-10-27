import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .config import Settings
from .service import process_message
from .webhook import extract_message, send_photo, send_text


OUTPUT_DIR = Path(os.environ.get("POSTER_OUTPUT_DIR", "/tmp/longsheng-posters"))


class TelegramWebhookHandler(BaseHTTPRequestHandler):
    def _respond(self, status: HTTPStatus) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    def do_GET(self) -> None:  # noqa: N802
        self._respond(HTTPStatus.OK if self.path == "/health" else HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        expected_secret = os.environ["TELEGRAM_WEBHOOK_SECRET"]
        if self.headers.get("X-Telegram-Bot-Api-Secret-Token") != expected_secret:
            self._respond(HTTPStatus.FORBIDDEN)
            return
        size = int(self.headers.get("Content-Length", "0"))
        try:
            update = json.loads(self.rfile.read(size))
        except json.JSONDecodeError:
            self._respond(HTTPStatus.BAD_REQUEST)
            return

        self._respond(HTTPStatus.OK)
        extracted = extract_message(update)
        if not extracted:
            return
        chat_id, text = extracted
        settings = Settings.from_environment()
        result = process_message(
            chat_id,
            text,
            settings,
            OUTPUT_DIR,
            on_processing=lambda: send_text(settings.bot_token, chat_id, "制作中，请稍候…"),
        )
        if result.kind == "poster" and result.image_path:
            try:
                send_photo(settings.bot_token, chat_id, result.image_path)
            finally:
                result.image_path.unlink(missing_ok=True)
        elif result.kind == "error" and result.message:
            send_text(settings.bot_token, chat_id, result.message)

    def log_message(self, _format: str, *_args: object) -> None:
        return


def run() -> None:
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), TelegramWebhookHandler)
    server.serve_forever()


if __name__ == "__main__":
    run()
