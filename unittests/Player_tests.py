import unittest



from Player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestPlayer")
    
    def test_player_initialization(self):
        self.assertEqual(self.player.name, "TestPlayer")
        self.assertEqual(len(self.player.get_values()), 5)
    
    def test_is_valid_bet(self):

        prev_bet = (2, 3)  
        
        # Valid
        self.assertTrue(self.player._is_valid_bet(3, 3, prev_bet))
        self.assertTrue(self.player._is_valid_bet(2, 4, prev_bet))
        
        # Invalid
        self.assertFalse(self.player._is_valid_bet(1, 3, prev_bet))
        self.assertFalse(self.player._is_valid_bet(2, 2, prev_bet))
        self.assertFalse(self.player._is_valid_bet(1, 6, prev_bet))

    def test_get_number_of_dices(self):
        self.assertEqual(self.player.get_number_of_dices(), 5)

    def test_lose_die(self):
        initial_dice_count = self.player.get_number_of_dices()
        self.player.lose_die()
        self.assertEqual(self.player.get_number_of_dices(), initial_dice_count - 1)
        for _ in range(initial_dice_count):
            self.player.lose_die()
        self.assertEqual(self.player.get_number_of_dices(), 0)
        self.player.lose_die()
        self.assertEqual(self.player.get_number_of_dices(), 0)

if __name__ == "__main__":
    unittest.main()
        
