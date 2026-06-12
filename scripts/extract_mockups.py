"""Extract images from 1024px design mockups – native resolution, no upscale."""
from PIL import Image
import glob
import os

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))

HEROES = {
    "hero-home.jpg": ("d2d89e46", (0.0, 0.07, 1.0, 0.58)),
    "hero-climbing.jpg": ("282d1462", (0.0, 0.07, 1.0, 0.55)),
    "hero-membership.jpg": ("dc5cc015", (0.0, 0.07, 1.0, 0.48)),
    "hero-community.jpg": ("3bdf6976", (0.0, 0.07, 1.0, 0.40)),
    "hero-cafe.jpg": ("68bc86b2", (0.0, 0.12, 1.0, 0.78)),
    "hero-contact.jpg": ("8089fff5", (0.33, 0.08, 1.0, 0.92)),
}

GALLERY = [
    ("gallery-social.jpg", (0.02, 0.405, 0.25, 0.505)),
    ("gallery-coffee.jpg", (0.26, 0.405, 0.49, 0.505)),
    ("gallery-student.jpg", (0.51, 0.405, 0.74, 0.505)),
    ("gallery-competition.jpg", (0.75, 0.405, 0.98, 0.505)),
]


def find_mock(prefix):
    hits = glob.glob(os.path.join(OUT, f"*images_{prefix}*.png"))
    if not hits:
        raise FileNotFoundError(prefix)
    return hits[0]


def crop_ratio(img, box):
    w, h = img.size
    l, t, r, b = box
    return img.crop((int(l * w), int(t * h), int(r * w), int(b * h)))


def save(img, name, q=95):
    path = os.path.join(OUT, name)
    img.convert("RGB").save(path, "JPEG", quality=q, optimize=True)
    print(f"{name}\t{img.size}\t{os.path.getsize(path)//1024}KB")


def main():
    for name, (prefix, box) in HEROES.items():
        save(crop_ratio(Image.open(find_mock(prefix)), box), name)

    comm = Image.open(find_mock("3bdf6976"))
    for name, box in GALLERY:
        save(crop_ratio(comm, box), name)
    save(crop_ratio(comm, (0.54, 0.70, 0.98, 0.95)), "impact-group.jpg")


if __name__ == "__main__":
    main()
