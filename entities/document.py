# entities/document.py
from core.node import Node
from settings import COLOR_DOCUMENT

class Document(Node):
    def __init__(self, node_id, label, x, y):
        icon_path = "assets/icons/document.png"
        super().__init__(node_id, "Document", label, x, y, COLOR_DOCUMENT, icon_path)
        self.properties = {
            "title": label,
            "content": None,
            "file_path": None,
            "associated_with": []  # List of person/organization IDs
        }
    
    def to_dict(self):
        data = super().to_dict()
        data["properties"] = self.properties
        return data