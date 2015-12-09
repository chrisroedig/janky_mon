#!/bin/sh -e

echo 'updating submodules'
git submodule init
git submodule update

echo 'building rpi_ws281x...'
(cd libs/rpi_ws281x && sudo scons)

echo 'setting up python bindings for rpi_ws281x...'
(cd libs/rpi_ws281x/python && sudo python setup.py install)

echo 'installing python dependencies'
pip install requests

echo 'done...'

