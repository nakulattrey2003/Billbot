# from ocr_pipeline import ocr_image_to_json
from ocr_pipeline import process_bill

if __name__ == "__main__":
    result = process_bill("dataset/images/r6.jpg")
    print("Structured Data from Bill:")
    print(result)
