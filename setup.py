import os

from setuptools import setup


def readfile(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


setup(
    name="landinggear",
    version="0.0.1",
    author="Jeremy Thurgood",
    author_email="firxen@gmail.com",
    description=("Wheels for aeroplanes:"
                 " a tool to extract packages from the pip cache."),
    long_description=readfile("README.rst"),
    license="MIT",
    keywords=["pip", "wheel", "aeroplane", "cache"],
    url="https://github.com/jerith/landinggear",
    install_requires=["pip", "wheel"],
    packages=["landinggear"],
    include_package_data=True,
    entry_points={
        "console_scripts": ['landinggear=landinggear.command:main'],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
)
