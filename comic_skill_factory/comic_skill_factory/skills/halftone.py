import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

from ..base import ComicSkill, SkillResult
from ..factory import register_skill
from ..utils import ensure_rgb, pil_to_numpy, numpy_to_pil


@register_skill
class HalftoneSkill(ComicSkill):
    name = "halftone"
    description = "半色调网点效果 — 将图片转为黑白漫画网点风格"

    def get_params_schema(self):
        return {
            "dot_size": {"type": "int", "default": 6, "description": "网点大小（像素）"},
            "contrast": {"type": "float", "default": 1.3, "description": "对比度增强系数"},
            "threshold": {"type": "int", "default": 128, "description": "二值化阈值"},
        }

    def process(self, image: Image.Image, dot_size: int = 6, contrast: float = 1.3, threshold: int = 128) -> SkillResult:
        image = ensure_rgb(image)
        gray = image.convert("L")
        gray = gray.filter(ImageFilter.GaussianBlur(radius=1))
        arr = pil_to_numpy(gray).astype(np.float32)

        arr = arr * contrast
        np.clip(arr, 0, 255, out=arr)

        h, w = arr.shape
        output = np.full((h, w), 255, dtype=np.uint8)

        for y in range(0, h, dot_size):
            for x in range(0, w, dot_size):
                y2 = min(y + dot_size, h)
                x2 = min(x + dot_size, w)
                block = arr[y:y2, x:x2]
                avg = block.mean()
                radius = max(0.5, (1.0 - avg / 255.0) * dot_size / 2.0)
                cy = (y + y2) // 2
                cx = (x + x2) // 2

                for dy in range(y, y2):
                    for dx in range(x, x2):
                        dist = np.sqrt((dx - cx) ** 2 + (dy - cy) ** 2)
                        if dist <= radius:
                            output[dy, dx] = 0

        return SkillResult(
            image=numpy_to_pil(np.stack([output] * 3, axis=-1)),
            metadata={"dot_size": dot_size, "contrast": contrast, "threshold": threshold},
        )
