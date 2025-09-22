# enhancer.py
from PIL import Image

try:
    from realesrgan_ncnn_py.realesrgan_ncnn_vulkan import Realesrgan
    HAS_ESRGAN = True
except ImportError:
    HAS_ESRGAN = False
    print("[WARN] ESRGAN not available, will fallback to original image.")

def enhance_with_esrgan(input_path: str, output_path: str) -> str:
    """
    Enhances a bill image using Real-ESRGAN (NCNN Vulkan backend).
    Falls back to original image if ESRGAN is unavailable.
    """
    try:
        if not HAS_ESRGAN:
            raise RuntimeError("ESRGAN not installed or not supported")

        sr = Realesrgan()   # ✅ no args → uses default x4 model
        print("[DEBUG] Realesrgan methods:", dir(sr))

        img = Image.open(input_path).convert("RGB")
        out = sr.process_pil(img)
        out.save(output_path)
        print("[INFO] ESRGAN enhancement applied successfully ✅")
        return output_path

    except Exception as e:
        print(f"[WARN] ESRGAN enhancement failed: {e}")
        # Fallback: just copy original image
        img = Image.open(input_path).convert("RGB")
        img.save(output_path)
        print("[INFO] Using original image instead ❌")
        return output_path
