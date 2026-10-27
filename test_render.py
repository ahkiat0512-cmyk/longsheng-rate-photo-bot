import tempfile
import unittest
from pathlib import Path

from PIL import Image

from longsheng_rate_bot.models import RateSheet
from longsheng_rate_bot.render import TEMPLATE, render_poster


class PosterRenderTests(unittest.TestCase):
    def test_renders_a_high_resolution_portrait_png(self) -> None:
        sheet = RateSheet(
            date="26/10/2026",
            local_rate="4.040",
            foreign_tng_rate="4.035",
            cash_rates=("4.045", "4.050", "4.055"),
            rmb_rates=("6.55", "6.54"),
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            output = render_poster(sheet, Path(temp_dir) / "poster.png")
            with Image.open(output) as image:
                self.assertEqual(image.format, "PNG")
                self.assertGreater(image.height, image.width)
                self.assertEqual(image.size, (1882, 3344))
                self.assertEqual(image.size[0] / image.size[1], 941 / 1672)

            with Image.open(TEMPLATE) as template:
                self.assertEqual(template.size, (941, 1672))
