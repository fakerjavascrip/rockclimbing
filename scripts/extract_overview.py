"""Extract hero photos from design-overview.png (matches spec sheet)."""
from PIL import Image
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
OVERVIEW = os.path.join(ROOT, "design-overview.png")

# grid on 1024x682 overview
TOP, ROW_H, COL_W = 236, 223, 341

# hero crop inside each thumb: (x0,y0,x1,y1) relative to thumb origin
HERO_IN_THUMB = {
    "home": (0, 26, 341, 118),
    "climbing": (0, 26, 341, 118),
    "membership": (0, 26, 341, 118),
    "community": (0, 26, 341, 118),
    "cafe": (0, 26, 341, 118),
    "contact": (120, 26, 341, 118),
}

# gallery inside community thumb (overview uses 4 vertical event cards)
GALLERY = [
    ("gallery-social.jpg", (10, 118, 82, 198)),
    ("gallery-beginner.jpg", (86, 118, 158, 198)),
    ("gallery-competition.jpg", (162, 118, 234, 198)),
    ("gallery-outdoor.jpg", (238, 118, 310, 198)),
]

PAGES = [
    ("hero-home.jpg", 0, 0),
    ("hero-climbing.jpg", 1, 0),
    ("hero-membership.jpg", 2, 0),
    ("hero-community.jpg", 0, 1),
    ("hero-cafe.jpg", 1, 1),
    ("hero-contact.jpg", 2, 1),
]
NAMES = ["home", "climbing", "membership", "community", "cafe", "contact"]


def upscale(img, tw=1920):
    s = tw / img.width
    return img.resize((tw, max(1, int(img.height * s))), Image.LANCZOS)


def main():
    im = Image.open(OVERVIEW)
    for (out, col, row), name in zip(PAGES, NAMES):
        tx, ty = col * COL_W, TOP + row * ROW_H
        thumb = im.crop((tx, ty, tx + COL_W, ty + ROW_H))
        x0, y0, x1, y1 = HERO_IN_THUMB[name]
        hero = thumb.crop((x0, y0, x1, y1))
        upscale(hero).convert("RGB").save(os.path.join(ROOT, out), "JPEG", quality=94)
        print(out, hero.size)

    cx, cy = 0, TOP + ROW_H
    comm = im.crop((cx, cy, cx + COL_W, cy + ROW_H))
    for fname, box in GALLERY:
        g = upscale(comm.crop(box), 960)
        g.convert("RGB").save(os.path.join(ROOT, fname), "JPEG", quality=94)
        print(fname, comm.crop(box).size)


if __name__ == "__main__":
    main()
