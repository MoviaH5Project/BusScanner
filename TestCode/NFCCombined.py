# Combined version of NFCAndroidHCE.py and NFCMifare.py
import time
import binascii

from pn532pi import Pn532, pn532
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

    # Set the max number of retry attempts to read from a card
    # This prevents us from waiting forever for a card, which is
    # the default behaviour of the PN532.
    # nfc.setPassiveActivationRetries(0xFF)

    # configure board to read RFID tags
    nfc.SAMConfig()


def loop():
    print("Waiting for a card or phone")

    # set shield to inListPassiveTarget
    success = nfc.inListPassiveTarget()

    if (success):

        print("Found something!")

        # region try reading Android HCE
        selectApdu = bytearray([0x00,  # CLA
                                0xA4,  # INS
                                0x04,  # P1
                                0x00,  # P2
                                0x07,  # Length of AID
                                0xF0, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06,  # AID defined on Android App
                                0x00  # Le
                                ])

        success, response = nfc.inDataExchange(selectApdu)
        # endregion

        if (success):  # Read Android HCE
            print("responseLength: {:d}", len(response))
            print(binascii.hexlify(response))

            while (success):
                apdu = bytearray(b"Hello from Arduino")
                success, back = nfc.inDataExchange(apdu)

                if (success):
                    print("responseLength: {:d}", len(back))
                    print(binascii.hexlify(back))
                else:
                    print("Broken connection?")
        else:
            print("Failed sending SELECT AID")
            # Try mifare
            read_mifare()
    else:
        print("Didn't find anything!")

    time.sleep(1)


def read_mifare():
    #  Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
    #  'uid' will be populated with the UID, and uidLength will indicate
    #  if the uid is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)
    success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

    if (success):
        #  Display some basic information about the card
        print("Found an ISO14443A card")
        print("UID Length: {:d}".format(len(uid)))
        print("UID Value: {}".format(binascii.hexlify(uid)))

        if (len(uid) == 4):
            #  We probably have a Mifare Classic card ...
            print("Seems to be a Mifare Classic card (4 byte UID)")

            #  Now we need to try to authenticate it for read/write access
            #  Try with the factory default KeyA: 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF
            print("Trying to authenticate block 4 with default KEYA value")
            keya = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

            #  Start with block 4 (the first block of sector 1) since sector 0
            #  contains the manufacturer data and it's probably better just
            #  to leave it alone unless you know what you're doing
            success = nfc.mifareclassic_AuthenticateBlock(uid, 4, 0, keya)

            if (success):
                print("Sector 1 (Blocks 4..7) has been authenticated")

                #  If you want to write something to block 4 to test with, uncomment
                #  the following line and this text should be read back in a minute
                # data = bytearray([ 'a', 'd', 'a', 'f', 'r', 'u', 'i', 't', '.', 'c', 'o', 'm', 0, 0, 0, 0])
                # success = nfc.mifareclassic_WriteDataBlock (4, data)

                #  Try to read the contents of block 4
                success, data = nfc.mifareclassic_ReadDataBlock(4)

                if (success):
                    #  Data seems to have been read ... spit it out
                    print("Reading Block 4: {}".format(binascii.hexlify(data)))
                    return True

                else:
                    print("Ooops ... unable to read the requested block.  Try another key?")
            else:
                print("Ooops ... authentication failed: Try another key?")

        elif (len(uid) == 7):
            #  We probably have a Mifare Ultralight card ...
            print("Seems to be a Mifare Ultralight tag (7 byte UID)")

            #  Try to read the first general-purpose user page (#4)
            print("Reading page 4")
            success, data = nfc.mifareultralight_ReadPage(4)
            if (success):
                #  Data seems to have been read ... spit it out
                binascii.hexlify(data)
                return True

            else:
                print("Ooops ... unable to read the requested page!?")

    return False


def setupNFC():
    nfc.begin()

    versiondata = nfc.getFirmwareVersion()
    if not versiondata:
        print("Didn't find PN53x board")
        raise RuntimeError("Didn't find PN53x board")  # halt

    # Got ok data, print it out!
    print("Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format((versiondata >> 24) & 0xFF, (versiondata >> 16) & 0xFF,
                                                                (versiondata >> 8) & 0xFF))

    # configure board to read RFID tags
    nfc.SAMConfig()


if __name__ == '__main__':
    setup()
    while True:
        loop()
