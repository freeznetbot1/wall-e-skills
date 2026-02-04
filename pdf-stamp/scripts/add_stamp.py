#!/usr/bin/env python3
"""
Add transparent PNG stamp overlay onto PDF documents.

Usage:
    python3 add_stamp.py <pdf_path> <stamp_path> <output_path> [options]

Options:
    --x           X coordinate (points from left) [default: auto]
    --y           Y coordinate (points from bottom) [default: auto]
    --size        Stamp size in points [default: 160]
    --all-pages   Apply to all pages [default: first page only]
    --right-box   Position in right signature box [default: false]
"""

import sys
import argparse
from pathlib import Path
from PIL import Image
import numpy as np
import fitz  # PyMuPDF


def process_stamp_transparency(stamp_path: str) -> Image.Image:
    """Load stamp and create transparency mask for dark backgrounds."""
    img = Image.open(stamp_path)
    rgb = np.array(img)
    h, w = rgb.shape[:2]

    # Convert to RGBA
    rgba = np.dstack([rgb, np.full((h, w), 255, dtype=np.uint8)])
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]

    # Detect stamp content (red pixels) vs background
    # Stamp is red, background is dark/black
    is_stamp = (r > g + 30) & (r > b + 30)
    brightness = (r + g + b) / 3
    is_bright = brightness > 100
    mask = is_stamp | is_bright

    # Set alpha: content = opaque, background = transparent
    rgba[:,:,3] = np.where(mask, 255, 0)

    return Image.fromarray(rgba, mode='RGBA')


def add_stamp(
    pdf_path: str,
    stamp_path: str,
    output_path: str,
    x: int = None,
    y: int = None,
    size: int = 160,
    all_pages: bool = False,
    right_box: bool = False
):
    """
    Add transparent PNG stamp to PDF.

    Args:
        pdf_path: Path to input PDF
        stamp_path: Path to PNG stamp image
        output_path: Path for output PDF
        x: X coordinate (points from left)
        y: Y coordinate (points from bottom)
        size: Stamp size in points (square)
        all_pages: Apply to all pages
        right_box: Position in right signature box
    """
    # Load PDF
    pdf = fitz.open(pdf_path)
    page = pdf[0]  # Start with first page
    page_width = page.rect.width
    page_height = page.rect.height

    # Load and process stamp
    stamp_img = process_stamp_transparency(stamp_path)
    aspect = stamp_img.width / stamp_img.height

    # Calculate stamp dimensions
    new_h = size
    new_w = int(size * aspect)
    stamp_img = stamp_img.resize((new_w, new_h), Image.LANCZOS)

    # Calculate position
    if right_box:
        # Position in right signature box area
        x = page_width - new_w - 35
        y = 500  # Middle of signature area
    elif x is None:
        # Default: bottom-right corner
        x = page_width - new_w - 50
        y = 80
    else:
        # Use provided x, y
        pass

    print(f"Stamp size: {new_w}x{new_h} pt")
    print(f"Position: X={x}, Y={y}")

    # Save temp transparent stamp
    temp_stamp = "temp_stamp.png"
    stamp_img.save(temp_stamp, "PNG")

    # Create rect for stamp placement
    # Note: fitz uses bottom-left origin, y is from bottom
    rect = fitz.Rect(x, y, x + new_w, y + new_h)

    # Apply to specified pages
    pages_to_stamp = list(pdf) if all_pages else [page]
    for p in pages_to_stamp:
        p.insert_image(rect, filename=temp_stamp, overlay=True)

    # Save output
    pdf.save(output_path)
    print(f"✓ Saved: {output_path}")

    # Cleanup
    import os
    if os.path.exists(temp_stamp):
        os.remove(temp_stamp)


def main():
    parser = argparse.ArgumentParser(
        description='Add transparent PNG stamp to PDF'
    )
    parser.add_argument('pdf', help='Input PDF path')
    parser.add_argument('stamp', help='PNG stamp path')
    parser.add_argument('output', help='Output PDF path')
    parser.add_argument('--x', type=int, default=None, help='X coordinate')
    parser.add_argument('--y', type=int, default=None, help='Y coordinate')
    parser.add_argument('--size', type=int, default=160, help='Stamp size in points')
    parser.add_argument('--all-pages', action='store_true', help='Apply to all pages')
    parser.add_argument('--right-box', action='store_true', help='Position in right signature box')

    args = parser.parse_args()

    add_stamp(
        pdf_path=args.pdf,
        stamp_path=args.stamp,
        output_path=args.output,
        x=args.x,
        y=args.y,
        size=args.size,
        all_pages=args.all_pages,
        right_box=args.right_box
    )


if __name__ == '__main__':
    main()
