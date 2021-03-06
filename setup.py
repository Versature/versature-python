# -*- coding: utf-8 -*-
"""
Versature's Rest API
------------

"""
from setuptools import setup


setup(
    name='Versature Python API Library',
    version='1.1.0',
    url='https://github.com/Versature/integrate-python.git',
    author='David Ward',
    author_email='dward@versature.com',
    description='A python library for the Versature API',
    long_description=__doc__,
    py_modules=['versature python api'],
    packages=['versature'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'requests-futures'
    ]
)
