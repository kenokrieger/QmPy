import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qmpy-schrodinger",  # Name for PyPI
    version="3.0.0",
    author="Keno Krieger, Helmut Wecke",
    author_email="kriegerk@uni-bremen.de",
    description="Package for numerical solving of the schroedinger equation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kenokrieger/QmPy",
    package_dir = {"": "source"},
    packages=setuptools.find_packages(where="source"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=['qmsolve', 'parse_legacy_config']
)
