echo 'updating submodules'
git submodule init
git submodule update

echo 'building rpi_ws281x...'
cd libs/rpi_ws281x
sudo scons

echo 'setting up python bindings for rpi_ws281x...'
cd python
python setup.py install

cd ../../

echo 'done...'
