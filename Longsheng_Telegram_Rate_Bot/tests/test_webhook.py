import unittest

from longsheng_rate_bot.webhook import extract_message


class WebhookTests(unittest.TestCase):
    def test_extracts_chat_id_and_text_from_a_telegram_message_update(self) -> None:
        message = extract_message(
            {"update_id": 1, "message": {"chat": {"id": -1001234567890}, "text": "汇率内容"}}
        )

        self.assertEqual(message, (-1001234567890, "汇率内容"))

    def test_ignores_updates_without_a_text_message(self) -> None:
        self.assertIsNone(extract_message({"update_id": 1, "my_chat_member": {}}))
