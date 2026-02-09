"""Setup configuration for NetEngine."""

from setuptools import setup, find_packages

setup(
    name="netengine",
    version="1.0.0",
    description="Multithreaded Networking Engine with ProxyChains Support",
    author="NetEngine Team",
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "netengine=netengine.cli.cli:CLI().run",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
)
