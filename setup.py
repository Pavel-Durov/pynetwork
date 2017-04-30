#!/usr/bin/env python

from setuptools import setup
README = open('README.md').read()

setup(
    name="pynetwork",
    version="1.0.0",
    license='MIT',
    description='Network ping/upload/download speed measurements analysis and reports',
    long_description=README,
    url='https://github.com/Pavel-Durov/pynetwork',
    author='Pavel Durov',
    author_email='pdurov0@gmail.com',
    py_modules=["pynetwork"],
    install_requires=[
        'mail', 'requests', 'google-api-python-client', 'httplib2', 'jinja2', 'slackclient'
    ],
    classifiers=[
        'Programming Language: Python 2.7',
        'Programming Language: Python 3.*'
    ],
    entry_points={
        'console_scripts': ['pynetwork=pynetwork:main']
    },
    keywords=['network', 'speedtest', 'notifications', 'reports', 'speed', 'test', 'bandwidth']
)