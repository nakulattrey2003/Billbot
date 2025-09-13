import requests
import json

ASPRISE_URL = "https://ocr.asprise.com/api/v1/receipt"
API_KEY = "TEST"  # Replace with your real key if you get one

async def extract_receipt(file) -> dict:  # Send receipt image to Asprise OCR API and return structured JSON.
    contents = await file.read()

    res = requests.post(
        ASPRISE_URL,
        data={
            'api_key': API_KEY,
            'recognizer': 'auto',
            'ref_no': 'billbot_python_123'
        },
        files={
            'file': ("receipt.png", contents, file.content_type)
        }
    )

    return json.loads(res.text)
