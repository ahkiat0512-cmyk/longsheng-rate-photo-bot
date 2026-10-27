import tempfile
import unittest
from pathlib import Path

from longsheng_rate_bot.config import Settings
from longsheng_rate_bot.service import process_message


VALID = """📅 26/10/2026
USDT ➡️ 马币转账
4.040｜本地人户口
4.035｜外国人户口/TNG
USDT ➡️ 马币现金
4.045｜5万以下
4.050｜5-15万
4.055｜15万或以上
USDT ➡️ 人民币
6.55｜支付宝
6.54｜银行卡（私户）"""


class ServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = Settings("test-token", -1001234567890)

    def test_ignores_message_from_other_group(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = process_message(-1009999999999, VALID, self.settings, Path(temp_dir))

        self.assertEqual(result.kind, "ignored")
        self.assertIsNone(result.image_path)

    def test_generates_poster_for_valid_message_in_allowed_group(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = process_message(-1001234567890, VALID, self.settings, Path(temp_dir))

            self.assertEqual(result.kind, "poster")
            self.assertIsNotNone(result.image_path)
            self.assertTrue(result.image_path.exists())

    def test_notifies_processing_before_rendering_a_valid_poster(self) -> None:
        events: list[str] = []

        with tempfile.TemporaryDirectory() as temp_dir:
            result = process_message(
                -1001234567890,
                VALID,
                self.settings,
                Path(temp_dir),
                on_processing=lambda: events.append("processing"),
            )

        self.assertEqual(result.kind, "poster")
        self.assertEqual(events, ["processing"])
