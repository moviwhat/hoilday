from setuptools import setup, find_packages

setup(
    name="comic_skill_factory",
    version="1.0.0",
    description="图片漫画风格处理 Skill 化工",
    author="",
    packages=find_packages(),
    install_requires=[
        "Pillow>=9.0.0",
        "numpy>=1.20.0",
    ],
    entry_points={
        "console_scripts": [
            "comic-skill = comic_skill_factory.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics",
    ],
)
