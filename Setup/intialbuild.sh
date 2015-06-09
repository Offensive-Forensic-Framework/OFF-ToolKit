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

func_install_requests(){
  echo ' [*] Installing and updating requests libary'
  #Insure we have the latest requests module in python
  sudo pip install --upgrade requests 

}

# Install Git Dependencies
func_git_deps(){
  echo ' [*] Installing Git Repo Dependencies'
  SIMPLE="$(sudo python -m simplekml)";
  if [[ ${SIMPLE} == *"No module named simplekml"* ]]; then
    echo ' [*] Installing SimpleKml python module'
    cd ${tempdir}
    git clone https://github.com/killswitch-GUI/simplekml.git
    cd simplekml
    sudo python setup.py install
    cd ${tempdir}
    sudo rm -rf simplekml
  fi
  echo ' [*] SimpleKml Already installed in python'
    return 0
}

func_install_googleearth(){
  #Check to see if google earth installed:
  GOOGLE="$(sudo dpkg --list 'googleearth')";
  if [[ ${GOOGLE} == *"Google Earth"* ]]; then
    echo ' [*] Google earth already installed'
    return 0
  fi
  #current way to build google earth
  echo ' [*] Google Earth for KML support'
  sudo apt-get install lsb-core
  sudo apt-get install googleearth-package
  make-googleearth-package --force
  sudo dpkg -i googleearth*
  sudo rm -rf googleearth*.deb
  sudo rm -rf GoogleEarthLinux.bin
}

# Menu Case Statement
case $1 in
  *)
  func_title
  func_check_env
  func_install_requests
  func_git_deps
  func_install_googleearth
  ;;

esac