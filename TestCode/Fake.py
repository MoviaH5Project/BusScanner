import time

from CallFunctionNonBlocking import call_function_non_blocking
from Peripherals.PeripheralHandler import PeripheralHandler

per = PeripheralHandler()

# Source: https://github.com/gassajor000/pn532pi/blob/master/examples/readMifare.py

import binascii

from pn532pi import Pn532, pn532
from pn532pi import Pn532I2c

PN532_I2C = Pn532I2c(1)
nfc = Pn532(PN532_I2C)


def setup():
    nfc.begin()

    versiondata = nfc.getFirmwareVersion()
    if (not versiondata):
        print("Didn't find PN53x board")
        raise RuntimeError("Didn't find PN53x board")  # halt

    print("Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format((versiondata >> 24) & 0xFF, (versiondata >> 16) & 0xFF,
                                                                (versiondata >> 8) & 0xFF))

    nfc.SAMConfig()

    print("Waiting for an ISO14443A Card ...")


def loop():
    success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

    if success:
        call_function_non_blocking(per.phone_scanned)
        time.sleep(0.5)



if __name__ == '__main__':
    setup()
    while True:
        loop()

