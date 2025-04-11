from setuptools import setup, find_packages

# Read dependencies from requirements.txt
def load_requirements(filename="requirements.txt"):
    with open(filename, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="RunScope",
    version="0.1.0",
    author="Joan Gracia",
    description="A Python package to compute and analyze advanced running metrics from GPS data.",
    packages=find_packages(),
    install_requires=load_requirements(),
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
