#!/usr/bin/python3.9
#-*- coding: utf-8 -*-
"""
////////////////////////////////////////////////////////////////////////////////////////////////////////

USB Class to use with pyudev class to create a USB object for scanning and perform methods in relation
to the USB Drive object to store data on the object and to manipulate the objects behaviours.

Date:08/04/22
Author: Darren Jackson

////////////////////////////////////////////////////////////////////////////////////////////////////////
"""

#Library imports

from pyudev import Context, Monitor, MonitorObserver
import os
import subprocess
import time
from datetime import datetime
from datetime import date
from collections import deque


#Class declaration
class USB:
    def __init__(self):

       #some USB drive attributes for stoting in the object
       self.USBDEV_UUID = None
       self.USBDEV_VENDOR = None
       self.USBDEV_SERID = None
       self.USBDEV_FSTYPE = None
       self.USBDEV_MODEL = None
       self.USBDEV_DEVPATH = None
       self.USBDEV_HAVEDATA = False
       self.USBDEV_DEVTYPE = None

       self.USBDEV_MNTPATH= '/media/pi'

    #Destructor Method
    def __del__(self):
        print("Destructor called")

    #Method to check if a drive is present and to set the attributes for the object
    def usbPresent(self):
        context = Context()
        for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
            self.USBDEV_VENDOR = device.get('ID_VENDOR')
            self.USBDEV_SERID = device.get('ID_SERIAL')
            self.USBDEV_UUID = device.get('ID_FS_UUID')
            self.USBDEV_FSTYPE = device.get('ID_FS_TYPE')
            self.USBDEV_MODEL = device.get('ID_MODEL')
            self.USBDEV_DEVPATH = device.get('DEVNAME')
            self.USBDEV_DEVTYPE = device.get('DEVTYPE')

            self.USBDEV_HAVEDATA = True

        print("Make: " + str(self.USBDEV_VENDOR))
        print("Serial: " + str(self.USBDEV_SERID))
        print("Model: " + str(self.USBDEV_MODEL))

        print("Partitoned:" + str(self.USBDEV_DEVTYPE))
        print("FileSystem:" + str(self.USBDEV_FSTYPE))
        print("##################################")


    #callback when a usb device is plugged in
    def usbEventCallback(self, action, device):


        if action == 'add':
            #store the device values
            self.USBDEV_VENDOR = device.get('ID_VENDOR')
            self.USBDEV_SERID = device.get('ID_SERIAL')
            self.USBDEV_UUID = device.get('ID_FS_UUID')
            self.USBDEV_FSTYPE = device.get('ID_FS_TYPE')
            self.USBDEV_MODEL = device.get('ID_MODEL')
            self.USBDEV_DEVPATH = device.get('DEVNAME')
            self.USBDEV_DEVTYPE = device.get('DEVTYPE')

            self.USBDEV_HAVEDATA = True

        elif action == 'remove':
            #clear the device data
            self.USBDEV_VENDOR = None
            self.USBDEV_SERID = None
            self.USBDEV_UUID = None
            self.USBDEV_FSTYPE = None
            self.USBDEV_MODEL = None
            self.USBDEV_DEVPATH = None
            self.USBDEV_DEVTYPE = None
            self.USBDEV_HAVEDATA = False

    # Remove USB method reset the object variables back
    def remove_usb(self):
        #clear the device data
        self.USBDEV_VENDOR = None
        self.USBDEV_SERID = None
        self.USBDEV_UUID = None
        self.USBDEV_FSTYPE = None
        self.USBDEV_MODEL = None
        self.USBDEV_DEVPATH = None
        self.USBDEV_DEVTYPE = None
        self.USBDEV_HAVEDATA = False


    #Method to listen for a USB drive been plugged in
    def startListener(self):
        # create a context, create monitor at kernel level, select devices
        context = Context()
        monitor = Monitor.from_netlink(context)
        monitor.filter_by(subsystem='block')


        #Setup object with attributes detected or when removed reset the object back
        def usbEventCallback(self, action, device):


           if action == 'add':
              #store the device values
              self.USBDEV_VENDOR = device.get('ID_VENDOR')
              self.USBDEV_SERID = device.get('ID_SERIAL')
              self.USBDEV_UUID = device.get('ID_FS_UUID')
              self.USBDEV_FSTYPE = device.get('ID_FS_TYPE')
              self.USBDEV_MODEL = device.get('ID_MODEL')
              self.USBDEV_DEVPATH = device.get('DEVNAME')
              self.USBDEV_DEVTYPE = device.get('DEVTYPE')

              self.USBDEV_HAVEDATA = True

           elif action == 'remove':
              #clear the device data
              self.USBDEV_VENDOR = None
              self.USBDEV_SERID = None
              self.USBDEV_UUID = None
              self.USBDEV_FSTYPE = None
              self.USBDEV_MODEL = None
              self.USBDEV_DEVPATH = None
              self.USBDEV_DEVTYPE = None
              self.USBDEV_HAVEDATA = False

         # Try creating observer and catch exception if it can not create it
        try:
           observer = MonitorObserver(monitor, self.usbEventCallback, name="usbdev")
           #set this as the main thread
           observer.setDaemon(False)
           observer.start()
        except Exception as e:
           print(e)

        return observer


    #Method to stop listener for USB devices been connected
    def stopListener(self, observer):
        try:
            self.observer.stop()
        except Exception as e:
            pass


    #Method to check if the device is connected
    def isDeviceConnected(self):
        self.USBDEV_HAVEDATA
        return self.USBDEV_HAVEDATA


    #Method to return the attributes
    def getDevData(self):
        if self.isDeviceConnected():
            return {'UUID': self.USBDEV_UUID,
                   'SERID': self.USBDEV_SERID,
                   'VENDOR': self.USBDEV_VENDOR,
                   'FSTYPE': self.USBDEV_FSTYPE,
                   'MODEL': self.USBDEV_MODEL,
                   'DEVPATH': self.USBDEV_DEVPATH,
                   'DEVTYPE': self.USBDEV_DEVTYPE}
        return None



    #returns the accesible path of the device on the Raspberry pi
    #you can change how the path gets calulated.
    def getMountPathUsbDevice(self):
        self.USBDEV_DEVPATH
        if not self.isDeviceConnected() or self.USBDEV_DEVPATH == None:
            return None

        #check if the dev path exists
        if os.path.exists(self.USBDEV_DEVPATH):

            os.system("sudo mount " + self.USBDEV_MNTPATH )

            #return the path to the folder from root
            truePath = self.USBDEV_MNTPATH

            return truePath

        return None


    #Method to check the drive
    def check_drive(self):
        if self.USBDEV_VENDOR is None:
           return "False"
        else:
           return "True"



    #Method to mount the usb drive by calling a shell script
    def mountUSB(self):
        #exec = subprocess.call(["./shscripts/insusb.sh"])
        #print (exec)
        #if exec == 0:
        #   return "USB DRIVE INSERTED"
        if self.USBDEV_DEVPATH is None:
           return "None"
        else:
           os.system("sudo mount "+ self.USBDEV_DEVPATH +" " +self.USBDEV_MNTPATH)
           return "USB Drive Inserted"




    #Method to eject USB drive
    def ejectUSB(self):
        exec = os.system("sudo umount /media/pi")
        #os.system("sudo killall clamd")
        os.system("sudo killall clamscan")
        os.system("sudo truncate -0 /opt/ScanberryPi/logs/scanReport.log")
        exec >>= 8
        if exec == 0:
           self.usbEventCallback("remove",self)
           #self.remove_usb()
           print("Eject Succesfully")
           print(self.usbPresent)
           return "EJECTED"
        else:
           return "NONE"


    #Insert USB Method
    def insertusb(self):
        connected = "False"
        while connected == "False":
              observering = self.startListener()
              print("Start Listening for USB")
              if self.isDeviceConnected():
                 print("Device Connected")
                 #ex_status = os.system('./shscripts/insusb.sh')
                 #ex_status >>= 8
                 #print(ex_status)
                 #if ex_status == 0:
                 ex_status = self.mountUSB()
                 if ex_status == "USB Drive Inserted":
                    self.stopListener(observering)
                    connected = "True"
                    time.sleep(1)
                    print("drive is connected insert method")
                    return "Drive Connected"
                    break
              time.sleep(1)
              print("INSERT USB")
              #return ("USB WILL NOT MOUNT TO SYSTEM... TRY ANOTHER USB")


    #Method to check the format of a the USB drive
    def check_format(self):
        usb_fs = self.USBDEV_FSTYPE
        return usb_fs



    #Method to format usb drive to a different filesystem
    def format_usb(self,pref_format):
        #Unmount USB
        os.system("sudo umount /media/pi")
        print ("Partition: "+self.USBDEV_DEVTYPE)
        print ("FSTYPE: "+ str(self.USBDEV_FSTYPE))
        if self.USBDEV_DEVTYPE == None:
           os.system("echo ',,7;' | sfdisk /dev/sd[a-z]")
           os.system("mkfs.vfat -I /dev/sd[a-z][0-9]")
           check = self.mountUSB()
           if check == None:
              return "NONE"
           else:
              self.USBDEV_FSTYPE = "vfat"
              return "VFAT"

        elif pref_format == "FAT16":
             os.system("sudo mkfs.fat -F 16 /dev/sd[a-z][0-9]")
             check = self.mountUSB()
             if check == "NONE":
                return "NONE"
             else:
                self.USBDEV_FSTYPE = "fat16"
                return "FAT16"

        elif pref_format == "FAT32":
             os.system("sudo mkfs.fat -F 32 /dev/sd[a-z][0-9]")
             check = self.mountUSB()
             if check == "NONE":
                return "NONE"
             else:
                self.USBDEV_FSTYPE = "fat32"
                return "FAT32"

        elif pref_format == "VFAT":
             os.system("sudo mkfs.vfat /dev/sd[a-z][0-9]")
             check = self.mountUSB()
             if check == "NONE":
                return "NONE"
             else:
                self.USBDEV_FSTYPE = "vfat"
                return "VFAT"

        elif pref_format == "EXFAT":
             os.system("sudo mkfs.exfat /dev/sd[a-z][0-9]")
             check = self.mountUSB()
             if check == "NONE":
                return "NONE"
             else:
                self.USBDEV_FSTYPE = "exfat"
                return "EXFAT"

        elif pref_format == "NTFS":
             os.system("sudo mkfs.ntfs /dev/sd[a-z][0-9]")
             check = self.mountUSB()
             if check == "NONE":
                return "NONE"
             else:
                self.USBDEV_FSTYPE = "ntfs"
                return "NTFS"
        else:
             return "NotFormatted"



    # Scan the USB drive and output the scan results to a log file
    # Has two modes either scan or scan and remove
    def scan_usb(self,mode):
       #variable definitions
       malware = 0
       num_files = 0
       ClamDRun = 5
       today = date.today()

       #Empty the log file
       os.system("sudo truncate -s 0 /opt/ScanberryPi/logs/scanAnalysis.log")
       os.system("sudo truncate -s 0 /opt/ScanberryPi/logs/scanReport.log")
       #os.system("sudo echo 'Usb Scan Report Analysis created:   ('+`date`+')'\n' >> /opt/ScanberryPi/logs/report.log")
       file1 = open("/opt/ScanberryPi/logs/scanReport.log","a")
       file1.write("Scanberry Pi Usb Scan Report Analysis create (%s):\n\n" %datetime.now() )

       time.sleep(1)

       #Check if autorun file exist on usb device and disarm it if it does
       if os.path.isfile("/media/pi/Autorun.inf"):
          os.system("sudo mv /media/pi/Autorun.inf /media/pi/Autorun.inf.DANGER")
          print("Autoinf detected and disarmed")

       # Check to see if clam daemon is running
       ClamDRun = subprocess.call(["systemctl", "is-active", "--quiet", "clamav-daemon"])
       
       #Check scan mode initiated and perform scan based on the mode
       #Check to see if Daemon is running as it can run out of memory on this device
       #If not running it reverts to using the clamav scan method which takes longer
       # As it has to load definitions to memory

       #os.system("echo 'Scanning USB Files' >> /opt/ScanberryPi/logs/lastAnalysis.log")
       if mode == "scan":
       	  #Scan the USB device
       	  #os.system("clamscan -r --verbose /media/pi >> /opt/ScanberryPi/logs/lastAnalysis.log ")
          if(ClamDRun == 0):  # if 0 (active), print "Active"
              print("Calm D Active")
              os.system("sudo clamdscan /media/pi/ --verbose --log /opt/ScanberryPi/logs/scanAnalysis.log")
          else:
              os.system("clamscan -r --verbose /media/pi >> /opt/ScanberryPi/logs/scanAnalysis.log ")
       elif mode == "scanremove":
          if(ClamDRun == 0):
              print("Calm D Active")
              os.system("sudo clamdscan /media/pi/ --remove --verbose --log /opt/ScanberryPi/logs/scanAnalysis.log")
        #If not mode detected just scan and detect
          else:
              os.system("sudo clamscan -r --remove --verbose /media/pi >> /opt/ScanberryPi/logs/scanAnalysis.log")

       # Open analysis file for processing
       openfile = open("/opt/ScanberryPi/logs/scanAnalysis.log","r")
       # Process each line of the file for stings and modify contents of file based on whats found
       for line in openfile:
           if "/media/pi: OK" in line:
              file1.write("\n\nNO KNOWN MALWARE FOUND: on this device still treat as hostile\n\n")

           elif "FOUND" in line and mode == "scanremove":
               print(line)
               malware+=1
               file1.write("Malware Found and removed: " +str(line)+"\n")
           elif "FOUND" in line:
               print(line)
               malware+=1
               file1.write("Malware Found: " +str(line)+"\n")
           elif "OK" in line:
               num_files+=1

       time.sleep(1)

       #for line in (openfile.readlines()[-5:]):
       #    file1.write(line)
       #    print(line +"TESTING")
       #Write out USB object summary of object attribs
       file1.write("\n##################################\n")
       file1.write("_____________USB STATS______________\n")
       file1.write("Make: " + str(self.USBDEV_VENDOR)+"\n")
       file1.write("Serial: " + str(self.USBDEV_SERID)+"\n")
       file1.write("Model: " + str(self.USBDEV_MODEL)+"\n")
       file1.write("Partitoned:" + str(self.USBDEV_DEVTYPE)+"\n")
       file1.write("FileSystem:" + str(self.USBDEV_FSTYPE)+"\n")
       file1.write("####################################\n")

       #Write the last 11 lines of analysis file to report containing clamscan summary:
       #summary = deque(openfile, 11)
       #print (summary)
       #file1.write(summary)
       time.sleep(1)

       # Close files that were opened
       file1.close()
       openfile.close()

       time.sleep(1)
       #Copy the log summary at the end of the report
       os.system("sudo tail -n 5 /opt/ScanberryPi/logs/scanAnalysis.log >> /opt/ScanberryPi/logs/scanReport.log")

       #copy report contents to the history file
       with open("/opt/ScanberryPi/logs/scanReport.log","r") as sreportf, open ("/opt/ScanberryPi/logs/scanHistory.log","a") as shistory:

            #Separate from other scans
            shistory.write("\n\n")
            shistory.write("#############################################\n\n")

            #Copy the content
            for line in sreportf:
                #print(line)
                shistory.write(line)

            #Copy the content
            #reportLines = reportf.readlines()
            #history.writelines(reportLines)


       print("EXITING SCAN FUNCTION")




