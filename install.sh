#!/bin/sh

#updating package lists
apt-get update

# Linux packages dependencies
apt-get install wkhtmltopdf -y
apt-get install xvfb -y

# Running pynetwork script
python setup.py install
