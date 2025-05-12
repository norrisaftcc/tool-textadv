"""
Setup script for the text adventure package.
"""

from setuptools import setup, find_packages

setup(
    name="text_adv",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "adventurelib>=1.2.1",
        "colorama>=0.4.6",
        "streamlit>=1.29.0",
    ],
)