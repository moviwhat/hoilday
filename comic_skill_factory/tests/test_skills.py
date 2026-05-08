import unittest
from PIL import Image

from comic_skill_factory import SkillRegistry, ComicPipeline


class TestSkills(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_image = Image.new("RGB", (100, 100), color=(128, 128, 128))
        cls.color_image = Image.new("RGB", (120, 80), color=(200, 100, 50))

    def test_skill_registry_has_skills(self):
        names = SkillRegistry.list_skills()
        self.assertGreater(len(names), 0)

    def test_each_skill_processes(self):
        for name in SkillRegistry.list_skills():
            with self.subTest(skill=name):
                skill = SkillRegistry.get(name)
                result = skill.process(self.color_image)
                self.assertIsInstance(result.image, Image.Image)
                self.assertEqual(result.image.size, self.color_image.size)

    def test_skill_info(self):
        info = SkillRegistry.list_all_info()
        self.assertGreater(len(info), 0)
        for item in info:
            self.assertIn("name", item)
            self.assertIn("description", item)
            self.assertIn("params", item)

    def test_get_invalid_skill(self):
        with self.assertRaises(KeyError):
            SkillRegistry.get("nonexistent_skill")

    def test_pipeline_single_skill(self):
        pipeline = ComicPipeline.from_skill_list(["pop_art"])
        result = pipeline.process(self.color_image)
        self.assertIsInstance(result.image, Image.Image)
        steps = result.metadata.get("pipeline_steps", [])
        self.assertEqual(len(steps), 1)
        self.assertEqual(steps[0]["skill"], "pop_art")

    def test_pipeline_multiple_skills(self):
        pipeline = ComicPipeline.from_skill_list(["line_art", "halftone"])
        result = pipeline.process(self.color_image)
        steps = result.metadata.get("pipeline_steps", [])
        self.assertEqual(len(steps), 2)

    def test_pipeline_with_params(self):
        pipeline = ComicPipeline.from_skill_list(
            ["halftone"], [{"dot_size": 4, "contrast": 1.5}]
        )
        result = pipeline.process(self.color_image)
        step = result.metadata["pipeline_steps"][0]
        self.assertEqual(step["metadata"]["dot_size"], 4)
        self.assertEqual(step["metadata"]["contrast"], 1.5)

    def test_skill_result_metadata(self):
        skill = SkillRegistry.get("line_art")
        result = skill.process(self.color_image, edge_strength=0.8, invert=False)
        self.assertEqual(result.metadata["edge_strength"], 0.8)
        self.assertFalse(result.metadata["invert"])


if __name__ == "__main__":
    unittest.main()
