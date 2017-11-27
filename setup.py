#!/usr/bin/env python

from os.path import exists
from setuptools import setup, find_packages

setup(
    name='lightbus-examples',
    version=open('VERSION').read().strip(),
    author='Adam Charnock',
    author_email='adam@adamcharnock.com',
    packages=find_packages(),
    url='https://github.com/adamcharnock/lightbus-examples',
    license='MIT',
    description='Example projects using Lightbus',
    long_description=open('README.rst').read() if exists("README.rst") else "",
    install_requires=[
        'lightbus',
        'dataset',
    ],
    include_package_data=True,
)
