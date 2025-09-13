# from fastapi import APIRouter, UploadFile, File
# from backend.app.services.tessaract_ocrService import extract_text, clean_ocr_text, extract_items

# router = APIRouter(prefix="/ocr", tags=["OCR"])

# @router.post("/extract")
# async def extract_bill_text(file: UploadFile = File(...)):
#     # Step 1: Extract raw text from the uploaded image
#     raw_text = await extract_text(file)
    
#     # Step 2: Clean the OCR text
#     cleaned_text = clean_ocr_text(raw_text)
    
#     # Step 3: Extract items and prices
#     items = extract_items(raw_text)  # You can also use cleaned_text if more accurate
    
#     # Step 4: Return structured response
#     return {
#         "raw_text": raw_text,
#         "cleaned_text": cleaned_text,
#         "items": items
#     }
