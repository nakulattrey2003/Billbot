import os
import sys
import pytesseract
from image_utils import partition_image
from parser import parse_receipt
from enhancer import enhance_with_esrgan

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


def process_bill(input_path: str) -> dict:
    """
    Full pipeline: Enhance -> Partition -> OCR -> Parse -> Return structured data
    """
    # Step 1: Enhance with ESRGAN
    enhanced_path = enhance_with_esrgan(input_path, "enhanced_bill.jpg")

    # Step 2: Partition enhanced image
    partitions = partition_image(enhanced_path, num_strips=10, overlap=0.2)
    print(f"[INFO] Partitioned {len(partitions)} images after ESRGAN enhancement")

    # Save partitions for debugging
    debug_dir = os.path.join(os.path.dirname(__file__), "debug_partitions")
    os.makedirs(debug_dir, exist_ok=True)
    for idx, part in enumerate(partitions):
        save_path = os.path.join(debug_dir, f"partition_{idx+1}.jpg")
        part.save(save_path)
        print(f"[DEBUG] Saved partition {idx+1} at {save_path}")

    # Step 3: Run OCR on partitions
    raw_text = run_ocr_on_partitions(enhanced_path)

    # Step 4: Parse OCR output
    parsed = parse_receipt(raw_text)
    parsed["raw_text"] = raw_text[:500] + "..."  # preview

    return parsed
