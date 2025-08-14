from typing import List

from Dice import Dice

from exceptions.InvalidBetError import InvalidBetError


class Player:

    def __init__(self, name):
        self.name = name
        self._dices = [Dice() for _ in range(5)]
        for die in self._dices:
            die.roll()

    def get_number_of_dices(self) -> int:

        return len(self._dices)

    def roll_dices(self):
        for die in self._dices:
            die.roll()

    def _is_valid_bet(self, quantity: int, face_value: int, prev_bet: tuple) -> bool:
        prev_quantity, prev_face_value = prev_bet
        if quantity > prev_quantity or (quantity == prev_quantity and face_value > prev_face_value):
            return True
        return False

    def get_values(self) -> List[int]:

        return [die.face for die in self._dices]

    def set_dices(self, dices: List[Dice]):
        if len(dices) > 5:
            raise ValueError("Cannot set more than 5 dices.")
        self._dices = dices

    def place_bet(self, prev_bet: tuple) -> tuple:

        prev_quantity, prev_face_value = prev_bet
        print(f"Current bet: {prev_quantity} dice of value {prev_face_value}")
        quantity = int(input(f"{self.name}, enter quantity: "))
        face_value = int(input(f"{self.name}, enter face value (1-6): "))

        if quantity <= 0:
            raise InvalidBetError("Invalid bet, please enter a positive quantity.")

        if face_value < 1 or face_value > 6:
            raise InvalidBetError("Invalid bet, please enter a face value between 1 and 6.")

        if not self._is_valid_bet(quantity, face_value, prev_bet):
            raise InvalidBetError(
                "Invalid bet, new bet should have higher quantity or same quantity with higher face value.")

        return quantity, face_value

    def lose_die(self):
        if len(self._dices) > 0:
            self._dices.pop()

    def print_dices(self):
        for die in self._dices:
            die.print()
