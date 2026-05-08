from typing import Any, Dict, List, Optional

from PIL import Image

from .base import ComicSkill, SkillResult
from .factory import SkillRegistry


class ComicPipeline:
    def __init__(self):
        self._steps: List[ComicSkill] = []

    def add_skill(self, skill_name: str, **params) -> "ComicPipeline":
        skill = SkillRegistry.get(skill_name)
        skill._pipeline_params = params
        self._steps.append(skill)
        return self

    def add_skills(self, skill_names: List[str], params_list: Optional[List[dict]] = None) -> "ComicPipeline":
        if params_list is None:
            params_list = [{}] * len(skill_names)
        for name, params in zip(skill_names, params_list):
            self.add_skill(name, **params)
        return self

    def process(self, image: Image.Image) -> SkillResult:
        current_image = image.copy()
        pipeline_meta: Dict[str, Any] = {"pipeline_steps": []}

        for skill in self._steps:
            skill.validate(current_image)
            params = getattr(skill, "_pipeline_params", {})
            result = skill.process(current_image, **params)
            current_image = result.image
            pipeline_meta["pipeline_steps"].append({
                "skill": skill.name,
                "metadata": result.metadata,
            })

        return SkillResult(image=current_image, metadata=pipeline_meta)

    @classmethod
    def from_skill_list(cls, skill_names: List[str], params_list: Optional[List[dict]] = None) -> "ComicPipeline":
        pipeline = cls()
        pipeline.add_skills(skill_names, params_list)
        return pipeline
