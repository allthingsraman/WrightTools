#! /usr/bin/env python3

import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(fname):
    with open(os.path.join(here, fname)) as f:
        return f.read()


extra_files = {
    "WrightTools": [
        "datasets",
        "datasets/*",
        "datasets/*/*",
        "datasets/*/*/*",
        "datasets/*/*/*/*",
        "CITATION",
        "VERSION",
        "WT5_VERSION",
    ]
}

with open(os.path.join(here, "WrightTools", "VERSION")) as version_file:
    version = version_file.read().strip()

docs_require = ["sphinx", "sphinx-gallery==0.8.2", "sphinx-rtd-theme"]

setup(
    name="WrightTools",
    packages=find_packages(exclude=("tests", "tests.*")),
    package_data=extra_files,
    python_requires=">=3.7",
    install_requires=[
        "h5py",
        "imageio",
        "matplotlib>=3.4.0",
        "numexpr",
        "numpy>=1.15.0",
        "pint",
        "python-dateutil",
        "scipy",
        "click",
        "tidy_headers>=1.0.0",
        "rich",
    ],
    extras_require={
        "docs": docs_require,
        "dev": [
            "black",
            "pre-commit",
            "pydocstyle",
            "pytest",
            "pytest-cov",
            "databroker>=1.2",
            "msgpack",
        ]
        + docs_require,
    },
    version=version,
    description="Tools for loading, processing, and plotting multidimensional spectroscopy data.",
    long_description=read("README.rst"),
    author="WrightTools Developers",
    license="MIT",
    url="http://wright.tools",
    keywords="spectroscopy science multidimensional visualization",
    entry_points={"console_scripts": [
        "wt-tree=WrightTools.__main__:tree", 
        "wt5=WrightTools.__main__:wt5", 
        "wt-convert=WrightTools.__main__:convert"
    ]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Framework :: Matplotlib",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
    ],
)
