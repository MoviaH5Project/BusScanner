# Source: https://github.com/IanHarvey/bluepy/blob/master/bluepy/blescan.py

from __future__ import print_function
import argparse
import binascii
import os
import sys
from bluepy import btle


class ScanPrint(btle.DefaultDelegate):

    def __init__(self, sensitivity=-128):
        btle.DefaultDelegate.__init__(self)
        self.sensitivity = sensitivity

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            status = "new"
        elif isNewData:
            status = "update"
        else:
            status = "old"

        if dev.rssi < self.sensitivity:
            return

        print(f'Device ({status}): {dev.addr} ({dev.addrType}), {dev.rssi} dBm {"" if dev.connectable else "(not connectable)"}')
        for (sdid, desc, val) in dev.getScanData():
            if sdid in [8, 9]:
                print(desc + ': \'' + val + '\'')
            else:
                print(desc + ': <' + val + '>')
        if not dev.scanData:
            print('\t(no data)')


def main():
    btle.Debugging = False

    scanner = btle.Scanner(0).withDelegate(ScanPrint())

    print("Scanning for devices...")
    devices = scanner.scan(0)


if __name__ == "__main__":
    main()
