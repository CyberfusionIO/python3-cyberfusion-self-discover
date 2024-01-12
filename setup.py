"""A setuptools based setup module."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="self-discover",
    version="1.0.2",
    description="Self Discover serves autodiscover (Outlook) and autoconfig (Thunderbird) XML files for mail auto-configuration.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    author="William Edwards",
    author_email="support@cyberfusion.nl",
    url="https://github.com/CyberfusionIO/Self-Discover",
    platforms=["linux"],
    packages=find_packages(
        include=[
            "self_discover",
            "self_discover.*",
        ]
    ),
    data_files=[],
    install_requires=["fastapi[all]==0.109.0", "defusedxml==0.7.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "cyberfusion",
        "fastapi",
        "mail",
        "email",
        "outlook",
        "thunderbird",
        "autodiscover",
        "autoconfig",
    ],
    license="MIT",
)
