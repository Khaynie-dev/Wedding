"""One-shot script to generate optimized WebP versions of engagement and about photos.

Outputs:
  assets/img/portfolio/optimized/portfolio-N.webp        (~1600px max, q82)  -> lightbox/parallax/hero
  assets/img/portfolio/optimized/portfolio-N-thumb.webp  (~800px max,  q80)  -> gallery grid thumbs
  assets/img/about/about-portrait-1.webp                 (~1200px max, q82)
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent / "assets" / "img"
PORT_SRC = ROOT / "portfolio"
PORT_OUT = PORT_SRC / "optimized"
PORT_OUT.mkdir(exist_ok=True)

ABOUT_SRC = ROOT / "about"

def fit(img, max_side):
    w, h = img.size
    if max(w, h) <= max_side:
        return img
    if w >= h:
        new_w = max_side
        new_h = int(round(h * max_side / w))
    else:
        new_h = max_side
        new_w = int(round(w * max_side / h))
    return img.resize((new_w, new_h), Image.LANCZOS)

def convert(src: Path, dst: Path, max_side: int, quality: int):
    with Image.open(src) as im:
        im = im.convert("RGB")
        im = fit(im, max_side)
        im.save(dst, "WEBP", quality=quality, method=6)
    print(f"  {src.name} ({src.stat().st_size//1024} KB)"
          f" -> {dst.name} ({dst.stat().st_size//1024} KB)"
          f" [{im.size[0]}x{im.size[1]}]")

print("Portfolio photos:")
for src in sorted(PORT_SRC.glob("portfolio-*.jpg")):
    stem = src.stem
    convert(src, PORT_OUT / f"{stem}.webp",       max_side=1600, quality=82)
    convert(src, PORT_OUT / f"{stem}-thumb.webp", max_side=800,  quality=80)

print("\nAbout portrait:")
for src in ABOUT_SRC.glob("about-portrait-*.jpg"):
    convert(src, ABOUT_SRC / f"{src.stem}.webp", max_side=1200, quality=82)

print("\nDone.")
