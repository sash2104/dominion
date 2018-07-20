""" Installs the Dominion simulator."""

from setuptools import setup, find_packages


setup(
    name='Dominion',
    version='0.0',
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        dominion=pydominion.main:main
    ''',
)
