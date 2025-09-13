from fastapi import APIRouter, UploadFile, File
from app.services.aspire_ocrService import extract_receipt

router = APIRouter(prefix="/ocr", tags=["OCR"])

@router.post("/extract")
async def extract_bill_text(file: UploadFile = File(...)):
    # Send to Asprise and get structured result
    result = await extract_receipt(file)
    return result
