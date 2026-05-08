from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from PIL import Image


@dataclass
class SkillResult:
    image: Image.Image
    metadata: Dict[str, Any] = field(default_factory=dict)


class ComicSkill(ABC):
    name: str = "base"
    description: str = "基础漫画风格技能"

    @abstractmethod
    def process(self, image: Image.Image, **kwargs) -> SkillResult:
        ...

    def validate(self, image: Image.Image) -> bool:
        if not isinstance(image, Image.Image):
            raise TypeError(f"期望 PIL.Image 类型，得到 {type(image)}")
        if image.size[0] == 0 or image.size[1] == 0:
            raise ValueError("图片尺寸不能为零")
        return True

    def get_params_schema(self) -> Dict[str, Any]:
        return {}

    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}')>"
