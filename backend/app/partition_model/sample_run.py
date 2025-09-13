from ocr_pipeline import ocr_image_to_json

if __name__ == "__main__":
    image_path = "dataset/images/r8.png"
    result_json = ocr_image_to_json(image_path)
    print("✅ OCR Result:")
    print(result_json)
