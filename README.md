# HoloFace
HoloFace, inspired by the InForm project from the MIT, aims at building 3D faces from face recognition and capture. This is the Fablab Project For The Maker Faire Paris 2019.

Setup your raspberry pi
--

install miniconda using:
wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh
md5sum Miniconda3-latest-Linux-armv7l.sh
bash Miniconda3-latest-Linux-armv7l.sh

# get pip and install virtualenv
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo pip install virtualenv virtualenvwrapper

append the following lines at the end of ~/.bashrc
# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh

# install dependency for numpy
sudo apt-get install libatlas3-base

# install more dependencies
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
sudo apt-get install libqtgui4
sudo apt install libqt4-test

# create our virtual env named py3cv34 and install our packages
mkvirtualenv py3cv34 -p python3
source ~/.profile
workon py3cv34
pip install numpy==1.13.3  # this takes time as we build numpy here
pip install "picamera[array]"
pip install pygame
pip install matplotlib
pip install scipy
pip install opencv-contrib-python
pip install dlib

# running
workon py3cv34
cd Holoface
python profiling.py  # or other programs
# on buster, ther is a missing librairy in the compiled binaries. workaround:
$ LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0 ipython
