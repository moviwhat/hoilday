import numpy as np
from PIL import Image, ImageFilter, ImageOps

from ..base import ComicSkill, SkillResult
from ..factory import register_skill
from ..utils import ensure_rgb, pil_to_numpy, numpy_to_pil


@register_skill
class LineArtSkill(ComicSkill):
    name = "line_art"
    description = "线稿描边效果 — 提取图片轮廓线，生成漫画线稿风格"

    def get_params_schema(self):
        return {
            "edge_strength": {"type": "float", "default": 1.0, "description": "边缘强度"},
            "invert": {"type": "bool", "default": True, "description": "是否反转颜色（白底黑线）"},
        }

    def process(self, image: Image.Image, edge_strength: float = 1.0, invert: bool = True) -> SkillResult:
        image = ensure_rgb(image)
        gray = image.convert("L")
        blurred = gray.filter(ImageFilter.GaussianBlur(radius=1.5))
        edges = gray.filter(ImageFilter.FIND_EDGES)

        arr_edges = pil_to_numpy(edges).astype(np.float32)
        arr_edges = np.clip(arr_edges * edge_strength, 0, 255)

        if invert:
            arr_edges = 255 - arr_edges

        arr_edges = np.clip(arr_edges, 0, 255).astype(np.uint8)
        return SkillResult(
            image=numpy_to_pil(np.stack([arr_edges] * 3, axis=-1)),
            metadata={"edge_strength": edge_strength, "invert": invert},
        )
