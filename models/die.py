import random
from models.exceptions.invalid_die_value_error import InvalidDieValueError


class Die:
    SIDES = 6

    def __init__(self, face=1):
        self.face = None
        self.set_face(face)

    def roll(self):
        self.face = random.randint(1, self.SIDES)
        return self.face

    def to_int(self) -> int:
        return self.face

    def set_face(self, face: int):
        if face < 1 or face > 6:
            raise InvalidDieValueError("Invalid dice value, must be between 1 and 6.")
        self.face = face

    def __str__(self):
        match self.face:
            case 1:
                return "⚀"
            case 2:
                return "⚁"
            case 3:
                return "⚂"
            case 4:
                return "⚃"
            case 5:
                return "⚄"
            case 6:
                return "⚅"
        return None