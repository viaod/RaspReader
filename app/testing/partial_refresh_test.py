"""Standalone Waveshare partial-refresh hardware test.

Run on the Raspberry Pi with:

    python -m app.testing.partial_refresh_test

This test talks directly to the display driver and does not change the
application's full-refresh-only Display class.
"""

import argparse
import time

from PIL import Image, ImageDraw, ImageFont


def run(iterations, delay):
    try:
        from lib.waveshare_epd import epd3in7
    except Exception as exc:
        raise SystemExit(
            "Could not claim the display GPIO pins. Stop the reader service "
            "before running this hardware test, then start it again afterward:\n"
            "  sudo systemctl stop raspreader.service\n"
            "  python -m app.testing.partial_refresh_test\n"
            "  sudo systemctl start raspreader.service\n"
            f"\nOriginal error: {exc}"
        ) from exc

    epd = epd3in7.EPD()

    try:
        print("Showing full-refresh baseline...")
        epd.init(0)
        epd.Clear(0xFF, 0)

        baseline = Image.new("L", (epd.height, epd.width), 0xFF)
        draw = ImageDraw.Draw(baseline)
        font = ImageFont.load_default()
        draw.text((20, 20), "Full refresh baseline", font=font, fill=0)
        epd.display_4Gray(epd.getbuffer_4Gray(baseline))
        time.sleep(3)

        print(f"Running {iterations} partial updates...")
        epd.init(1)
        epd.Clear(0xFF, 1)

        image = Image.new("1", (epd.height, epd.width), 1)
        draw = ImageDraw.Draw(image)

        for iteration in range(iterations):
            draw.rectangle((20, 60, 260, 100), fill=1)
            draw.text(
                (20, 60),
                f"Partial update {iteration + 1}/{iterations}",
                font=font,
                fill=0,
            )
            epd.display_1Gray(epd.getbuffer(image))
            time.sleep(delay)

        print("Partial-refresh test complete. Clearing display...")
        epd.init(0)
        epd.Clear(0xFF, 0)
    except KeyboardInterrupt:
        print("Interrupted. Clearing display...")
        epd.init(0)
        epd.Clear(0xFF, 0)
    finally:
        epd.sleep()
        epd3in7.epdconfig.module_exit(cleanup=True)


def main():
    parser = argparse.ArgumentParser(description="Test Waveshare partial refresh")
    parser.add_argument(
        "--iterations",
        type=int,
        default=20,
        help="number of partial updates to perform (default: 20)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="seconds between updates (default: 0.5)",
    )
    args = parser.parse_args()

    if args.iterations < 1:
        parser.error("--iterations must be at least 1")
    if args.delay < 0:
        parser.error("--delay cannot be negative")

    run(args.iterations, args.delay)


if __name__ == "__main__":
    main()