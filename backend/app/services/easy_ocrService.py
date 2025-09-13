# import easyocr
# import numpy as np
# import cv2
# import io

# # Initialize EasyOCR reader (load once)
# reader = easyocr.Reader(['en'])

# async def extract_text(file) -> str:  # Extract text from an uploaded image file using EasyOCR.
#     contents = await file.read()

#     # Convert bytes → NumPy array → OpenCV image
#     np_img = np.frombuffer(contents, np.uint8)
#     img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

#     # Run OCR
#     results = reader.readtext(img)

#     # Join detected text
#     text = "\n".join([res[1] for res in results])
#     return text

# def extract_items(text: str) -> list[dict]:   # Extract items and prices from OCR text.
#     import re
#     items = []
#     for line in text.split("\n"):
#         line = line.strip()
#         if not line:
#             continue

#         # Match item name + price (support ₹ and decimals)
#         match = re.match(r'(.+?)\s+₹?(\d+(?:\.\d{1,2})?)$', line)
#         if match:
#             name, price = match.groups()
#             items.append({"item": name.strip(), "price": float(price)})
#     return items
