import unittest

from longsheng_rate_bot.config import Settings, is_allowed_chat


class WhitelistTests(unittest.TestCase):
    def test_only_configured_group_is_allowed(self) -> None:
        settings = Settings(bot_token="test-token", allowed_chat_id=-1001234567890)

        self.assertTrue(is_allowed_chat(-1001234567890, settings))
        self.assertFalse(is_allowed_chat(-1009876543210, settings))
        self.assertFalse(is_allowed_chat(8319094308, settings))
