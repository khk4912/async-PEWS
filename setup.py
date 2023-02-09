"""Install packages as defined in this file into the Python environment."""
from setuptools import setup, find_packages

setup(
    name="async-pews",
    author="khk4912",
    author_email="vb.net@kakao.com",
    url="https://github.com/khk4912/async-PEWS",
    description="PEWS Python asynchronous client.",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "setuptools",
        "aiohttp",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.0",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
    ],
)
