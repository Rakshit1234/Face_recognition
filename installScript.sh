# This install script has been tested on Debian 9.3 2018-01-28 4GB SD LXQT for BeagleBone

# Update and Upgrade

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y dist-upgrade
sudo apt-get -y autoremove

# INSTALL THE DEPENDENCIES

# Build tools:
sudo apt-get install -y build-essential cmake

# GUI
sudo apt-get install -y libgtkglext1-dev libvtk6-dev

# Media I/O:
sudo apt-get install -y zlib1g-dev libjpeg-dev libwebp-dev libpng-dev libtiff5-dev libjasper-dev libopenexr-dev libgdal-dev

# Video I/O:
sudo apt-get install -y libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev yasm libopencore-amrnb-dev libopencore-amrwb-dev libv4l-dev libxine2-dev

# Parallelism and linear algebra libraries:
sudo apt-get install -y libtbb-dev libeigen3-dev

# Python:
sudo apt-get install -y python-dev python-tk python-numpy python3-dev python3-tk python3-numpy

# Java:
sudo apt-get install -y ant default-jdk

# Adafruit BBIO Library:
sudo pip install Adafruit_BBIO

# Flite Text to Speech Synthesizer:
sudo apt-get install flite

# pyttsx:
sudo pip install pyttsx

# Documentation:
sudo apt-get install -y doxygen

# Download v3.1.0 .zip file and extract.
curl -sL https://github.com/Itseez/opencv/archive/3.1.0.zip > opencv.zip
unzip opencv.zip

# Download EXTRA MODULES and extract.
curl -sL https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip > opencv_contrib.zip
unzip opencv_contrib.zip

cd opencv-3.1.0
mkdir build
cd build
cmake -DENABLE_PRECOMPILED_HEADERS=OFF -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.1.0/modules -DBUILD_opencv_legacy=OFF -DWITH_OPENGL=ON -DFORCE_VTK=ON -DWITH_TBB=ON -DWITH_GDAL=ON -DWITH_XINE=ON -DBUILD_EXAMPLES=ON ..
make
sudo make install
sudo ldconfig
