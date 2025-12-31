from setuptools import setup, find_packages

setup(
    name="stateshaper",
    version="0.1.0",
    description="Create infinite deterministic data from a small seed. Compressed. Reproducible. Reversible. Jump to any state from anywhere.",
    author="Jason G. Dunn",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
)
