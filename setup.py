#!python
# -*- coding: utf-8 -*-
'''
@File: setup.py
@Date: 2021/05/20 17:01:53
@Version: 1.0
@Description: None
'''

from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name='cdtf', # project name
    version='0.1.0', # versiion
    author='Baoming Yu', # author's name
    author_email='dingxuanliang@icloud.com', # author's email
    url='https://github.com/Baoming520/cdtf', # url on github
    description='This is a case-driven test framework.', # abstract
    long_description=readme(), # contents in README.MD file
    long_description_content_type="text/markdown", # type of long description
    packages=['cdtf'], # pakages waiting for packing
    package_data={}, # data files in package
    install_requires=[], # required packages
)