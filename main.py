#!/usr/bin/python3.9
#-*- coding: utf-8 -*-
"""///////////////////////////////////////////////////////////////////////////////////////////

Main Loop of the program
creates the object and does the basic checking to make sure a USB drive is present when 
opening the program, If not it looks for one to be inserted

Date 08/04/22
Author : Darren Jackson

///////////////////////////////////////////////////////////////////////////////////////////"""

#Import Libraries for use
from gui import *
import USB
import time
import threading

#USB Object drive
drive = USB.USB()
print (drive)

#Variables set for checking
connected = "False"
count = 0

"""Check to see if USB is prensent Already
if so it mounts the drive and begins the program"""
ex_status = os.system('./shscripts/insusb.sh')
ex_status >>= 8
print (ex_status)
#ex_status = drive.mountUSB()
#if ex_status == "USB Drive Inserted":
if ex_status == 0:
   connected = "True"
   drive.usbPresent()
   main_menu(drive)

""" If the drive is not present start the observer to listen for USB events
Once a usb drive is detected it breaks the loop and starts the program"""
#start listening for usb device change events
#you may have to unplug the flashdrive and replug
while connected == "False":


      observer = drive.startListener()

      #get the status of the connected usb device
      status = drive.isDeviceConnected()
      print (status)


      #get some identification data
      #returns a dict with keys UUID, SERID (for serial ID),
      #VENDOR (the manufacturer), FSTYPE (file system), MODEL (the model), DEVPATH for the path under ~/dev.
      device = drive.getDevData()
      print (device)


      #get the path (currently set for Rpi, can be changed)
      path = drive.getMountPathUsbDevice()
      print("PLEASE INSERT USB DRIVE")
      print("Stat: " + str(status))
      print("dev: " + str(device))
      print("path: " + str(path))
      print("############################")
      count += 1


      #STOP USB LISTENER
      if drive.isDeviceConnected():
         #ins_usb_msg("close")
         ex_status = os.system('./shscripts/insusb.sh')
         ex_status >>= 8
         if ex_status == 0:
            drive.stopListener(observer)
            connected = "True"
            time.sleep(2)
            break
         print ("USB WILL NOT MOUNT TO SYSTEM... TRY ANOTHER USB")


      time.sleep(4)

if count >=1:
   drive.usbPresent()
   threading.Thread(target=main_menu(drive)).start()





