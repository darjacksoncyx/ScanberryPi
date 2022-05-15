#!/bin/bash
#Change directory
cd /opt/ScanberryPi/logs

#Check if the USB stick is partitioned
partitioned=1

while read x
do
	if [[ "$x" =~ ^sd[a-z][0-9] ]]; then
		partitioned="0"
	fi;
done << EOF
$(ls /dev)
EOF

#Mount the USB device depending on the number of partitions
if [ "$partitioned" = "0" ]; then
	sudo mount /dev/sd[a-z][0-9] /media/pi
	sudo printf "Partitioned: yes\n" >> ./scanReport.log
else
	sudo mount /dev/sd[a-z] /media/pi
	sudo printf "Partitioned: no\n" >> ./scanReport.log
fi;

#Create a file to store format info
sudo touch /opt/ScanberryPi/checks/checkFormat
sudo chmod +r+w /opt/ScanberryPi/checks/checkFormat


#Store format info about the key
sudo mount | grep /media/pi > /opt/ScanberryPi/checks/checkFormat


