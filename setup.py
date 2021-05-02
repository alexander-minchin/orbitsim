# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='orbitsim',
    version='0.1.0',
    description='3D orbit simulation visualisation tool',
    long_description=readme,
    author='Alexander Minchin',
    author_email='alexander.w.minchin@gmail.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

