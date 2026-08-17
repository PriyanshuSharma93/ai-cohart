"""
make_scanned_enrollment.py - Day 5
Generates a SYNTHETIC 'scanned' enrollment form (image-based PDF, for OCR practice).
"""

from PIL import Image, ImageDraw, ImageFont

OUT_IMAGE = "source_docs/enrollment_scan.png"
OUT_PDF = "source_docs/enrollment.pdf"

LINES = [
    "SAMPLECARE HEALTH PLANS",
    "MEMBER ENROLLMENT FORM (SYNTHETIC DEMO)",
    "",
    "Member Name:      Jordan A. Sample",
    "Date of Birth:     01/15/1990",
    "Member ID:         MBR0099",
    "",
    "Plan Selected:      Gold PPO 2026",
    "Effective Date:     01/01/2026",
    "",
    "Employer Group:     Demo Corp Inc.",
    "Employee ID:        EMP-4471",
    "",
    "Dependents:",
    "  1. Sam Sample (Spouse) - DOB 03/22/1991",
    "  2. Alex Sample (Child) - DOB 07/09/2015",
    "",
    "Signature: ______________________     Date: __________",
    "",
    "This is a synthetic demo document. No real member",
    "information is contained in this form.",
]


def build_image():
    width, height = 1000, 1300
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 28)
        font_body = ImageFont.truetype("arial.ttf", 22)
    except Exception:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()

    y = 60
    for i, line in enumerate(LINES):
        font = font_title if i < 2 else font_body
        draw.text((60, y), line, fill="black", font=font)
        y += 45 if i >= 2 else 50

    img.save(OUT_IMAGE)
    return img


def build_pdf(img):
    img.convert("RGB").save(OUT_PDF)
    print(f"Wrote {OUT_IMAGE}")
    print(f"Wrote {OUT_PDF} (image-based PDF - requires OCR to read)")


if __name__ == "__main__":
    image = build_image()
    build_pdf(image)