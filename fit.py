import io

# Optional: Pillow powers the fit-to-screen resize/crop. Without it we fall
# back to uploading images untouched, preserving the original behaviour.
try:
    from PIL import Image, ImageOps
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def fit_to_tv(data, target, fit='cover'):
    """Return JPEG bytes resized/cropped to the TV screen, or None to skip.

    * ``cover`` (default) center-crops the image to fill the target.
    * ``contain`` shows the whole image, centred on white.

    Returns None (meaning 'upload untouched') if Pillow is unavailable or the
    image cannot be decoded, so a single bad image never breaks a run.
    """
    if not HAS_PIL:
        return None
    try:
        img = Image.open(io.BytesIO(data))
        img = ImageOps.exif_transpose(img)
        img = img.convert('RGB')
        width, height = (int(p) for p in target.lower().split('x'))
        if fit == 'contain':
            img.thumbnail((width, height), Image.LANCZOS)
            canvas = Image.new('RGB', (width, height), (255, 255, 255))
            canvas.paste(img, ((width - img.width) // 2, (height - img.height) // 2))
            img = canvas
        else:
            img = ImageOps.fit(img, (width, height), Image.LANCZOS, centering=(0.5, 0.5))
        buf = io.BytesIO()
        img.save(buf, 'JPEG', quality=95)
        return buf.getvalue()
    except Exception:
        return None