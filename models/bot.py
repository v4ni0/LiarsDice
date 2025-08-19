import math
from models.player import Player


class Bot(Player):
    def __init__(self, name: str, is_wild = False):
        super().__init__(name, is_wild)

    @staticmethod
    def binomial_probability(k: int, n: int, p: float) -> int:
        """Calculates probability of having at least k successful attempts out of n attempts using binomial distribution"""
        if k < 0 or n <= 0:
            return 0
        result = 0
        for i in range(k, n + 1):
            result += math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
        return result

    def _find_most_frequent_face(self) -> int:
        """Returns the most frequent face value among the bot's dice"""
        most_frequent_face = 1
        for face in range(2, 7):
            if self._face_values[face] >= self._face_values[most_frequent_face]:
                most_frequent_face = face
        return most_frequent_face

    def decide_to_challenge(self, current_bet: tuple, total_dice: int) -> bool:
        """Decides whether to challenge the current bet based on number of players and current bet"""
        quantity, face_value = current_bet
        remaining_quantity = quantity - self._face_values[face_value]
        remaining_dice = total_dice - self.get_number_of_dice()
        if remaining_quantity <= 0:
            return False
        if remaining_quantity > remaining_dice:
            return True
        p = 1 / 6
        if self.is_wild and face_value != 1:
            p = 1 / 3
        probability = self.binomial_probability(remaining_quantity, remaining_dice ,p)
        if probability >= 0.3:
            return False
        return True

    def _get_start_bet(self, current_bet: tuple, total_dice: int, lower: float, p: float) -> tuple:
        """Returns the minimum valid bet including the most frequent face value, if it is likely enough
        else returns the most likely minimum bet, based on the current bet"""
        quantity, face_value = current_bet
        best_face = self._find_most_frequent_face()
        best_count = self._face_values[best_face]
        next_quantity = quantity + 1 if (best_face <= face_value or quantity==0) else quantity
        next_face_value = best_face
        current_probability = 1
        if next_quantity > best_count:
            current_probability = (
                self.binomial_probability(next_quantity - best_count, total_dice - self.get_number_of_dice(), p))
        if current_probability < lower:
            for face in range(6, face_value, -1):
                temp_probability = self.binomial_probability(quantity - self._face_values[face],
                                                             total_dice - self.get_number_of_dice(), p)
                if temp_probability > current_probability:
                    current_probability = temp_probability
                    next_quantity = quantity
                    next_face_value = face
        return next_quantity, next_face_value

    def place_bet(self, current_bet: tuple, total_dice: int) -> tuple:
        """Places a bet based on the current bet and own dice if it decides not to challenge"""
        p = 1 / 6
        if self.is_wild:
            p = 1 / 3
        lower_probability = 1 / 2
        next_quantity, next_face_value = self._get_start_bet(current_bet, total_dice, lower_probability, p)
        most_frequent_face = self._find_most_frequent_face()
        if next_face_value != most_frequent_face:
            return next_quantity, next_face_value
            # every bet with higher quantity will have too low probability
        best_count = self._face_values[most_frequent_face]
        for _ in range(3):
            # Try to increase the quantity up to 3 times and check if the probability is still acceptable
            temp_probability = 1
            if next_quantity + 1 > best_count:
                temp_probability = self.binomial_probability(next_quantity + 1 - best_count,
                                                             total_dice - self.get_number_of_dice(), p)
            if lower_probability <= temp_probability:
                next_quantity += 1
            else:
                return next_quantity, next_face_value

        return next_quantity, next_face_value
