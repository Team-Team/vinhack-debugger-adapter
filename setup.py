import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "vinhack-debug",
    version = "0.0.1",
    author = "Naman Agrawal",
    author_email = "naman2003now@gmail.com",
    description = "A Visual Debgger for python",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "github.com",
    install_requires=['flask',
                      'flask-cors',                     
                      'gitpython',
                      ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = setuptools.find_packages(),
    python_requires = ">=3.7"
)
