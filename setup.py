from setuptools import find_packages, setup


def get_version() -> str:
    rel_path = "src/closedai/__init__.py"
    with open(rel_path, "r") as fp:
        for line in fp.read().splitlines():
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


requirements = [
    "huggingface_hub>=0.12.0",
]

extras = {}
extras["quality"] = ["black~=23.1", "ruff>=0.0.241"]

setup(
    name="closedai",
    description="ClosedAI is a drop-in replacement for OpenAI.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nateraw/closedai",
    version=get_version(),
    author="Nathan Raw",
    author_email="naterawdata@gmail.com",
    license="Apache",
    install_requires=requirements,
    extras_require=extras,
    package_dir={"": "src"},
    packages=find_packages("src"),
)
