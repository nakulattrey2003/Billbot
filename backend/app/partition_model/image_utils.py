from PIL import Image, ImageOps
import cv2
import numpy as np


def preprocess_image(img_path: str):
    """
    Load and refine an image for better OCR:
    - Convert to grayscale
    - Apply adaptive thresholding (handles uneven lighting better than Otsu)
    - Sharpen to make edges clearer
    - Resize ×2 for better OCR recognition
    """
    img = Image.open(img_path).convert("RGB")
    img = ImageOps.grayscale(img)
    cv_img = np.array(img)

    # Adaptive thresholding (better than global Otsu for receipts)
    thresh = cv2.adaptiveThreshold(
        cv_img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,  # block size (larger = smoother background)
        10   # constant subtracted (tunes contrast)
    )

    # Sharpening filter (helps OCR read clearer edges)
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(thresh, -1, kernel)

    # Resize ×2
    resized = cv2.resize(sharpened, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    return Image.fromarray(resized)


def partition_image(img_path: str, num_strips: int = 10, overlap: float = 0.2):
    """
    Partition an image into horizontal overlapping strips.
    - num_strips: how many horizontal slices to create
    - overlap: fraction overlap between strips
    """
    refined_img = preprocess_image(img_path)
    width, height = refined_img.size

    # Calculate actual strip height considering overlap
    effective_strip = height / (num_strips - (num_strips - 1) * overlap)
    overlap_px = int(effective_strip * overlap)

    partitions = []
    for i in range(num_strips):
        top = int(i * (effective_strip - overlap_px))
        bottom = int(top + effective_strip)
        if bottom > height:
            bottom = height
        crop = refined_img.crop((0, top, width, bottom))
        partitions.append(crop)

    return partitions

