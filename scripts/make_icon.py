import os
from PIL import Image


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    png_path = os.path.join(root, 'assets', 'icon.png')
    ico_path = os.path.join(root, 'assets', 'app.ico')

    if not os.path.exists(png_path):
        raise FileNotFoundError(f"Icon PNG not found: {png_path}. Please place your icon at assets/icon.png")

    img = Image.open(png_path).convert('RGBA')
    # Ensure square icon
    w, h = img.size
    if w != h:
        s = min(w, h)
        left = (w - s) // 2
        top = (h - s) // 2
        img = img.crop((left, top, left + s, top + s))

    # Resize to standard ICO sizes
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (24, 24), (16, 16)]
    img.save(ico_path, format='ICO', sizes=sizes)
    print(f"Wrote {ico_path}")


if __name__ == '__main__':
    main()