"#!/bin/bash"
#sudo python3 /opt/ScanberryPi/main.py
sudo killall freshclam
cd /opt/ScanberryPi/
lxterminal --title="ScanberryPi" --command="bash -ci 'sudo python3 /opt/ScanberryPi/main.py; $SHELL'; 'while [[ \$response != q ]]; do read -n 1 -p [q]uit? response; echo; done'"
