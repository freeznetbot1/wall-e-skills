---
name: pdf-stamp
description: Add transparent PNG stamp/seal overlay onto PDF documents. Supports position customization (coordinates or keywords like "右下角"), size adjustment, and transparency handling.
---

# PDF Stamp Overlay

Add a transparent PNG stamp/seal onto PDF documents.

## Requirements

- Python 3.9+
- PyMuPDF (`pymupdf`)
- Pillow (PIL)

## Usage

```python
from scripts.add_stamp import add_stamp

# Basic: stamp on bottom-right of all pages
add_stamp(
    pdf_path="合同.pdf",
    stamp_path="印章.png",
    output_path="已盖章合同.pdf"
)

# Custom position (x, y in points from bottom-left)
add_stamp(
    pdf_path="合同.pdf",
    stamp_path="印章.png",
    output_path="已盖章合同.pdf",
    x=450,      # X coordinate (points)
    y=100,      # Y coordinate (points)
    size=120    # Stamp size in points (square)
)

# All pages
add_stamp(
    pdf_path="合同.pdf",
    stamp_path="印章.png",
    output_path="已盖章合同.pdf",
    all_pages=True
)
```

## Position Guide

**Keywords** (not yet implemented):
- `右下角` → X = page_width - size - 50, Y = 100
- `左下角` → X = 50, Y = 100
- `右上角` → X = page_width - size - 50, Y = page_height - size - 50
- `左上角` → X = 50, Y = page_height - size - 50

**Manual coordinates** (recommended):
- X: 0 = left edge, page_width = right edge
- Y: 0 = bottom edge, page_height = top edge
- Default origin: bottom-left corner

## Tips

- A4 page: 595 × 842 points
- Stamp size 150-200pt usually works well for contract seals
- PNG transparency is preserved automatically
