import os
import sys
import pytesseract
from image_utils import partition_image
from parser import parse_receipt  # <-- NEW import

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
CUSTOM_CONFIG = r"--oem 3 --psm 6 -c preserve_interword_spaces=1"

def run_ocr_on_partitions(img_path: str) -> str:
    partitions = partition_image(img_path, num_strips=10, overlap=0.2)
    all_text = []

    for part in partitions:
        text = pytesseract.image_to_string(part, config=CUSTOM_CONFIG)
        all_text.append(text)

    combined = "\n".join(all_text)

    # Save for debugging
    debug_file = os.path.join(os.path.dirname(__file__), "debug_ocr_output.txt")
    with open(debug_file, "w", encoding="utf-8") as f:
        f.write(combined)

    return combined

def ocr_image_to_json(img_path: str) -> dict:
    raw_text = run_ocr_on_partitions(img_path)
    parsed = parse_receipt(raw_text)  # <-- run through parser
    parsed["raw_text"] = raw_text[:500] + "..."  # keep preview
    return parsed
