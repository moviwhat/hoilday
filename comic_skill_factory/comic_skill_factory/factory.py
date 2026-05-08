from typing import Dict, List, Optional, Type

from .base import ComicSkill


class SkillRegistry:
    _skills: Dict[str, Type[ComicSkill]] = {}
    _instances: Dict[str, ComicSkill] = {}

    @classmethod
    def register(cls, skill_cls: Type[ComicSkill]) -> Type[ComicSkill]:
        instance = skill_cls()
        cls._skills[instance.name] = skill_cls
        cls._instances[instance.name] = instance
        return skill_cls

    @classmethod
    def get(cls, name: str) -> ComicSkill:
        if name not in cls._instances:
            available = ", ".join(cls._skills.keys())
            raise KeyError(
                f"未找到技能 '{name}'。可用技能: {available}"
            )
        return cls._instances[name]

    @classmethod
    def list_skills(cls) -> List[str]:
        return list(cls._skills.keys())

    @classmethod
    def get_skill_info(cls, name: str) -> dict:
        skill = cls.get(name)
        return {
            "name": skill.name,
            "description": skill.description,
            "params": skill.get_params_schema(),
        }

    @classmethod
    def list_all_info(cls) -> List[dict]:
        return [cls.get_skill_info(name) for name in cls._skills]


def register_skill(cls: Type[ComicSkill]) -> Type[ComicSkill]:
    return SkillRegistry.register(cls)
