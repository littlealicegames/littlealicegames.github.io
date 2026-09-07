"""Build the web-ready image set from the studio's source artwork."""

import argparse
from collections import deque

from pathlib import Path

from PIL import Image


SITE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = SITE_ROOT / "assets" / "images"


def fit_within(source: Path, destination: str, maximum: tuple[int, int], quality: int = 84) -> None:
    image = Image.open(source)
    image.thumbnail(maximum, Image.Resampling.LANCZOS)
    image.save(OUTPUT / destination, "WEBP", quality=quality, method=6)


def cover_jpeg(source: Path, destination: str, size: tuple[int, int]) -> None:
    image = Image.open(source).convert("RGB")
    scale = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    resized.crop((left, top, left + size[0], top + size[1])).save(
        OUTPUT / destination,
        "JPEG",
        quality=88,
        optimize=True,
        progressive=True,
    )


def remove_edge_background(image: Image.Image, tolerance: int = 24) -> Image.Image:
    """Make only the near-white background connected to the canvas edge transparent."""
    image = image.copy()
    width, height = image.size
    pixels = image.load()
    background = pixels[0, 0][:3]
    connected = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def add_if_background(x: int, y: int) -> None:
        index = y * width + x
        if connected[index]:
            return
        red, green, blue, alpha = pixels[x, y]
        if alpha and max(
            abs(red - background[0]),
            abs(green - background[1]),
            abs(blue - background[2]),
        ) <= tolerance:
            connected[index] = 1
            queue.append((x, y))

    for x in range(width):
        add_if_background(x, 0)
        add_if_background(x, height - 1)
    for y in range(height):
        add_if_background(0, y)
        add_if_background(width - 1, y)

    while queue:
        x, y = queue.popleft()
        if x:
            add_if_background(x - 1, y)
        if x + 1 < width:
            add_if_background(x + 1, y)
        if y:
            add_if_background(x, y - 1)
        if y + 1 < height:
            add_if_background(x, y + 1)

    output = list(image.getdata())
    for index, is_background in enumerate(connected):
        if is_background:
            red, green, blue, _ = output[index]
            output[index] = (red, green, blue, 0)
    image.putdata(output)
    return image


def square_png(source: Path, destination: str, size: int, trim_background: bool = False) -> None:
    image = Image.open(source).convert("RGBA")
    if trim_background:
        image = remove_edge_background(image)
        bounds = image.getbbox()
        if bounds:
            padding = round(max(bounds[2] - bounds[0], bounds[3] - bounds[1]) * 0.06)
            image = image.crop(
                (
                    max(0, bounds[0] - padding),
                    max(0, bounds[1] - padding),
                    min(image.width, bounds[2] + padding),
                    min(image.height, bounds[3] + padding),
                )
            )
    image.thumbnail((size, size), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.alpha_composite(image, ((size - image.width) // 2, (size - image.height) // 2))
    canvas.save(OUTPUT / destination, "PNG", optimize=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unity-root", type=Path, default=SITE_ROOT.parent / "frogs-game")
    parser.add_argument("--downloads", type=Path, default=Path.home() / "Downloads")
    parser.add_argument(
        "--screenshots",
        type=Path,
        default=Path.home() / "Pictures" / "Screenshots",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    OUTPUT.mkdir(parents=True, exist_ok=True)

    studio_banner = args.downloads / "CroakWars" / "LittleAliceGames&Tools.png"
    publisher_logo = args.downloads / "logo_publisher.png"

    fit_within(studio_banner, "studio-pond.webp", (1600, 1000), quality=84)
    fit_within(studio_banner, "studio-pond-1200.webp", (1200, 675), quality=82)
    fit_within(studio_banner, "studio-pond-800.webp", (800, 450), quality=82)
    fit_within(publisher_logo, "studio-mark.webp", (560, 560), quality=88)
    fit_within(publisher_logo, "studio-mark-128.webp", (128, 128), quality=88)
    fit_within(
        args.unity_root / "PlayConsole" / "images" / "feature_graphic.png",
        "croak-feature.webp",
        (1200, 700),
        quality=86,
    )
    fit_within(
        args.unity_root
        / "PlayConsole"
        / "images"
        / "store_mockups_v2"
        / "01_chain_reaction.png",
        "croak-gameplay.webp",
        (720, 1280),
        quality=84,
    )
    fit_within(
        args.unity_root
        / "PlayConsole"
        / "images"
        / "store_mockups_v2"
        / "01_chain_reaction.png",
        "croak-gameplay-480.webp",
        (480, 854),
        quality=82,
    )
    fit_within(
        args.screenshots / "Screenshot 2026-08-29 202818.png",
        "publisher-ui.webp",
        (1280, 1000),
        quality=84,
    )
    fit_within(
        args.screenshots / "Screenshot 2026-08-29 202818.png",
        "publisher-ui-720.webp",
        (720, 556),
        quality=82,
    )

    cover_jpeg(studio_banner, "og-image.jpg", (1200, 630))
    square_png(publisher_logo, "favicon-32.png", 32, trim_background=True)
    square_png(publisher_logo, "apple-touch-icon.png", 180, trim_background=True)


if __name__ == "__main__":
    main()
