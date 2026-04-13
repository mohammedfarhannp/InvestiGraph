# entities/person.py
from core.node import Node
from settings import COLOR_PERSON_MALE, COLOR_PERSON_FEMALE

class Person(Node):
    def __init__(self, node_id, label, x, y, gender="male"):
        color = COLOR_PERSON_MALE if gender == "male" else COLOR_PERSON_FEMALE
        super().__init__(node_id, "Person", label, x, y, color)
        self.gender = gender
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