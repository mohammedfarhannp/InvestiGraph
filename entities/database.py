# entities/database.py
from core.node import Node
from settings import COLOR_DATABASE

class Database(Node):
    def __init__(self, node_id, label, x, y):
        icon_path = "assets/icons/Database.png"
        super().__init__(node_id, "Database", label, x, y, COLOR_DATABASE, icon_path)
        self.properties = {
            "name": label,
            "type": None,  # MySQL, PostgreSQL, etc.
            "host": None,
            "associated_data": []  # List of document IDs
        }
    
    def to_dict(self):
        data = super().to_dict()
        data["properties"] = self.properties
        return data