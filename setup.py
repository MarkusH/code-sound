#!/usr/bin/env python

from pkg_resources.extern.packaging.version import Version
from setuptools import find_packages, setup


setup(
    name="code_sound",
    author="Markus Holtermann, Michael Kleen, Sergei Zyubin",
    author_email="info+code-sound@markusholtermann.eu",
    url="https://github.com/MarkusH/code-sound",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "pysndfx==0.3.6",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
