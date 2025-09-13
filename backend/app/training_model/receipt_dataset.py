import os                      # for working with file paths
import json                    # for reading JSON label files
from PIL import Image          # for opening and converting images
import torch                   # for tensor operations
from torch.utils.data import Dataset  # to create a custom PyTorch dataset

# Custom dataset class for receipts
class ReceiptDataset(Dataset):
    def __init__(self, image_dir, label_dir, processor, file_exts=(".jpg",".jpeg",".png"), max_target_length=512):
        # image_dir → folder where receipt images are stored
        self.image_dir = image_dir
        # label_dir → folder where JSON labels are stored
        self.label_dir = label_dir
        # processor → DonutProcessor (handles both image preprocessing + tokenizer)
        self.processor = processor
        # max_target_length → maximum number of tokens for the JSON output
        self.max_target_length = max_target_length

        # Create a list of (image_path, label_path) pairs
        self.samples = []
        # Loop through all files in the image directory
        for fname in sorted(os.listdir(image_dir)):
            # Check if file is an image (jpg, jpeg, png)
            if fname.lower().endswith(file_exts):
                # Get full path of image file
                image_path = os.path.join(image_dir, fname)
                # Convert image filename to corresponding JSON filename
                label_name = os.path.splitext(fname)[0] + ".json"
                # Get full path of JSON label file
                label_path = os.path.join(label_dir, label_name)

                # Only add pair if the JSON label exists
                if os.path.exists(label_path):
                    self.samples.append((image_path, label_path))

        # If no valid samples found, raise an error
        if len(self.samples) == 0:
            raise RuntimeError(f"No image/label pairs found in {image_dir} / {label_dir}")

    def __len__(self):
        # Return number of samples in dataset
        return len(self.samples)

    def __getitem__(self, idx):
        # Get image and label paths at index
        image_path, label_path = self.samples[idx]

        # Open image and convert to RGB
        image = Image.open(image_path).convert("RGB")

        # Load JSON label file
        with open(label_path, "r", encoding="utf-8") as f:
            label = json.load(f)

        # Convert JSON dict → canonical string (sorted keys, compact format)
        label_text = json.dumps(label, separators=(",", ":"), sort_keys=True, ensure_ascii=False)

        # Preprocess image with DonutProcessor → returns pixel_values tensor
        encoding = self.processor(image, return_tensors="pt")
        # Remove batch dimension (squeeze from [1, C, H, W] → [C, H, W])
        pixel_values = encoding["pixel_values"].squeeze(0)

        # Tokenize the JSON string into token IDs
        tokenized = self.processor.tokenizer(
            label_text,                 # the label JSON string
            add_special_tokens=True,    # add special tokens like <s> and </s>
            truncation=True,            # truncate if longer than max_target_length
            max_length=self.max_target_length,  # maximum allowed tokens
        )
        # Convert token IDs into a PyTorch tensor
        labels = torch.tensor(tokenized["input_ids"], dtype=torch.long)

        # Return everything needed for training
        return {
            "pixel_values": pixel_values,  # processed image tensor
            "labels": labels,              # tokenized label IDs
            "label_text": label_text,      # original JSON string (for debugging)
            "image_path": image_path       # path of image (for debugging)
        }


# Function to collate a batch of samples (needed for DataLoader)
def collate_fn(batch, processor):
    # Stack all image tensors into a batch → shape [B, C, H, W]
    pixel_values = torch.stack([b["pixel_values"] for b in batch])

    # Collect label sequences (different lengths per receipt)
    labels_list = [b["labels"] for b in batch]

    # Get pad token ID from tokenizer (if missing, use EOS token)
    pad_token_id = processor.tokenizer.pad_token_id
    if pad_token_id is None:
        pad_token_id = processor.tokenizer.eos_token_id

    # Pad all labels to same length with pad_token_id
    labels_padded = torch.nn.utils.rnn.pad_sequence(
        labels_list, batch_first=True, padding_value=pad_token_id
    )

    # Replace pad tokens with -100 (so model ignores them in loss calculation)
    labels_padded[labels_padded == pad_token_id] = -100

    # Return final batch dictionary
    return {"pixel_values": pixel_values, "labels": labels_padded}
