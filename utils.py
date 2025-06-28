# utils.py

# utils.py

import pdfplumber
import re

def clean_text(text):
    """Clean only unwanted CID characters without affecting useful formatting."""
    if text:
        # Remove only (cid:XX) patterns
        text = re.sub(r'\(cid:\d+\)', '', text)
        # Replace strange non-printable characters (optional)
        text = text.replace('\x0b', ' ')
        text = text.replace('\x0c', ' ')
    return text

def extract_text_from_pdf(pdf_path):
    """Extract full PDF text with page count."""
    full_text = ""
    total_pages = 0
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for page in pdf.pages:
            text = page.extract_text()
            cleaned = clean_text(text)
            full_text += cleaned + "\n"
    return full_text, total_pages

def get_text_by_page(pdf_path, page_number):
    """Extract cleaned text for a specific page."""
    with pdfplumber.open(pdf_path) as pdf:
        if 1 <= page_number <= len(pdf.pages):
            raw_text = pdf.pages[page_number - 1].extract_text()
            return clean_text(raw_text)
        else:
            return None

