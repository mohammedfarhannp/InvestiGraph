# entities/organization.py
from core.node import Node
from settings import COLOR_ORGANIZATION, ORGANIZATION_ICON

class Organization(Node):
    def __init__(self, node_id, label, x, y):
        icon_path = ORGANIZATION_ICON
        super().__init__(node_id, "Organization", label, x, y, COLOR_ORGANIZATION, icon_path)
        self.properties = {
            "name": label,
            "website": None,
            "email": None,
            "phone": None,
            "employees": []  # List of person IDs
        }
    
    def to_dict(self):
        data = super().to_dict()
        data["properties"] = self.properties
        return data