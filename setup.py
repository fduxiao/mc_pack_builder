from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="mc_pack_builder",
    version="0.0.1",
    description="convenient way to generate a minecraft datapack or resource pack",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/fduxiao/mc_pack_builder",
    author="fduxiao",  # Optional

    # https://pypi.org/classifiers/
    classifiers=[  # Optional
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",

        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(exclude=["examples", "tests"]),
    python_requires=">=3.7, <4",
    install_requires=["nbtlib"],
    project_urls={
        "Bug Reports": "https://github.com/fduxiao/mc_pack_builder/issues",
        "Source": "https://github.com/fduxiao/mc_pack_builder",
    },
)
