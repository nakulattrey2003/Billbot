import os
import json
import google.generativeai as genai

# set your Gemini API key
genai.configure(api_key="AIzaSyAQ90-hXmUtkYqx-5UihVapxwPCvvqj7IA")

model = genai.GenerativeModel("gemini-1.5-flash")

# Load OCR text
with open("debug_ocr_output.txt", "r", encoding="utf-8") as f:
    ocr_text = f.read()

# Prompt Gemini
prompt = f"""
You are a receipt parser AI. 
Convert the following OCR text into structured JSON.
Extract:
- merchant_name
- date
- time
- items (list of objects: description, quantity, price)

OCR text:
{ocr_text}
"""

response = model.generate_content(prompt)

print("Gemini Response:")
print(response.text)
