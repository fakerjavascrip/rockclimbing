"""Extract hero & gallery images from full-page design mockups (399x279)."""
from PIL import Image
import os

ASSETS = r"C:\Users\Lenovo\.cursor\projects\c-Users-Lenovo-Desktop-Yinc1009\assets"
OUT = os.path.join(os.path.dirname(__file__), "..", "images")

FILES = {
    "hero-home.jpg": "c__Users_Lenovo_AppData_Roaming_Cursor_User_workspaceStorage_ba510dc1cc60771f095dbd9468bc410c_images_image-c121f2af-64a5-4f72-9b5f-1cc37bd725ea.png",
    "hero-climbing.jpg": "c__Users_Lenovo_AppData_Roaming_Cursor_User_workspaceStorage_ba510dc1cc60771f095dbd9468bc410c_images_image-fe98be63-f7d6-4622-a2e1-265b715621f7.png",
    "hero-membership.jpg": "c__Users_Lenovo_AppData_Roaming_Cursor_User_workspaceStorage_ba510dc1cc60771f095dbd9468bc410c_images_image-24770fd5-d525-43e7-aaa6-0a34763ddd54.png",
    "hero-community.jpg": "c__Users_Lenovo_AppData_Roaming_Cursor_User_workspaceStorage_ba510dc1cc60771f095dbd9468bc410c_images_image-1bcfe761-c8a6-421a-8fbd-c20e82d0322d.png",
    "hero-cafe.jpg": "c__Users_Lenovo_AppData_Roaming_Cursor_User_workspaceStorage_ba510dc1cc60771f095dbd9468bc410c_images_image-bdbfa5e6-43c7-49af-8190-11451d82ef58.png",
    "hero-contact.jpg": "c__Users_Lenovo_AppData_Roaming_Cursor_User_workspaceStorage_ba510dc1cc60771f095dbd9468bc410c_images_image-3fc5e899-ca41-4247-8918-08ec38bf4e18.png",
}

# Normalized crop boxes (left, top, right, bottom)
HERO_CROPS = {
    "hero-home.jpg": (0.0, 0.12, 1.0, 0.58),
    "hero-climbing.jpg": (0.0, 0.10, 1.0, 0.72),
    "hero-membership.jpg": (0.0, 0.10, 1.0, 0.55),
    "hero-community.jpg": (0.0, 0.10, 1.0, 0.72),
    "hero-cafe.jpg": (0.0, 0.10, 1.0, 0.72),
    "hero-contact.jpg": (0.22, 0.10, 1.0, 0.92),  # right panel storefront photo
}

COMMUNITY_CARDS = [
    ("gallery-social.jpg", (0.03, 0.72, 0.26, 0.98)),
    ("gallery-beginner.jpg", (0.27, 0.72, 0.50, 0.98)),
    ("gallery-competition.jpg", (0.51, 0.72, 0.74, 0.98)),
    ("gallery-outdoor.jpg", (0.75, 0.72, 0.98, 0.98)),
]

TARGET_W = 1920


def crop(img, box):
    w, h = img.size
    l, t, r, b = box
    return img.crop((int(l * w), int(t * h), int(r * w), int(b * h)))


def upscale(img, width=TARGET_W):
    if img.width >= width:
        return img
    ratio = width / img.width
    return img.resize((width, int(img.height * ratio)), Image.LANCZOS)


def save(img, name, q=92):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    img.convert("RGB").save(path, "JPEG", quality=q, optimize=True)
    print(f"{name}\t{img.size}\t{os.path.getsize(path) // 1024}KB")


def main():
    for out, fname in FILES.items():
        path = os.path.join(ASSETS, fname)
        if not os.path.isfile(path):
            print("MISSING", fname)
            continue
        im = Image.open(path)
        box = HERO_CROPS.get(out, (0.0, 0.10, 1.0, 0.65))
        save(upscale(crop(im, box)), out)

    comm = os.path.join(ASSETS, FILES["hero-community.jpg"])
    if os.path.isfile(comm):
        im = Image.open(comm)
        for name, box in COMMUNITY_CARDS:
            c = upscale(crop(im, box), 480)
            save(c, name)


if __name__ == "__main__":
    main()
