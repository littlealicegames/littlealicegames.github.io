"""Build the web-ready image set from the studio's source artwork."""

import argparse

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


def square_png(source: Path, destination: str, size: int) -> None:
    image = Image.open(source).convert("RGBA")
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
    croak_icon = args.unity_root / "Assets" / "Resources" / "CroakWarsLogo.png"

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
    square_png(croak_icon, "favicon-32.png", 32)
    square_png(croak_icon, "apple-touch-icon.png", 180)


if __name__ == "__main__":
    main()
