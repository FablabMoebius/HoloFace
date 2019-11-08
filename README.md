# HoloFace
HoloFace, inspired by the InForm project from the MIT, aims at building 3D faces from face recognition and capture. This is the Fablab Project For The Maker Faire Paris 2019.

Setup your raspberry pi
--

install miniconda using:
wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh
md5sum Miniconda3-latest-Linux-armv7l.sh
bash Miniconda3-latest-Linux-armv7l.sh

sudo pip install virtualenv virtualenvwrapper
mkvirtualenv py3cv34 -p python3
pip install numpy=1.13.3
pip install pygame
pip install matplotlib
pip install scipy opencv-contrib-python

source ~/.profile
workon py3cv34
cd Holoface
python profiling.py