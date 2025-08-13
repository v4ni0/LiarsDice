import random

from exceptions.InvalidDiceValueError import InvalidDiceValueError


class Dice:

    def __init__(self, face=1):
        self.sides = 6
        if face < 1 or face > 6:
            raise InvalidDiceValueError("Invalid dice value, must be between 1 and 6.")
        self.face = face

    def roll(self):
        self.face = random.randint(1, self.sides)
        return self.face
    
    def print(self):
        faces = [[
            "┌─────┐",
            "│     │",
            "│  *  │",
            "│     │",
            "└─────┘"],
            [
            "┌─────┐",
            "│ ●   │",
            "│     │",
            "│   ● │",
            "└─────┘"],
            [
            "┌─────┐",
            "│ ●   │",
            "│  ●  │",
            "│   ● │",
            "└─────┘"],
            [
            "┌─────┐",
            "│ ● ● │",
            "│     │",
            "│ ● ● │",
            "└─────┘"],
            [
            "┌─────┐",
            "│ ● ● │",
            "│  ●  │",
            "│ ● ● │",
            "└─────┘"],
            [
            "┌─────┐",
            "│ ● ● │",
            "│ ● ● │",
            "│ ● ● │",
            "└─────┘"]
        ]
        
        output = faces[self.face-1]
        
        print("\n".join(output))
        
    