#!/bin/bash

if [ "$(uname -s)" != "Linux" ]; then
	echo "This script requires Linux operating system, please ensure you are running Linux.";
	exit 1;
fi

sudo -v &> /dev/null

file_name="vitals";
system_path="/etc/systemd/system/";
sudo touch $system_path$file_name".service";

echo "[Unit]" >> $system_path$file_name.service;
echo "Description=System Vitals Service" >> $system_path$file_name.service;

echo "" >> $system_path$file_name.service;

echo "[Service]" >> $system_path$file_name.service;
echo "Which user account should the service be run on ?";
read user;
echo "User="$user >> $system_path$file_name.service;

echo "Please enter your working directory absolute path :";
read directory;
echo "WorkingDirectory="$directory >> $system_path$file_name.service;
echo "Please enter your python execution path relative to the directory path :";
read python;
echo "ExecStart="$python" main.py" >> $system_path$file_name.service;
echo "Should this service always restart ?(Y/N)";
read answer;
if [[ $answer == "Y" || $answer == "y" ]]; then
	echo "Restart=always" >> $system_path$file_name.service;
fi

echo "" >> $system_path$file_name.service;

echo "[Install]" >> $system_path$file_name.service;
echo "WantedBy=multi-user.target" >> $system_path$file_name.service;

echo "Your service was succesfully created at" $system_path$file_name".service";
echo "You can start it right away, or check by yourself if the service is correctly setup and run the command manually";
echo "Should this installer run the commands for you ?(Y/N)";
read setup;
if [[ $setup == "Y" || $setup == "y" ]]; then
	sudo systemctl daemon-reload;
	sudo systemctl start $file_name.service;
	sudo systemctl status $file_name.service;
fi