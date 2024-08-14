"""A setuptools based setup module."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="self-discover",
    version="1.0.2",
    description="self-discover serves autodiscover (Outlook) and autoconfig (Thunderbird) XML files for mail auto-configuration.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Cyberfusion",
    author_email="support@cyberfusion.io",
    url="https://github.com/CyberfusionIO/self-discover",
    platforms=["linux"],
    packages=find_packages(
        include=[
            "self_discover",
            "self_discover.*",
        ]
    ),
    data_files=[],
    install_requires=["fastapi[all]==0.112.0", "defusedxml==0.7.1"],
)
