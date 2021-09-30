# Source: https://github.com/gassajor000/pn532pi/blob/master/examples/android_hce.py
# For a working example app that can send data see: https://github.com/grundid/host-card-emulation-sample

import binascii

from pn532pi import Pn532
from pn532pi import Pn532I2c

PN532_I2C = Pn532I2c(1)
nfc = Pn532(PN532_I2C)


def setup():
    print("-------Peer to Peer HCE--------")

    nfc.begin()

    versiondata = nfc.getFirmwareVersion()
    if not versiondata:
        print("Didn't find PN53x board")
        raise RuntimeError("Didn't find PN53x board")  # halt

    # Got ok data, print it out!
    print("Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format((versiondata >> 24) & 0xFF, (versiondata >> 16) & 0xFF,
                                                                (versiondata >> 8) & 0xFF))

    nfc.SAMConfig()


def loop():
    #print("Waiting for an ISO14443A card")

    success = nfc.inListPassiveTarget()

    if (success):

        #print("Found something!")

        selectApdu = bytearray([0x00,  # CLA
                                0xA4,  # INS
                                0x04,  # P1
                                0x00,  # P2
                                0x07,  # Length of AID
                                0xF0, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06,  # AID defined on Android App
                                0x00  # Le
                                ])

        success, response = nfc.inDataExchange(selectApdu)

        if (success):

            #print("responseLength: {:d}", len(response))
            #print(binascii.hexlify(response))
            print(response.decode())
        else:
            pass
            #print("Failed sending SELECT AID")
    else:
        pass
        #print("Didn't find anything!")


def setupNFC():
    nfc.begin()

    versiondata = nfc.getFirmwareVersion()
    if not versiondata:
        print("Didn't find PN53x board")
        raise RuntimeError("Didn't find PN53x board")  # halt

    print("Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format((versiondata >> 24) & 0xFF, (versiondata >> 16) & 0xFF,
                                                                (versiondata >> 8) & 0xFF))

    nfc.SAMConfig()


if __name__ == '__main__':
    setup()
    while True:
        loop()
