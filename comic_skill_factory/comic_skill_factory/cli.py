import argparse
import sys

from PIL import Image

from . import SkillRegistry, ComicPipeline


def main():
    parser = argparse.ArgumentParser(
        prog="comic-skill",
        description="图片漫画风格处理 Skill 化工",
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    list_parser = subparsers.add_parser("list", help="列出所有可用技能")
    info_parser = subparsers.add_parser("info", help="查看技能详情")
    info_parser.add_argument("skill", type=str, help="技能名称")

    process_parser = subparsers.add_parser("process", help="处理图片")
    process_parser.add_argument("input", type=str, help="输入图片路径")
    process_parser.add_argument("output", type=str, help="输出图片路径")
    process_parser.add_argument("--skill", "-s", type=str, action="append", dest="skills",
                                required=True, help="要使用的技能（可多次指定，按顺序执行）")
    process_parser.add_argument("--param", "-p", type=str, action="append", dest="params",
                                default=[], help="技能参数，格式: key=value（与 --skill 顺序对应）")

    args = parser.parse_args()

    if args.command == "list":
        print("可用技能:")
        print("-" * 40)
        for info in SkillRegistry.list_all_info():
            print(f"  {info['name']:<20} {info['description']}")

    elif args.command == "info":
        info = SkillRegistry.get_skill_info(args.skill)
        print(f"技能: {info['name']}")
        print(f"描述: {info['description']}")
        if info["params"]:
            print("参数:")
            for k, v in info["params"].items():
                print(f"  --{k:<20} {v.get('description', '')} (默认: {v.get('default', 'N/A')})")
        else:
            print("参数: 无")

    elif args.command == "process":
        params_list = []
        for param_str in args.params:
            params_list.append({})
            for pair in param_str.split(","):
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    try:
                        v = float(v) if "." in v else int(v)
                    except ValueError:
                        pass
                    params_list[-1][k.strip()] = v

        if not params_list:
            params_list = [{}] * len(args.skills)
        elif len(params_list) < len(args.skills):
            params_list.extend([{}] * (len(args.skills) - len(params_list)))

        image = Image.open(args.input)
        pipeline = ComicPipeline.from_skill_list(args.skills, params_list)
        result = pipeline.process(image)
        result.image.save(args.output)
        print(f"处理完成 → {args.output}")
        print(f"管道步骤: {' → '.join(args.skills)}")
        for step in result.metadata.get("pipeline_steps", []):
            step_meta = {k: v for k, v in step["metadata"].items()}
            if step_meta:
                print(f"  [{step['skill']}] 参数: {step_meta}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
