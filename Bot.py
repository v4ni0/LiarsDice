from Player import Player
import math


class Bot(Player):
    def __init__(self, name, dices=None):
        super().__init__(name)
        if dices is not None:
            self.set_dices(dices)

    # Calculates probability of having at least k successful attempts out of n attempts using binomial distribution
    @staticmethod
    def binomial_probability(k: int, n: int, p: float) -> int:
        result = 0
        for i in range(k, n + 1):
            result += math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
        return result

    # Decides whether to challenge the current bet based on number of players and current bet
    def decide_to_challenge(self, current_bet: tuple, total_dices: int) -> bool:
        quantity, face_value = current_bet
        p = 1 / 6
        if face_value != 1:
            p = 1 / 3

        own_dices_count = 0
        for die in self._dices:
            if die.face == face_value or die.face == 1:
                own_dices_count += 1
        if own_dices_count >= quantity:
            return False
        probability = self.binomial_probability(quantity - own_dices_count, total_dices - self.get_number_of_dices(), p)
        if probability >= 1/3:
            return False
        return True

    # Places a bet based on the current bet and own dices if it decides not to challenge
    def place_bet_bot(self, current_bet: tuple, total_dices: int) -> tuple:
        quantity, face_value = current_bet
        best_face = None
        best_count = 0

        counts = {i: 0 for i in range(1, 7)}
        for die in self._dices:
            counts[die.face] += 1

        # Finds the number of the most frequent face and its frequency
        # it will never be one because every other face value is >= number of ones
        for face in range(1, 7):
            if face == 1:
                if counts[1] > best_count:
                    best_face = 1
                    best_count = counts[1]
            else:
                total_count = counts[face] + counts[1]
                if total_count >= best_count:
                    best_face = face
                    best_count = total_count

        next_quantity = quantity + 1 if best_face <= face_value else quantity
        next_face_value = best_face
        lower_probability = 1 / 2

        current_probability = 1
        if next_quantity > best_count:
            current_probability = (
                self.binomial_probability(next_quantity - best_count, total_dices - self.get_number_of_dices(), 1 / 3))

        # if raising the quantity of current bet is not a good probability, check higher faces with lower quantity
        # we check the highest face first, and then lower faces
        if current_probability < lower_probability:
            temp_probability = 0
            for face in range(6, best_face, -1):
                temp_probability = self.binomial_probability(quantity - counts[face] - counts[1],
                                                             total_dices - self.get_number_of_dices(), 1 / 3)
                if temp_probability > current_probability:
                    current_probability = temp_probability
                    next_quantity = quantity
                    next_face_value = face

            return next_quantity, next_face_value

        # best_face contains the face with the highest probability of winning with the highest face value
        # the new bet with the highest quantity will contain the best_face value as face value of the dice
        # will increase the quantity by at most 3 from the current bet
        for _ in range(3):
            temp_probability = 1
            if next_quantity + 1 > best_count:
                temp_probability = self.binomial_probability(next_quantity + 1 - best_count,
                                                             total_dices - self.get_number_of_dices(), 1 / 3)

            if lower_probability <= temp_probability:
                next_quantity += 1
            else:
                return next_quantity, next_face_value

        return next_quantity, next_face_value
