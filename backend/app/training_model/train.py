from transformers import TrOCRProcessor, VisionEncoderDecoderModel, Seq2SeqTrainer, Seq2SeqTrainingArguments
from receipt_dataset import ReceiptDataset, collate_fn

# Load smaller model
model_name = "microsoft/trocr-small-stage1"
processor = TrOCRProcessor.from_pretrained(model_name)
model = VisionEncoderDecoderModel.from_pretrained(model_name)

model.config.decoder_start_token_id = processor.tokenizer.bos_token_id
model.config.pad_token_id = processor.tokenizer.pad_token_id

# Make sure tokenizer has pad token
if processor.tokenizer.pad_token is None:
    processor.tokenizer.pad_token = processor.tokenizer.eos_token

# Load dataset
train_dataset = ReceiptDataset(
    image_dir="dataset/images",
    label_dir="dataset/labels",
    processor=processor
)

# Training args (lighter setup)
training_args = Seq2SeqTrainingArguments(
    output_dir="./trocr-receipt-model",
    per_device_train_batch_size=1,
    num_train_epochs=5,
    learning_rate=5e-5,
    save_steps=100,
    logging_steps=10,
    save_total_limit=2,
    predict_with_generate=True,
    remove_unused_columns=False
)

# Trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    tokenizer=processor,
    data_collator=lambda batch: collate_fn(batch, processor),
)

trainer.train()

# Save model
trainer.save_model("./trocr-receipt-model")
processor.save_pretrained("./trocr-receipt-model")



# this is a big model which we cannot use

# # Import HuggingFace classes for model, trainer, etc.
# from transformers import VisionEncoderDecoderModel, DonutProcessor, Seq2SeqTrainer, Seq2SeqTrainingArguments
# from torch.utils.data import DataLoader
# import torch

# # Import our custom dataset + collator from receipt_dataset.py
# from receipt_dataset import ReceiptDataset, collate_fn

# # Step 1: Load pretrained Donut model and processor
# # - The processor handles both images and text
# # - The model is a VisionEncoderDecoder (image → JSON text)
# model_name = "naver-clova-ix/donut-base"
# processor = DonutProcessor.from_pretrained(model_name)
# model = VisionEncoderDecoderModel.from_pretrained(model_name)

# # Ensure tokenizer has a pad token (important for batching)
# if processor.tokenizer.pad_token is None:
#     processor.tokenizer.pad_token = processor.tokenizer.eos_token

# # Step 2: Load our dataset (images + JSON labels)
# train_dataset = ReceiptDataset(
#     image_dir="dataset/images",   # path to images
#     label_dir="dataset/labels",   # path to JSON labels
#     processor=processor
# )

# # Step 3: Define training arguments
# training_args = Seq2SeqTrainingArguments(
#     output_dir="./donut-receipt-model",   # folder to save model checkpoints
#     per_device_train_batch_size=2,        # batch size per GPU/CPU
#     num_train_epochs=10,                  # number of training epochs
#     save_steps=50,                        # save checkpoint every 50 steps
#     logging_steps=10,                     # log training loss every 10 steps
#     learning_rate=5e-5,                   # learning rate
#     save_total_limit=2,                   # keep only last 2 checkpoints
#     predict_with_generate=True,           # allow generation during eval
#     remove_unused_columns=False           # keep dataset columns
# )

# # Step 4: Create trainer
# trainer = Seq2SeqTrainer(
#     model=model,
#     args=training_args,
#     train_dataset=train_dataset,
#     tokenizer=processor,
#     data_collator=lambda batch: collate_fn(batch, processor),
# )

# # Step 5: Start training
# trainer.train()

# print(1)

# # Step 6: Save the final model + processor
# trainer.save_model("./donut-receipt-model")
# processor.save_pretrained("./donut-receipt-model")

# print(2)
