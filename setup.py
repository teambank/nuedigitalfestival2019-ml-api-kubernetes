"""Setup
"""
from setuptools import setup, find_packages
from version import get_version
setup(
    name="nuedigitalmlapi", 
    version=get_version(),
    packages=find_packages()
    )
