#!/usr/bin/env python
import os
from setuptools import find_packages
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(here, "RIAssigner", "__version__.py")) as f:
    exec(f.read(), version)

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="RIAssigner",
    version=version["__version__"],
    description="Python library for retention index calculation.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Helge Hecht",
    author_email="hechth.tum@gmail.com",
    url="https://github.com/hechth/RIAssigner",
    packages=find_packages(exclude=['*tests*']),
    license="MIT License",
    zip_safe=False,
    keywords=[
        "gas chromatography",
        "mass spectrometry",
        "retention index"
    ],
    test_suite="tests",
    python_requires='>=3.7',
    install_requires=[ ],
    extras_require={ },
)