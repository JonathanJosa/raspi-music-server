#!/usr/bin/env python3
"""PyBluez simple example sdp-browse.py
Displays services being advertised on a specified bluetooth device.
Author: Albert Huang <albert@csail.mit.edu>
$Id: sdp-browse.py 393 2006-02-24 20:30:15Z albert $
"""

import sys

import bluetooth

nearby_devices = bluetooth.discover_devices(lookup_names=True)
if len(nearby_devices) > 0:
    print("Found %d devices!" % len(nearby_devices))
else:
    print("No devices found! Please check your Bluetooth device and restart the demo!")
    exit(0)

i = 0 # Just an incrementer for labeling the list entries
# Print out a list of all the discovered Bluetooth Devices
for addr, name in nearby_devices:
    print("%s. %s - %s" % (i, addr, name))
    i =+ 1

input("Salida....")
