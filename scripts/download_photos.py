"""Download high-resolution hero photos matching each page theme."""
import os
import urllib.request

OUT = os.path.join(os.path.dirname(__file__), "..", "images")

PHOTOS = {
    "hero-home.jpg": "https://images.pexels.com/photos/69903/pexels-photo-69903.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "hero-climbing.jpg": "https://images.pexels.com/photos/3225531/pexels-photo-3225531.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "hero-membership.jpg": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=2560&q=85",
    "hero-community.jpg": "https://images.pexels.com/photos/3184418/pexels-photo-3184418.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "hero-cafe.jpg": "https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "hero-contact.jpg": "https://images.pexels.com/photos/1732414/pexels-photo-1732414.jpeg?auto=compress&cs=tinysrgb&w=1920",
    "gallery-social.jpg": "https://images.pexels.com/photos/3184418/pexels-photo-3184418.jpeg?auto=compress&cs=tinysrgb&w=800",
    "gallery-beginner.jpg": "https://images.pexels.com/photos/3184192/pexels-photo-3184192.jpeg?auto=compress&cs=tinysrgb&w=800",
    "gallery-competition.jpg": "https://images.pexels.com/photos/3225531/pexels-photo-3225531.jpeg?auto=compress&cs=tinysrgb&w=800",
    "gallery-outdoor.jpg": "https://images.pexels.com/photos/1687845/pexels-photo-1687845.jpeg?auto=compress&cs=tinysrgb&w=800",
}


def download(name, url):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    if len(data) < 5000:
        print(f"SKIP {name} – too small ({len(data)} bytes)")
        return False
    with open(path, "wb") as f:
        f.write(data)
    print(f"{name}\t{len(data) // 1024}KB")
    return True


if __name__ == "__main__":
    for name, url in PHOTOS.items():
        try:
            download(name, url)
        except Exception as e:
            print(f"FAIL {name}: {e}")
