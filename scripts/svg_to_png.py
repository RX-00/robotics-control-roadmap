#!/usr/bin/env python3
"""Render an SVG file as a PNG using an installed command-line renderer."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SVG = ROOT / "images" / "robotics-control-roadmap.svg"
DEFAULT_PNG = ROOT / "images" / "robotics-control-roadmap.png"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render an SVG as a PNG using rsvg-convert, Inkscape, or ImageMagick."
    )
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        default=DEFAULT_SVG,
        help=f"SVG input (default: {DEFAULT_SVG.relative_to(ROOT)})",
    )
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        default=DEFAULT_PNG,
        help=f"PNG output (default: {DEFAULT_PNG.relative_to(ROOT)})",
    )
    parser.add_argument(
        "--width",
        type=int,
        help="Output width in pixels; preserves the SVG aspect ratio.",
    )
    return parser.parse_args()


def renderer_command(input_path: Path, output_path: Path, width: int | None) -> list[str]:
    if rsvg_convert := shutil.which("rsvg-convert"):
        command = [rsvg_convert, "--format=png", f"--output={output_path}"]
        if width is not None:
            command.append(f"--width={width}")
        return command + [str(input_path)]

    if inkscape := shutil.which("inkscape"):
        command = [
            inkscape,
            str(input_path),
            "--export-type=png",
            f"--export-filename={output_path}",
        ]
        if width is not None:
            command.append(f"--export-width={width}")
        return command

    if magick := shutil.which("magick"):
        command = [magick, str(input_path), "-background", "none"]
    elif convert := shutil.which("convert"):
        command = [convert, str(input_path), "-background", "none"]
    else:
        raise RuntimeError(
            "No SVG renderer found. Install librsvg (rsvg-convert), Inkscape, "
            "or ImageMagick, then try again."
        )

    if width is not None:
        command.extend(["-resize", f"{width}x"])
    return command + [str(output_path)]


def main() -> int:
    args = parse_args()
    if args.width is not None and args.width <= 0:
        print("error: --width must be a positive integer", file=sys.stderr)
        return 2

    input_path = args.input.resolve()
    output_path = args.output.resolve()
    if not input_path.is_file():
        print(f"error: SVG input does not exist: {input_path}", file=sys.stderr)
        return 2
    if output_path.suffix.lower() != ".png":
        print("error: output path must end in .png", file=sys.stderr)
        return 2

    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        command = renderer_command(input_path, output_path, args.width)
        subprocess.run(command, check=True)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
