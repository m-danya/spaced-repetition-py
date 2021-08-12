#!/usr/bin/env python

from setuptools import setup, find_packages

requirements = [  ]

setup(
    author="Danila Mikhaltsov",
    author_email='danila-mikh@ya.ru',
    python_requires='>=3.6',
    description="My implementation of a popular method aimed at learning things effectively",
    entry_points={
        'console_scripts': [
            'spaced-repetition=spaced_repetition.main:main',
        ],
    },
    packages=find_packages(include=['spaced_repetition', 'spaced_repetition.*']),
    install_requires=requirements,
    license="MIT license",
    keywords='spaced_repetition',
    name='spaced_repetition',
    url='https://github.com/m-danya/spaced-repetition-py',
    version='0.9.9',
    include_package_data=True,
)
