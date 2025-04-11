from setuptools import setup, find_packages

setup(
    name="one_card_limit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "typing-extensions>=4.0.0",
    ],
    author="Ryan Faris",
    author_email="ryan@idearealm.io",
    description="A One Card Limit Poker implementation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/idea-realm/Simple-Poker-Game",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)