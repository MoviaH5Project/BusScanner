from datetime import datetime


class Device:
    def __init__(self, mac_address=None, last_seen_timestamp=None):
        self.mac_address = mac_address
        self.last_seen_timestamp: datetime = last_seen_timestamp

    def device_string(self):
        return self.mac_address
