import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("VERSION.txt", "r", encoding="utf-8") as v:
    version = v.read()

setuptools.setup(
    name="teamtrakapi-pkg-billycohen96",  # Replace with your own username
    version=version,
    author="William Cohen",
    author_email="k1763966@kcl.ac.uk",
    description="A package used for handling API requests related to the TeamTrak project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    include_package_data=True
)
