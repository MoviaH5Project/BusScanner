import time
from typing import List
from datetime import datetime, timedelta

from Peripherals.PeripheralHandler import PeripheralHandler
from CallFunctionNonBlocking import call_function_non_blocking
from Devices.CardFobCombo import CardFobCombo
from Devices.Device import Device
from Devices.Phone import Phone
from GRPCCaller import GRPCCaller
from LoggerInterface import LoggerInterface


class DeviceHandler:
    def __init__(self, logger: LoggerInterface, grpc_caller: GRPCCaller, peripheral_handler: PeripheralHandler):
        self.devices: List[Device] = []
        self.logger = logger
        self.consider_seen = 15  # Time to consider a device seen, before considering it as left (in seconds)
        self.check_interval = 1
        self.grpc_caller = grpc_caller
        self.peripheral_handler = peripheral_handler

    def add_device(self, device: Device):
        self.devices.append(device)
        # TODO Call API

    def add_device_by_nfc_id(self, nfc_id):
        #  self.add_device(device=CardFobCombo())
        if self.grpc_caller.check_in().succeeded:
            self.peripheral_handler.success()
        else:
            self.peripheral_handler.fail()
        self.logger.log(f'Check in: {self.grpc_caller.check_in().succeeded}', self.logger.INFO)

    def update_device_last_seen_time(self, device):
        device.last_seen_timestamp = datetime.now()
        self.logger.log(f'Updating last seen time for device: {device.device_string()}', level=self.logger.INFO)

    def find_device_by_mac(self, mac_address: str):
        if self.devices and len(self.devices) > 0:
            for device in self.devices:
                if device.mac_address == mac_address:
                    return device
        return False

    def find_device_by_advertisement_id(self, advertisement_id: str):
        if self.devices and len(self.devices) > 0:
            for device in self.devices:
                if type(device) == Phone:
                    if Phone(Device).advertisement_id == advertisement_id:
                        return Device
        return False

    def devices_check_if_last_seen_surpasses_threshold(self):
        while True:
            now_minus_consider_seen = datetime.now() - timedelta(seconds=self.consider_seen)
            for device in self.devices:
                if device.last_seen_timestamp:
                    if device.last_seen_timestamp < now_minus_consider_seen:
                        self.logger.log(f'Device last seen time surpasses threshold, device: {device.device_string()}',
                                        level=self.logger.INFO)
                        self.devices.remove(device)
                        self.grpc_caller.check_out(mac_address=device.mac_address)
            time.sleep(self.check_interval)

    def start_checking_timestamps(self):
        call_function_non_blocking(self.devices_check_if_last_seen_surpasses_threshold)
