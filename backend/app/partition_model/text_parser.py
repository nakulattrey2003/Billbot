import re
import json

def clean_text(text: str) -> str:
    """
    Basic cleanup for OCR output.
    """
    text = text.replace("\n", " ").replace("\x0c", " ")  # remove newlines & page breaks
    text = re.sub(r"\s+", " ", text)  # collapse multiple spaces
    return text.strip()

def extract_fields(text: str) -> dict:
    """
    Extract structured fields (merchant, date, total, etc.) from OCR text using regex.
    """
    data = {}

    # Merchant name (assume first line = merchant)
    lines = text.split("\n")
    if lines:
        data["merchant_name"] = lines[0].strip()

    # Date
    date_match = re.search(r"(\d{2}[/-]\d{2}[/-]\d{4})", text)
    if date_match:
        data["date"] = date_match.group(1)

    # Time
    time_match = re.search(r"(\d{1,2}:\d{2}(?:\s?[APMapm]{2})?)", text)
    if time_match:
        data["time"] = time_match.group(1)

    # Total (pick last occurrence of a number after 'Total')
    total_match = re.findall(r"Total\s*[:\-]?\s*([\d,.]+)", text, re.IGNORECASE)
    if total_match:
        data["total"] = float(total_match[-1].replace(",", ""))

    return data

def text_to_json(text: str) -> str:
    """
    Convert cleaned text to JSON string.
    """
    structured = extract_fields(text)
    return json.dumps(structured, indent=2)
