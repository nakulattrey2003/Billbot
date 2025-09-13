# from fastapi import APIRouter, UploadFile, File
# from app.services.easy_ocrService import extract_text, extract_items

# router = APIRouter(prefix="/ocr", tags=["OCR"])

# @router.post("/extract")
# async def extract_bill_text(file: UploadFile = File(...)):
#     # Step 1: Extract text using EasyOCR
#     raw_text = await extract_text(file)

#     # Step 2: Extract items and prices
#     items = extract_items(raw_text)

#     # Step 3: Return structured response
#     return {
#         "raw_text": raw_text,
#         "items": items
#     }
