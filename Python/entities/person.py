# entities/person.py
from core.node import Node
from settings import COLOR_PERSON_MALE, COLOR_PERSON_FEMALE, PERSON_MALE_ICON, PERSON_FEMALE_ICON

class Person(Node):
    def __init__(self, node_id, label, x, y, gender="male"):
        color, icon_path = (COLOR_PERSON_MALE, PERSON_MALE_ICON) if gender == "male" else (COLOR_PERSON_FEMALE, PERSON_FEMALE_ICON)        
        self.gender = gender
        
        super().__init__(node_id, "Person", label, x, y, color, icon_path)
        self.properties = {
            "name": label,
            "gender": gender,
            "email": None,
            "phone": None
        }
    
    def to_dict(self):
        data = super().to_dict()
        data["gender"] = self.gender
        data["properties"] = self.properties
        return data