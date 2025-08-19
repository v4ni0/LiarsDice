from models.exceptions.invalid_bet_error import InvalidBetError
from models.player import Player


class Human(Player):

    def __init__(self, name: str, is_wild: bool = False):
        super().__init__(name, is_wild)

    def validate_bet(self, quantity: int, face_value: int, prev_bet: tuple) -> None:
        """Raise error if bet is invalid."""
        if quantity <= 0:
            raise InvalidBetError("Quantity must be positive.")

        if face_value not in range(1, 7):
            raise InvalidBetError("Face value must be between 1 and 6.")

        if not self._is_valid_bet(quantity, face_value, prev_bet):
            raise InvalidBetError(
                "New bet must have higher quantity or same quantity with higher face value."
            )
