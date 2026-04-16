# entities/device.py
from core.node import Node
from settings import COLOR_DEVICE

class Device(Node):
    def __init__(self, node_id, label, x, y, device_type=None):
        icon_path = "assets/icons/device.png"
        super().__init__(node_id, "Device", label, x, y, COLOR_DEVICE, icon_path)
        self.device_type = device_type  # Computer, Phone, Server, Tablet, etc.
        self.properties = {
            "name": label,
            "device_type": device_type,
            "manufacturer": None,
            "model": None,
            "associated_with": []  # List of person/organization IDs
        }
    
    def to_dict(self):
        data = super().to_dict()
        data["device_type"] = self.device_type
        data["properties"] = self.properties
        return data