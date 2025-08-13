import unittest

from Bot import Bot
from Dice import Dice


class TestBot(unittest.TestCase):
    def setUp(self):
        self.bot = Bot("TestBot", [Dice(1), Dice(2), Dice(1), Dice(2), Dice(5)])

    def test_initialization(self):
        self.assertIsInstance(self.bot, Bot)

    def test_get_name(self):
        self.assertEqual(self.bot.name, "TestBot")

    def test_binomial_probability(self):
        # Test with k=2, n=5, p=0.5
        result = self.bot.binomial_probability(7, 10, 1 / 2)

        # "Probability of at least 7 successes in 6 trials with p=0.5 is appr. 0.171875"
        self.assertAlmostEqual(result, 0.171875, 6)

        result = self.bot.binomial_probability(1, 5, 0.5)
        # "Probability of at least 1 success in 5 trials with p=0.5 is appr. 0.96875"
        self.assertAlmostEqual(result, 0.96875, 6)

    def test_decide_to_challenge(self):
        current_bet = (2, 3)
        total_dices = 10
        decision = self.bot.decide_to_challenge(current_bet, total_dices)

        # With 2 players and 2 dices of value 3, the bot should not challenge
        self.assertFalse(decision)

        current_bet = (5, 3)
        decision = self.bot.decide_to_challenge(current_bet, total_dices)
        # With 2 players and 2 dices of value 3(including wilds), the bot should challenge
        self.assertTrue(decision)

        current_bet = (2, 1)
        decision = self.bot.decide_to_challenge(current_bet, total_dices)
        # With 1 player and 2 dices of value 1, the bot should not challenge
        self.assertFalse(decision)

        number_of_players = 5
        current_bet = (10, 3)
        decision = self.bot.decide_to_challenge(current_bet, total_dices)
        # With 5 players and 2 dices of value 3(including wilds), the bot should challenge
        self.assertTrue(decision)

        current_bet = (7, 3)
        decision = self.bot.decide_to_challenge(current_bet, number_of_players)
        # With 5 players and 2 dices of value 3(including wilds), the bot should not challenge
        self.assertTrue(decision)

    def test_place_bet_bot(self):
        current_bet = (2, 3)
        total_dices = 10
        new_bet = self.bot.place_bet_bot(current_bet, total_dices)

        # With 2 players and 2 dices of value 3(including wilds), the bot should place a bet of (3, 3)
        self.assertEqual(new_bet, (6, 2))

        current_bet = (5, 3)
        new_bet = self.bot.place_bet_bot(current_bet, total_dices)
        # With 2 players and 2 dices of value 3(including wilds), the bot should place a bet of (6, 3)
        self.assertEqual(new_bet, (6, 2))

        # unlikely bet, new bet should be 8, 2 because it is equally probable as 7, 5  but with higher quantity
        current_bet = (7, 2)
        new_bet = self.bot.place_bet_bot(current_bet, total_dices)
        self.assertEqual(new_bet, (8, 2))

        current_bet = (5, 1)
        new_bet = self.bot.place_bet_bot(current_bet, total_dices)
        self.assertEqual(new_bet, (6, 2))

if __name__ == "__main__":
    unittest.main()
