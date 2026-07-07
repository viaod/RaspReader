# Setting up raspberry pi 

## stop entering sudo password

```
sudo visudo

# add to bottom of file 
viaod ALL=(ALL) NOPASSWD: ALL
```


## setting up static IP address

https://johnj.com/posts/e-paper-rpi-display/

```

```

## Screen

https://www.waveshare.com/wiki/3.7inch_e-Paper_HAT+_(G)_Manual#Raspberry_Pi
https://www.waveshare.com/wiki/3.7inch_e-Paper_HAT%2B_(G)
https://github.com/waveshareteam/e-Paper/tree/master

```
sudo raspi-config
# Select Interfacing Options -> SPI -> Yes to enable the SPI interface

sudo reboot

# Install the libraries required for the virtual environment
sudo apt-get update
sudo apt-get install git python3-pip -y
sudo apt install python3-venv

# Create a new virtual environment (myenv is the name of the virtual environment, which can be modified)
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Install the libraries 
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo apt-get install python3-spidev

sudo apt-get update
sudo apt install python3-gpiozero

pip install spidev
pip install gpiozero lgpio
pip install pillow

# Exit the virtual environment
deactivate
```

## Encoder

https://learn.adafruit.com/adafruit-ano-rotary-navigation-encoder-to-i2c-stemma-qt-adapter

```
# install blika in venv 
cd ~
pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo -E env PATH=$PATH python3 raspi-blinka.py

# check I2C and SPI
ls /dev/i2c* /dev/spi*

# add second SPI
sudo nano /boot/firmware/config.txt
# add:
# dtoverlay=spi1-3cs

pip install adafruit-circuitpython-seesaw

# increase encoder bus speed
sudo nano /boot/firmware/config.txt
# /boot/firmware/config.txt

```