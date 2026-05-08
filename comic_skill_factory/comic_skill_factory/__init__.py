from .base import ComicSkill, SkillResult
from .factory import SkillRegistry
from .pipeline import ComicPipeline
from . import skills as _skills  # noqa: F401 — 触发技能注册

__version__ = "1.0.0"
__all__ = ["ComicSkill", "SkillResult", "SkillRegistry", "ComicPipeline"]
