# import pytesseract
# from PIL import Image
# import io
# import re

# # Configure Tesseract path
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# async def extract_text(file) -> str:
#     """
#     Extract raw text from an uploaded image file using OCR.
#     """
#     contents = await file.read()
#     image = Image.open(io.BytesIO(contents))
#     text = pytesseract.image_to_string(image)
#     return text

# def clean_ocr_text(text: str) -> str:
#     """
#     Clean OCR text while keeping useful billing information.
#     - Retains ₹, decimals, %, and basic punctuation.
#     - Removes unwanted symbols.
#     """
#     # Allow ₹, digits, letters, ., %, :, and -
#     text = re.sub(r'[^\w\s₹.,:%-]', '', text)
#     # Normalize spaces/newlines
#     text = re.sub(r'\s+', ' ', text)
#     return text.strip()

# def get_lines(text: str) -> list[str]:
#     """
#     Split text into cleaned non-empty lines.
#     """
#     lines = [line.strip() for line in text.split("\n") if line.strip()]
#     return lines

# def extract_items(text: str) -> list[dict]:
#     """
#     Extract items and prices from bill text.
#     Supports:
#     - "Amul Masti Dahi 55"
#     - "Milk 2L ₹120.50"
#     - "Eggs 12pc 85.00"
#     """
#     items = []
#     for line in text.split("\n"):
#         line = line.strip()
#         if not line:
#             continue

#         # Match item name + price at end (with optional ₹ and decimals)
#         match = re.match(r'(.+?)\s+₹?(\d+(?:\.\d{1,2})?)$', line)
#         if match:
#             name, price = match.groups()
#             items.append({
#                 "item": name.strip(),
#                 "price": float(price)
#             })
#     return items

# def process_bill(text: str) -> dict:
#     """
#     Process the OCR text and return structured bill data.
#     """
#     cleaned_text = clean_ocr_text(text)
#     items = extract_items(cleaned_text)

#     return {
#         "raw_text": text,
#         "cleaned_text": cleaned_text,
#         "items": items
#     }
