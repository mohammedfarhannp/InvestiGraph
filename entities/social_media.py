# entities/social_media.py
from core.node import Node
from settings import COLOR_SOCIAL_MEDIA

class SocialMedia(Node):
    def __init__(self, node_id, label, x, y, platform=None):
        icon_path = "assets/icons/social_media.png"
        super().__init__(node_id, "SocialMedia", label, x, y, COLOR_SOCIAL_MEDIA, icon_path)
        self.platform = platform  # Twitter, Facebook, LinkedIn, etc.
        self.properties = {
            "username": label,
            "platform": platform,
            "url": None,
            "associated_with": []  # List of person/organization IDs
        }
    
    def to_dict(self):
        data = super().to_dict()
        data["platform"] = self.platform
        data["properties"] = self.properties
        return data