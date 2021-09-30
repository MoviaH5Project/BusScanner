from Devices.Device import Device


class Phone(Device):
    def __init__(self, mac_address=None, advertisement=None):
        super().__init__(mac_address=mac_address)
        self.advertisement_id = advertisement

    def device_string(self):
        return f'{self.mac_address} {self.advertisement_id}'
