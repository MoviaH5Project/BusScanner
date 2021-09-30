# Source: https://github.com/gassajor000/pn532pi/blob/master/examples/readMifare.py

import binascii
from datetime import datetime

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

    # print("Waiting for an ISO14443A Card ...")


def loop():
    success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)
    if success:
        #  Display some basic information about the card
        # print("Found an ISO14443A card")
        # print("UID Length: {:d}".format(len(uid)))
        print("UID Value: {}".format(binascii.hexlify(uid)))
        while success:
            success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS, timeout=10)
    return False


if __name__ == '__main__':
    setup()
    found = loop()
    while not found:
        found = loop()
