import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance


def pil_to_numpy(image: Image.Image) -> np.ndarray:
    return np.array(image)


def numpy_to_pil(array: np.ndarray) -> Image.Image:
    if array.dtype != np.uint8:
        array = np.clip(array, 0, 255).astype(np.uint8)
    return Image.fromarray(array)


def ensure_rgb(image: Image.Image) -> Image.Image:
    if image.mode == "RGBA":
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])
        return background
    if image.mode != "RGB":
        return image.convert("RGB")
    return image


def enhance_contrast(image: Image.Image, factor: float = 1.2) -> Image.Image:
    return ImageEnhance.Contrast(image).enhance(factor)


def enhance_sharpness(image: Image.Image, factor: float = 1.5) -> Image.Image:
    return ImageEnhance.Sharpness(image).enhance(factor)


def apply_edge_preserving_smooth(image: Image.Image, radius: int = 2) -> Image.Image:
    arr = pil_to_numpy(image).astype(np.float32)
    h, w, c = arr.shape
    result = np.zeros_like(arr)
    pad = radius
    padded = np.pad(arr, ((pad, pad), (pad, pad), (0, 0)), mode="reflect")

    for i in range(h):
        for j in range(w):
            patch = padded[i : i + 2 * radius + 1, j : j + 2 * radius + 1]
            center = padded[i + pad, j + pad]
            diff = np.abs(patch - center).sum(axis=2)
            weights = np.exp(-diff / (30.0))
            weights = weights / (weights.sum() + 1e-8)
            for c in range(3):
                result[i, j, c] = np.sum(patch[:, :, c] * weights)

    return numpy_to_pil(result)
