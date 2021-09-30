import time
import binascii

from pn532pi import Pn532, pn532
from pn532pi import Pn532I2c

from Devices.DeviceHandler import DeviceHandler
from CallFunctionNonBlocking import call_function_non_blocking
from LoggerInterface import LoggerInterface
from Peripherals.PeripheralHandler import PeripheralHandler


class NFC:
    def __init__(self, peripheral_handler: PeripheralHandler, device_handler: DeviceHandler, logger: LoggerInterface):
        self.logger = logger
        self.device_handler = device_handler
        self.pn532_i2c = Pn532I2c(1)
        self.nfc = Pn532(self.pn532_i2c)
        self.peripheral_handler: PeripheralHandler = peripheral_handler
        self.setup()

    def setup(self):
        self.logger.log("NFC started")

        self.nfc.begin()

        versiondata = self.nfc.getFirmwareVersion()
        if not versiondata:
            self.logger.log("Didn't find PN53x board", level=self.logger.CRITICAL)
            raise RuntimeError("Didn't find PN53x board")  # halt

        # Got ok data, print it out!
        self.logger.log("Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format((versiondata >> 24) & 0xFF,
                                                                              (versiondata >> 16) & 0xFF,
                                                                              (versiondata >> 8) & 0xFF),
                        level=self.logger.INFO)

        # configure board to read RFID tags
        self.nfc.SAMConfig()

    def loop(self):
        while True:
            self.logger.log("Waiting for a card or phone", self.logger.DEBUG)

            success = self.nfc.inListPassiveTarget()

            if (success):
                self.logger.log("Found something!", self.logger.INFO)

                # region try reading Android HCE
                selectApdu = bytearray([0x00,  # CLA
                                        0xA4,  # INS
                                        0x04,  # P1
                                        0x00,  # P2
                                        0x07,  # Length of AID
                                        0xF0, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06,  # AID defined on Android App
                                        0x00  # Le
                                        ])

                success, response = self.nfc.inDataExchange(selectApdu)
                # endregion

                if success:  # Read Android HCE
                    self.logger.log(f'Read from HCE: {response.decode()}', self.logger.INFO)
                    call_function_non_blocking(self.peripheral_handler.phone_scanned)
                else:
                    success, uid = self.nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

                    if success and uid != bytearray(b'\x01\x02\x03\x04'):
                        #  Display some basic information about the card
                        # print("Found an ISO14443A card")
                        # print("UID Length: {:d}".format(len(uid)))
                        uid_hex = binascii.hexlify(uid)
                        self.logger.log("Read UID value: {}".format(uid_hex), self.logger.INFO)
                        call_function_non_blocking(self.peripheral_handler.card_scanned)
                        self.device_handler.add_device_by_nfc_id(nfc_id=uid_hex)
                        while success:
                            success, uid = self.nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS, timeout=50)
            else:
                pass
                # print("Didn't find anything!")

    def setupNFC(self):
        self.nfc.begin()

        versiondata = self.nfc.getFirmwareVersion()
        if not versiondata:
            self.logger.log("Didn't find PN53x board", self.logger.DEBUG)
            raise RuntimeError("Didn't find PN53x board")  # halt

        # Got ok data, print it out!
        self.logger.log("Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format((versiondata >> 24) & 0xFF,
                                                                              (versiondata >> 16) & 0xFF,
                                                                              (versiondata >> 8) & 0xFF),
                        self.logger.INFO)

        # configure board to read RFID tags
        self.nfc.SAMConfig()

    def start_listening(self):
        call_function_non_blocking(self.loop)
