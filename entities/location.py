# entities/location.py
from core.node import Node
from settings import COLOR_LOCATION

class Location(Node):
    def __init__(self, node_id, label, x, y):
        icon_path = "assets/icons/Location.png"
        super().__init__(node_id, "Location", label, x, y, COLOR_LOCATION, icon_path)
        self.properties = {
            "name": label,
            "address": None,
            "city": None,
            "country": None,
            "coordinates": None,
            "associated_with": []  # List of person/organization IDs
        }
    
    def to_dict(self):
        data = super().to_dict()
        data["properties"] = self.properties
        return data