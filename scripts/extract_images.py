"""Extract hero & gallery photos from design mockup PNGs."""
from PIL import Image
import os
import glob

BASE = os.path.join(os.path.dirname(__file__), "..", "images")
BASE = os.path.abspath(BASE)


def find_mock(prefix: str) -> str:
    matches = glob.glob(os.path.join(BASE, f"*images_{prefix}*.png"))
    if not matches:
        raise FileNotFoundError(prefix)
    return matches[0]


def save_crop(box, src_prefix, out_name, quality=90):
    path = find_mock(src_prefix)
    img = Image.open(path).convert("RGB")
    w, h = img.size
    # box: left, top, right, bottom (absolute or ratio)
    if all(0 <= v <= 1 for v in box):
        l, t, r, b = box
        box = (int(l * w), int(t * h), int(r * w), int(b * h))
    cropped = img.crop(box)
    # upscale to reasonable hero size
    target_w = 1920
    if cropped.width < target_w:
        ratio = target_w / cropped.width
        cropped = cropped.resize((target_w, int(cropped.height * ratio)), Image.LANCZOS)
    out = os.path.join(BASE, out_name)
    cropped.save(out, "JPEG", quality=quality, optimize=True)
    print(f"Saved {out_name} from {os.path.basename(path)} {box} -> {cropped.size}")


# Photo-heavy regions (avoid baked-in headline text)
CROPS = [
    # heroes – prefer photo areas without overlay text
    ((0.48, 0.08, 1.0, 0.62), "d2d89e46", "hero-home.jpg"),
    ((0.48, 0.08, 1.0, 0.58), "282d1462", "hero-climbing.jpg"),
    ((0.38, 0.08, 1.0, 0.52), "dc5cc015", "hero-membership.jpg"),
    ((0.32, 0.07, 1.0, 0.37), "3bdf6976", "hero-community.jpg"),
    ((0.0, 0.16, 1.0, 0.98), "68bc86b2", "hero-cafe.jpg"),
    ((0.40, 0.08, 1.0, 0.92), "8089fff5", "hero-contact.jpg"),
    # community gallery – thumbnail images only
    ((0.02, 0.405, 0.25, 0.505), "3bdf6976", "gallery-social.jpg"),
    ((0.26, 0.405, 0.49, 0.505), "3bdf6976", "gallery-coffee.jpg"),
    ((0.51, 0.405, 0.74, 0.505), "3bdf6976", "gallery-student.jpg"),
    ((0.75, 0.405, 0.98, 0.505), "3bdf6976", "gallery-competition.jpg"),
    # community impact group photo
    ((0.54, 0.70, 0.98, 0.95), "3bdf6976", "impact-group.jpg"),
]

if __name__ == "__main__":
    for box, prefix, name in CROPS:
        save_crop(box, prefix, name)
