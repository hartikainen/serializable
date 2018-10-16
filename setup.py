from distutils.core import setup
from setuptools import find_packages

NAME = 'Serializable'
VERSION = '0.1.0'

setup(
    name=NAME,
    packages=find_packages(),
    version=VERSION,
    description="Utilities for handling serializable classes.",
    author='Kristian Hartikainen',
    author_email='kristian.hartikainen@gmail.com',)
