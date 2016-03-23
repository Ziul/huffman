#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
huffman
===================
A file compactor
"""
from setuptools import setup, find_packages

install_requires = [
    'bitarray>=0.8.1',
    'ipdb>=0.9.0',
    'optparse-pretty>=0.1.1',
    'bintrees>=2.0.2',
]


setup(
    name="huffman",
    version='0.0.8',
    author='Luiz Oliveira',
    author_email='ziuloliveira@gmail.com',
    url='https://gitlab.com/Ziul/huffman/',
    entry_points={
        'console_scripts': [
            'huffman = huffman:main',
            # 'main-test = main:test',
        ]},
    description='A program to compact/descompact a file',
    long_description=__doc__,
    license='GPLv3',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    test_suite="tests.run.runtests",
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3',
        'Topic :: Utilities',
    ],
)
