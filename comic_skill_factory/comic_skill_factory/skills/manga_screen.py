import numpy as np
from PIL import Image, ImageFilter

from ..base import ComicSkill, SkillResult
from ..factory import register_skill
from ..utils import ensure_rgb, pil_to_numpy, numpy_to_pil


@register_skill
class MangaScreenSkill(ComicSkill):
    name = "manga_screen"
    description = "漫画网纹效果 — 模拟日式漫画的灰度网纹（スクリーントーン）"

    def get_params_schema(self):
        return {
            "levels": {"type": "int", "default": 4, "description": "灰度层级数"},
            "pattern_scale": {"type": "float", "default": 1.0, "description": "网纹图案缩放系数"},
        }

    _patterns: list = []

    @classmethod
    def _init_patterns(cls):
        if cls._patterns:
            return
        pattern_size = 8
        for level in range(5):
            pattern = np.zeros((pattern_size, pattern_size), dtype=np.float32)
            density = level / 4.0
            for i in range(pattern_size):
                for j in range(pattern_size):
                    x = (j - pattern_size // 2) / (pattern_size / 2)
                    y = (i - pattern_size // 2) / (pattern_size / 2)
                    r = np.sqrt(x * x + y * y)
                    if r <= density * 0.85:
                        pattern[i, j] = 1.0
            cls._patterns.append(pattern)

    def process(self, image: Image.Image, levels: int = 4, pattern_scale: float = 1.0) -> SkillResult:
        self._init_patterns()
        image = ensure_rgb(image)
        gray = image.convert("L")
        gray = gray.filter(ImageFilter.GaussianBlur(radius=0.8))
        arr = pil_to_numpy(gray).astype(np.float32)
        h, w = arr.shape

        step = 255.0 / levels
        quantized = (arr // step) * step
        quantized = np.clip(quantized, 0, 255)

        output = np.full((h, w), 255, dtype=np.uint8)
        ps = max(2, int(8 * pattern_scale))

        for y in range(0, h, ps):
            for x in range(0, w, ps):
                y2 = min(y + ps, h)
                x2 = min(x + ps, w)
                block = quantized[y:y2, x:x2]
                avg_val = block.mean()
                pattern_idx = min(len(self._patterns) - 1, int(avg_val / 255.0 * len(self._patterns)))
                pattern = self._patterns[pattern_idx]

                bh, bw = y2 - y, x2 - x
                scaled_pattern = np.zeros((bh, bw), dtype=np.float32)
                for pi in range(bh):
                    for pj in range(bw):
                        si = int(pi / bh * pattern.shape[0])
                        sj = int(pj / bw * pattern.shape[1])
                        scaled_pattern[pi, pj] = pattern[min(si, pattern.shape[0] - 1), min(sj, pattern.shape[1] - 1)]

                for pi in range(bh):
                    for pj in range(bw):
                        if scaled_pattern[pi, pj] > 0.4:
                            output[y + pi, x + pj] = 0

        return SkillResult(
            image=numpy_to_pil(np.stack([output] * 3, axis=-1)),
            metadata={"levels": levels, "pattern_scale": pattern_scale},
        )
