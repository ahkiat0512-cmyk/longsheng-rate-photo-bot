import unittest

from longsheng_rate_bot.parser import parse_rate_sheet


class ParserTests(unittest.TestCase):
    def test_parses_standard_longsheng_rate_message(self) -> None:
        sheet = parse_rate_sheet(
            """🐉 龙盛换汇｜每日汇率更新
📅 26/10/2026
🇲🇾 USDT ➡️ 马币转账
👤 4.040｜本地人户口
🌏 4.035｜外国人户口/TNG
💵 USDT ➡️ 马币现金
💰 4.045｜(5万以下)
💰 4.050｜(5-15万)
💰 4.055｜(15万或以上)
🇨🇳 USDT ➡️ 人民币
🔵 6.55｜支付宝
🏦 6.54｜银行卡（私户）"""
        )

        self.assertEqual(sheet.date, "26/10/2026")
        self.assertEqual(sheet.local_rate, "4.040")
        self.assertEqual(sheet.foreign_tng_rate, "4.035")
        self.assertEqual(sheet.cash_rates, ("4.045", "4.050", "4.055"))
        self.assertEqual(sheet.rmb_rates, ("6.55", "6.54"))
