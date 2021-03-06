from setuptools import setup, find_packages

setup(
    name="wnghub",
    version="0.0.1",
    author="Brighton Balfrey",
    author_email="balfrey@usc.edu",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "wnghub = wnghub.__main__:main",
        ],
    },
    install_requires=["marshmallow==3.9.1", "click==7.1.2", "prettytable==2.0.0"],
)
