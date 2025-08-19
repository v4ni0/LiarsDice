from abc import ABC, abstractmethod
from models.die import Die


class Player(ABC):
    def __init__(self, name: str, is_wild: bool = False):
        self.name = name
        self.is_wild = is_wild
        self._dice = [Die() for _ in range(5)]
        self._face_values = {i: 0 for i in range(1, 7)}
        self.roll_dice()

    @staticmethod
    def _is_valid_bet(quantity: int, face_value: int, prev_bet: tuple) -> bool:
        prev_quantity, prev_face_value = prev_bet
        if quantity > prev_quantity or (quantity == prev_quantity and face_value > prev_face_value):
            return True
        return False

    def _count_own_dice(self) -> None:
        """Counts the number of own dice with the given face value"""
        for i in range(1, 7):
            self._face_values[i] = 0
        for die in self._dice:
            self._face_values[die.face] += 1
        if self.is_wild:
            for i in range(2, 7):
                self._face_values[i] += self._face_values[1]

    def get_number_of_dice(self) -> int:
        return len(self._dice)

    def get_values(self) -> dict[int, int]:
        return self._face_values

    def roll_dice(self) -> None:
        for die in self._dice:
            die.roll()
            self._count_own_dice()

    def lose_die(self) -> None:
        if len(self._dice) > 0:
            self._dice.pop()

    def dice_to_str(self) -> list[str]:
        """Returns a list of dice."""
        return [str(die) for die in self._dice]
