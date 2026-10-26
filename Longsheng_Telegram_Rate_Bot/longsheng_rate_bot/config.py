from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    bot_token: str
    allowed_chat_id: int

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            bot_token=os.environ["TELEGRAM_BOT_TOKEN"],
            allowed_chat_id=int(os.environ["ALLOWED_CHAT_ID"]),
        )


def is_allowed_chat(chat_id: int, settings: Settings) -> bool:
    return chat_id == settings.allowed_chat_id
