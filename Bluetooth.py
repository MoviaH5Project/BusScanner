from bluepy import btle

from CallFunctionNonBlocking import call_function_non_blocking
from Devices.DeviceHandler import DeviceHandler
from LoggerInterface import LoggerInterface


class ScanHandler(btle.DefaultDelegate):

    def __init__(self, device_handler: DeviceHandler, logger: LoggerInterface, sensitivity=-128):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.sensitivity = sensitivity
        self.device_handler = device_handler

    def log_device_discovered(self, dev, is_new_dev, is_new_data, scan_data):
        if is_new_dev:
            status = "new"
        elif is_new_data:
            status = "update"
        else:
            status = "old"

        self.logger.log(
            f'Device ({status}): {dev.addr} ({dev.addrType}), {dev.rssi} dBm {"" if dev.connectable else "(not connectable)"}',
            level=self.logger.DEBUG)
        for (sdid, desc, val) in scan_data:
            if sdid in [8, 9]:
                self.logger.log(desc + ': \'' + val + '\'', self.logger.DEBUG)
            else:
                self.logger.log(desc + ': <' + val + '>', self.logger.DEBUG)
        if not dev.scanData:
            self.logger.log('\t(no data)', self.logger.DEBUG)

    def handleDiscovery(self, dev, is_new_dev, is_new_data):
        if dev.rssi < self.sensitivity:
            return
        scan_data = dev.getScanData()
        self.log_device_discovered(dev, is_new_dev, is_new_data, scan_data)

        device = None
        device = self.device_handler.find_device_by_mac(dev.addr)
        if device:
            self.device_handler.update_device_last_seen_time(device)
        elif dev.scanData:
            self.logger.log(f'Found device with scan data: {scan_data}', level=self.logger.DEBUG)
            for (sdid, desc, val) in scan_data:
                device = self.device_handler.find_device_by_advertisement_id(val)
                if device:
                    self.device_handler.update_device_last_seen_time(device)


class BluetoothHandler:
    def __init__(self, device_handler: DeviceHandler, logger: LoggerInterface):
        btle.Debugging = False
        self.logger = logger
        self.scanner = btle.Scanner(0).withDelegate(ScanHandler(device_handler=device_handler, logger=logger))

    def start_scanning(self):
        self.logger.log("Started scanning for Bluetooth devices", self.logger.INFO)
        call_function_non_blocking(self.scanner.scan, 0)

    def stop_scanning(self):
        self.logger.log("Stopped scanning for Bluetooth devices", self.logger.INFO)
        self.scanner.stop()
