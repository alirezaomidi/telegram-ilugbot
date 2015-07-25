#! /bin/bash

sudo apt-get -y install python-pip
sudo pip install --upgrade -r requirements.txt

if [ $? -eq 0 ]; then
	echo -e "\nDone!"
else
	echo -e "\nError!"
fi
