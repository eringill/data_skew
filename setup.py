import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data_skew-egill", 
    version="0.0.1",
    author="Erin Gill",
    author_email="erin.gill81@gmail.com",
    description="Methods to automatically remove outliers from numerical data, plot histograms and detect skewness",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/egill/data_skew",
    packages=setuptools.find_packages(),
    package_data={
        "": ["*.csv"],
    }
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL 3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)