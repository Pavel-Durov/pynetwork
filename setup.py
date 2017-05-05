#!/usr/bin/env python

from setuptools import setup
README = open('README.md').read()

setup(
    name="pynetwork",
    version="0.1dev",
    packages=['pynetwork'],
    license='MIT',
    description='Network ping/upload/download speed measurements analysis and reports',
    long_description=README,
    url='https://github.com/Pavel-Durov/pynetwork',
    install_requires=[
        'mail', 'requests', 'google-api-python-client', 'httplib2', 'jinja2', 'slackclient'
    ],
    keywords=['network', 'speedtest', 'notifications', 'reports', 'speed', 'test', 'bandwidth']
)