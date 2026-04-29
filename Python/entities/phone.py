# entities/phone.py
from core.node import Node
from settings import COLOR_PHONE, PHONE_ICON

class Phone(Node):
    def __init__(self, node_id, label, x, y):
        icon_path = PHONE_ICON
        super().__init__(node_id, "Phone", label, x, y, COLOR_PHONE, icon_path)
        self.properties = {
            "number": label,
            "associated_with": []  # List of person/organization IDs
        }
    
    def to_dict(self):
        data = super().to_dict()
        data["properties"] = self.properties
        return data