import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

from ..base import ComicSkill, SkillResult
from ..factory import register_skill
from ..utils import ensure_rgb, pil_to_numpy, numpy_to_pil


@register_skill
class WatercolorSkill(ComicSkill):
    name = "watercolor"
    description = "水彩漫画效果 — 柔化边缘 + 色彩增强，营造水彩质感"

    def get_params_schema(self):
        return {
            "smooth_radius": {"type": "int", "default": 3, "description": "平滑半径"},
            "color_boost": {"type": "float", "default": 1.3, "description": "色彩增强系数"},
            "edge_darken": {"type": "float", "default": 0.6, "description": "边缘加深强度"},
        }

    def process(self, image: Image.Image, smooth_radius: int = 3, color_boost: float = 1.3, edge_darken: float = 0.6) -> SkillResult:
        image = ensure_rgb(image)
        smoothed = image.filter(ImageFilter.BilateralBlur(radius=smooth_radius))

        edges = image.convert("L").filter(ImageFilter.FIND_EDGES)
        edges = edges.filter(ImageFilter.GaussianBlur(radius=smooth_radius // 2 + 1))

        color_enhanced = ImageEnhance.Color(smoothed).enhance(color_boost)
        contrast_enhanced = ImageEnhance.Contrast(color_enhanced).enhance(1.1)

        arr = pil_to_numpy(contrast_enhanced).astype(np.float32)
        edge_arr = pil_to_numpy(edges).astype(np.float32) / 255.0
        edge_arr = np.stack([edge_arr] * 3, axis=-1)

        darken = 1.0 - edge_arr * edge_darken
        arr = arr * darken
        arr = np.clip(arr, 0, 255).astype(np.uint8)

        return SkillResult(
            image=numpy_to_pil(arr),
            metadata={"smooth_radius": smooth_radius, "color_boost": color_boost, "edge_darken": edge_darken},
        )
