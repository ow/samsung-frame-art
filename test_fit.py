import io
import unittest

from fit import HAS_PIL, fit_to_tv

try:
    from PIL import Image
except ImportError:
    Image = None


def _png(size, mode='RGB', color=(200, 30, 30)):
    buf = io.BytesIO()
    Image.new(mode, size, color).save(buf, 'PNG')
    return buf.getvalue()


def _jpg_size(data):
    return Image.open(io.BytesIO(data)).size


@unittest.skipUnless(HAS_PIL, 'Pillow not installed')
class FitToTvTest(unittest.TestCase):
    def test_cover_landscape(self):
        self.assertEqual(_jpg_size(fit_to_tv(_png((8000, 1000)), '3840x2160', 'cover')),
                         (3840, 2160))

    def test_cover_portrait(self):
        self.assertEqual(_jpg_size(fit_to_tv(_png((1000, 8000)), '3840x2160', 'cover')),
                         (3840, 2160))

    def test_cover_default_fit(self):
        self.assertEqual(_jpg_size(fit_to_tv(_png((8000, 1000)), '3840x2160')),
                         (3840, 2160))

    def test_contain_landscape(self):
        self.assertEqual(_jpg_size(fit_to_tv(_png((8000, 1000)), '3840x2160', 'contain')),
                         (3840, 2160))

    def test_contain_4x3(self):
        self.assertEqual(_jpg_size(fit_to_tv(_png((1200, 900)), '3840x2160', 'contain')),
                         (3840, 2160))

    def test_rgba_png(self):
        self.assertEqual(_jpg_size(fit_to_tv(_png((1920, 1080), mode='RGBA'), '3840x2160', 'cover')),
                         (3840, 2160))

    def test_custom_resolution(self):
        self.assertEqual(_jpg_size(fit_to_tv(_png((8000, 1000)), '1920x1080', 'cover')),
                         (1920, 1080))

    def test_uppercase_target(self):
        self.assertEqual(_jpg_size(fit_to_tv(_png((8000, 1000)), '3840X2160', 'cover')),
                         (3840, 2160))

    def test_invalid_image_returns_none(self):
        self.assertIsNone(fit_to_tv(b'not an image', '3840x2160', 'cover'))

    def test_contain_does_not_crop(self):
        # 4:3 image should be letterboxed whole, not cropped, in contain mode
        out = fit_to_tv(_png((1200, 900)), '3840x2160', 'contain')
        img = Image.open(io.BytesIO(out))
        self.assertEqual(img.size, (3840, 2160))
        # the original 4:3 content must still be visible: black/white bars,
        # but the centre pixel should be the original colour (red).
        self.assertEqual(img.getpixel((1920, 1080)), (200, 30, 30))


if __name__ == '__main__':
    unittest.main()