from comic_skill_factory import SkillRegistry, ComicPipeline
from PIL import Image


def demo_single_skills(input_path: str, output_dir: str = "."):
    image = Image.open(input_path)

    for skill_name in SkillRegistry.list_skills():
        skill = SkillRegistry.get(skill_name)
        result = skill.process(image)
        output_path = f"{output_dir}/demo_{skill_name}.png"
        result.image.save(output_path)
        print(f"[{skill_name}] 已保存 → {output_path}")


def demo_pipeline(input_path: str, output_path: str):
    image = Image.open(input_path)

    pipeline = (
        ComicPipeline()
        .add_skill("line_art", edge_strength=1.2, invert=True)
        .add_skill("watercolor", smooth_radius=2, color_boost=1.4, edge_darken=0.3)
    )
    result = pipeline.process(image)
    result.image.save(output_path)
    print(f"[Pipeline: line_art → watercolor] 已保存 → {output_path}")
    print(f"管道元数据: {result.metadata}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python demo.py <输入图片路径> [输出目录]")
        print("示例: python demo.py photo.jpg ./output")
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    print("=" * 50)
    print("Demo 1: 逐个技能处理")
    print("=" * 50)
    demo_single_skills(input_path, output_dir)

    print()
    print("=" * 50)
    print("Demo 2: 管道组合处理 (线稿 + 水彩)")
    print("=" * 50)
    demo_pipeline(input_path, f"{output_dir}/demo_pipeline_lineart_watercolor.png")
