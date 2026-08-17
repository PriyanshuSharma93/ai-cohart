"""
extract_text.py - Day 5
Extracts text from PDFs, Word docs, OCR scans, and a public web page.
Normalizes and saves everything as .txt files under raw_text/.
"""

import os
import re
import pdfplumber
from docx import Document
import pytesseract
from pdf2image import convert_from_path
import requests
from bs4 import BeautifulSoup

RAW_TEXT_DIR = "raw_text"
os.makedirs(RAW_TEXT_DIR, exist_ok=True)


def normalize_text(text: str) -> str:
    replacements = {
        "\u2019": "'", "\u2018": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-",
        "\xa0": " ",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)

    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append("")
            continue
        if stripped.startswith("CONFIDENTIAL"):
            continue
        if re.match(r"^Page \d+\s*\|", stripped):
            continue
        cleaned_lines.append(stripped)

    text = "\n".join(cleaned_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip() + "\n"


def dedupe_lines(text: str) -> str:
    lines = text.split("\n")
    deduped = []
    prev = None
    for line in lines:
        if line == prev and line.strip() != "":
            continue
        deduped.append(line)
        prev = line
    return "\n".join(deduped)


def extract_benefits_pdf():
    path = "source_docs/benefits.pdf"
    all_text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            all_text.append(page_text)

    raw = "\n\n".join(all_text)
    cleaned = dedupe_lines(normalize_text(raw))

    out_path = os.path.join(RAW_TEXT_DIR, "benefits.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    print(f"[pdfplumber] {path} -> {out_path} ({len(cleaned)} chars)")


def extract_claims_docx():
    path = "source_docs/claims_process.docx"
    doc = Document(path)

    parts = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    raw = "\n\n".join(parts)
    cleaned = dedupe_lines(normalize_text(raw))

    out_path = os.path.join(RAW_TEXT_DIR, "claims_process.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    print(f"[python-docx] {path} -> {out_path} ({len(cleaned)} chars)")


def extract_enrollment_ocr():
    path = "source_docs/enrollment.pdf"
    images = convert_from_path(path, dpi=300)

    ocr_text_parts = [pytesseract.image_to_string(image) for image in images]
    raw = "\n\n".join(ocr_text_parts)
    cleaned = dedupe_lines(normalize_text(raw))

    out_path = os.path.join(RAW_TEXT_DIR, "enrollment.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    print(f"[pytesseract OCR] {path} -> {out_path} ({len(cleaned)} chars)")


def extract_provider_faq(url: str):
    headers = {"User-Agent": "Mozilla/5.0 (educational scraping demo)"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "form"]):
        tag.decompose()

    main = soup.find("main") or soup.find("article") or soup

    parts = []
    for el in main.find_all(["h1", "h2", "h3", "p", "li"]):
        text = el.get_text(strip=True)
        if text:
            parts.append(text)

    raw = "\n\n".join(parts)
    cleaned = dedupe_lines(normalize_text(raw))

    out_path = os.path.join(RAW_TEXT_DIR, "provider_faq.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    print(f"[BeautifulSoup] {url} -> {out_path} ({len(cleaned)} chars)")


if __name__ == "__main__":
    extract_benefits_pdf()
    extract_claims_docx()
    extract_enrollment_ocr()

    FAQ_URL = "https://www.medicare.gov/basics/get-started-with-medicare/medicare-basics/parts-of-medicare"
    try:
        extract_provider_faq(FAQ_URL)
    except Exception as e:
        print(f"[BeautifulSoup] Skipped scraping ({FAQ_URL}): {e}")