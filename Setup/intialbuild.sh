#!/bin/bash


# Current supported platforms: 
#   Kali-Linux
# Global Variables
runuser=$(whoami)
tempdir=$(pwd)

# Title Function
func_title(){
  # Clear (For Prettyness)
  clear

  # Echo Title
  echo '=========================================================================='
  echo ' Setup Script | [Updated]: '
  echo '=========================================================================='
  echo ' [Web]: https://www. | [Twitter]: @'
  echo '=========================================================================='
}



# Environment Checks
func_check_env(){
  # Check Sudo Dependency going to need that!
  if [ $(which sudo|wc -l) -eq '0' ]; then
    echo
    echo ' [ERROR]: This Setup Script Requires sudo!'
    echo '          Please Install sudo Then Run This Setup Again.'
    echo
    exit 1
  fi
}

func_instal(){
#Insure we have the latest requests module in python
sudo pip install --upgrade requests 
#Install SimpleKML into python
python simplekml/setup.py
python wigle/.setup.py
build Googleearth