from Devices.Device import Device


class CardFobCombo(Device):
    def __init__(self, mac_address, card_id=None):
        super().__init__(mac_address=mac_address)
        self.card_id = card_id
