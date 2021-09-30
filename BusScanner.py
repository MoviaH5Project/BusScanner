from Bluetooth import BluetoothHandler
from Devices.CardFobCombo import CardFobCombo
from Devices.DeviceHandler import DeviceHandler
from Devices.Phone import Phone
from GRPCCaller import GRPCCaller
from NFC import NFC
from Peripherals.PeripheralHandler import PeripheralHandler
from LoggerInterface import LoggerInterface
from MyLogger import MyLogger


def main():
    logger: LoggerInterface = MyLogger()
    peripheral_handler = PeripheralHandler()
    grpc_caller = GRPCCaller(logger=logger)
    device_handler = DeviceHandler(logger=logger, grpc_caller=grpc_caller, peripheral_handler=peripheral_handler)
    nfc = NFC(peripheral_handler, logger=logger, device_handler=device_handler)
    bluetooth_handler = BluetoothHandler(device_handler=device_handler, logger=logger)

    bluetooth_handler.start_scanning()
    nfc.start_listening()
    device_handler.start_checking_timestamps()

    # TODO Get this data from NFC scan and server lookup
    #device_handler.add_device(Phone(advertisement='a596c37f9ee8de908d4f163dd2ece0ff74657374'))
    #device_handler.add_device(CardFobCombo(card_id='3921c16e', mac_address='ff:ff:70:09:20:34'))


if __name__ == '__main__':
    main()
