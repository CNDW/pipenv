import ast
import os

from setuptools import setup, find_packages

ROOT = os.path.dirname(__file__)

PACKAGE_NAME = "private_package_a"

VERSION = None

with open(os.path.join(ROOT, "src", PACKAGE_NAME.replace("-", "_"), "__init__.py")) as f:
    for line in f:
        if line.startswith("__version__ = "):
            VERSION = ast.literal_eval(line[len("__version__ = ") :].strip())
            break
if VERSION is None:
    raise OSError("failed to read version")

setup(
    name=PACKAGE_NAME,
    # These really don't work.
    package_dir={"": "src"},
    packages=find_packages("src"),
    # I don't know how to specify an empty key in setup.cfg.
    package_data={
        "": ["LICENSE*", "README*"],
    },
    install_requires=[
        "six>=0.0.1",
        "private-package-b>=0.0.1",
    ],
    description="A fake python package.",
    author="Dan Ryan",
    author_email="dan@danryan.co",
    url="https://github.com/sarugaku/legacy_backend_package",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python",
    ],
    setup_requires=["setuptools-git-versioning"],
)
