import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

from ..base import ComicSkill, SkillResult
from ..factory import register_skill
from ..utils import ensure_rgb, pil_to_numpy, numpy_to_pil


@register_skill
class PopArtSkill(ComicSkill):
    name = "pop_art"
    description = "波普漫画效果 — 高饱和 + 强对比 + 粗轮廓，美式漫画风格"

    def get_params_schema(self):
        return {
            "saturation": {"type": "float", "default": 2.0, "description": "饱和度系数"},
            "contrast": {"type": "float", "default": 1.5, "description": "对比度系数"},
            "edge_thickness": {"type": "int", "default": 2, "description": "轮廓线粗细"},
        }

    def process(self, image: Image.Image, saturation: float = 2.0, contrast: float = 1.5, edge_thickness: int = 2) -> SkillResult:
        image = ensure_rgb(image)
        enhanced = ImageEnhance.Color(image).enhance(saturation)
        enhanced = ImageEnhance.Contrast(enhanced).enhance(contrast)

        gray = image.convert("L")
        edges = gray.filter(ImageFilter.FIND_EDGES)
        if edge_thickness > 1:
            for _ in range(edge_thickness - 1):
                edges = edges.filter(ImageFilter.MaxFilter(3))
        edges_inv = Image.fromarray(255 - np.array(edges))

        arr = pil_to_numpy(enhanced).astype(np.float32)
        edge_mask = pil_to_numpy(edges).astype(np.float32) / 255.0
        edge_mask = np.stack([edge_mask] * 3, axis=-1)

        arr = arr * (1.0 - edge_mask * 0.85)
        arr = np.clip(arr, 0, 255).astype(np.uint8)

        return SkillResult(
            image=numpy_to_pil(arr),
            metadata={"saturation": saturation, "contrast": contrast, "edge_thickness": edge_thickness},
        )
