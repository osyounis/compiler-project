"""Setup configuration for mini-compiler package."""

from pathlib import Path

from setuptools import find_packages, setup

# Read the long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = []
dev_requirements = (this_directory / "requirements-dev.txt").read_text().splitlines()
dev_requirements = [
    line.strip()
    for line in dev_requirements
    if line.strip() and not line.startswith("#")
]

setup(
    name="mini-compiler",
    version="1.0.0",
    author="Omar Younis",
    author_email="your.email@example.com",  # Update with your email
    description="A predictive LL(1) parser and compiler with Python code generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/osyounis/compiler-project",
    project_urls={
        "Bug Reports": "https://github.com/osyounis/compiler-project/issues",
        "Source": "https://github.com/osyounis/compiler-project",
        "CI": "https://github.com/osyounis/compiler-project/actions",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Compilers",
        "Topic :: Education",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
    },
    entry_points={
        "console_scripts": [
            "mini-compiler=mini_compiler.__main__:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
