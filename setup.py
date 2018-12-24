import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="docinstance",
    version="0.0.1",
    author="Taewon D. Kim",
    author_email="david.kim.91@gmail.com",
    description="Docstring using flexible objects rather than strings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kimt33/docinstance",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
