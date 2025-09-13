from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch
import json

# Step 1: Load fine-tuned model + processor
model_path = "./trocr-receipt-model"   # change to your training output folder
processor = TrOCRProcessor.from_pretrained(model_path)
model = VisionEncoderDecoderModel.from_pretrained(model_path)

# Put model in eval mode
model.eval()

# Step 2: Load test image
image_path = "dataset/images/r1.png"   # test receipt image
image = Image.open(image_path).convert("RGB")

# Step 3: Preprocess
pixel_values = processor(image, return_tensors="pt").pixel_values

# Step 4: Generate prediction
with torch.no_grad():
    outputs = model.generate(
        pixel_values,
        max_length=512,
        num_beams=4,
        early_stopping=True
    )

# Step 5: Decode
predicted_text = processor.batch_decode(outputs, skip_special_tokens=True)[0]

# Step 6: Try JSON parsing
print("🔎 Predicted text:")
print(predicted_text)
# try:
#     predicted_json = json.loads(predicted_text)
#     print("✅ Predicted JSON:")
#     print(json.dumps(predicted_json, indent=2))
# except json.JSONDecodeError:
#     print("⚠️ Not valid JSON. Raw output:")
#     print(predicted_text)
