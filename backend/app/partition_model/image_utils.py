from PIL import Image, ImageOps
import cv2
import numpy as np

def preprocess_image(img_path: str):
    img = Image.open(img_path).convert("RGB")
    img = ImageOps.grayscale(img)
    cv_img = np.array(img)
    _, thresh = cv2.threshold(cv_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    denoised = cv2.medianBlur(thresh, 3)
    resized = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    return Image.fromarray(resized)

def partition_image(img_path: str, num_strips: int = 10, overlap: float = 0.2):
    """
    Partition an image into vertical overlapping strips.
    """
    refined_img = preprocess_image(img_path)
    width, height = refined_img.size

    # Calculate actual strip width considering overlap
    effective_strip = width / (num_strips - (num_strips - 1) * overlap)
    overlap_px = int(effective_strip * overlap)

    partitions = []
    for i in range(num_strips):
        left = int(i * (effective_strip - overlap_px))
        right = int(left + effective_strip)
        if right > width:
            right = width
        crop = refined_img.crop((left, 0, right, height))
        partitions.append(crop)

    return partitions
