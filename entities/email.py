# entities/email.py
from core.node import Node
from settings import COLOR_EMAIL, EMAIL_ICON

class Email(Node):
    def __init__(self, node_id, label, x, y):
        icon_path = EMAIL_ICON
        super().__init__(node_id, "Email", label, x, y, COLOR_EMAIL, icon_path)
        self.properties = {
            "address": label,
            "associated_with": []  # List of person/organization IDs
        }
    
    def to_dict(self):
        data = super().to_dict()
        data["properties"] = self.properties
        return data