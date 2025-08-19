from models.exceptions.empty_name_error import EmptyNameError
from models.exceptions.invalid_bet_error import InvalidBetError
from models.exceptions.invalid_command_error import InvalidCommandError
from models.exceptions.invalid_number_of_players_error import InvalidNumberOfPlayersError
from models.game import Game
from view.view_interface import ViewInterface


class GameController:
    def __init__(self, view: ViewInterface, wild_mode=False):
        self.view = view
        self.game = Game(2, wild_mode)

    def _set_up(self) -> None:
        """Sets up the game by initializing players and starting the first round"""
        while True:
            try:
                number_of_players = self.view.enter_number_of_players()
                self.game.set_number_of_players(number_of_players)
                break
            except (InvalidNumberOfPlayersError, ValueError) as e:
                self.view.show_error(str(e))
        while True:
            try:
                player_name = self.view.enter_player_name()
                self.game.initialize_player(player_name)
                break
            except EmptyNameError as e:
                self.view.show_error(str(e))
        self.game.initialize_bots()

    def _check_player_elimination(self, player_index: int) -> int:
        """Checks if the previous player is eliminated and returns the next player index"""
        if self.game.players[player_index].get_number_of_dice() == 0:
            if player_index == 0 and not self.game.is_human_eliminated:
                self.game.is_human_eliminated = True
            self.view.display_player_eliminated(self.game.players[player_index].name)
            self.game.number_of_players -= 1
            self.game.players.pop(player_index)
        return player_index % self.game.number_of_players

    def _challenge_bet(self) -> int:
        """Challenges the current bet by checking if the bet is valid
         returns the index of the loser if not eliminated, otherwise next player index"""
        quantity, face_value = self.game.current_bet
        actual_count = self.game.values_on_table[face_value]
        current_player_index = self.game.current_player_index
        previous_player_index = (current_player_index - 1 + self.game.number_of_players) % self.game.number_of_players
        challenger = self.game.players[current_player_index].name
        challenged = self.game.players[previous_player_index].name
        loser_index = previous_player_index
        if quantity > actual_count:
            success = True
        else:
            success = False
            loser_index = current_player_index
        self.game.total_dice -= 1
        dice = [player.dice_to_str() for player in self.game.players]
        names = [player.name for player in self.game.players]
        self.view.display_challenge(challenger, challenged, success, names, dice, self.game.values_on_table)
        self.game.players[loser_index].lose_die()
        next_player_index = self._check_player_elimination(loser_index)
        return next_player_index

    def get_valid_choice(self) -> str:
        """Gets a valid choice from the player"""
        choices = ['1', '3', '4'] if self.game.is_first_bet() else ['1', '2', '3', '4']
        while True:
            try:
                choice = self.view.enter_bet_choice()
                if choice not in choices:
                    raise InvalidCommandError("Invalid choice. Please enter new choice")
                break
            except InvalidCommandError as e:
                self.view.show_error(str(e))
        return choice

    def take_turn_human(self, choice: str) -> bool:
        """Handles the player's turn, allowing them to place a bet or challenge the current bet,
        returns true if a new round should start"""
        if choice == '1':
            while True:
                try:
                    new_bet = self.view.enter_bet()
                    self.game.players[0].validate_bet(int(new_bet[0]), int(new_bet[1]), self.game.current_bet)
                    break
                except InvalidBetError as e:
                    self.view.show_error(str(e))
            self.game.current_bet = int(new_bet[0]), int(new_bet[1])
            current_player_index = self.game.current_player_index
            self.view.display_new_bet(self.game.current_bet, self.game.players[current_player_index].name)
            self.game.current_player_index = (current_player_index + 1) % self.game.number_of_players
        elif choice == '2':
            self.game.current_player_index = self._challenge_bet()
            return True
        elif choice == '4':
            self.game.spectate_game()
            return True
        else:
            exit(0)
        return False

    def take_turn_bot(self) -> bool:
        current_player = self.game.players[self.game.current_player_index]
        self.view.display_bot_thinking(current_player.name)
        will_challenge = current_player.decide_to_challenge(self.game.current_bet, self.game.total_dice)
        if will_challenge and not self.game.is_first_bet():
            self.game.current_player_index = self._challenge_bet()
            return True
        else:
            self.game.current_bet = current_player.place_bet(self.game.current_bet, self.game.total_dice)
            self.view.display_new_bet(self.game.current_bet, current_player.name)
            self.game.current_player_index = (self.game.current_player_index + 1) % self.game.number_of_players
        return False

    def take_turn(self) -> bool:
        """Manages the turn of the current player, allowing them to place a bet or challenge the current bet,
                returns true if a new round should start"""
        self.view.display_turn_info(self.game.players[self.game.current_player_index].name,
                                    self.game.current_bet, self.game.total_dice)
        if self.game.is_human_player_turn():
            self.view.display_player_dice(self.game.players[0].dice_to_str())
            while True:
                try:
                    choice = self.get_valid_choice()
                    break
                except InvalidCommandError as e:
                    self.view.show_error(str(e))
            if self.take_turn_human(choice):
                return True
        else:
            if self.take_turn_bot():
                return True
        return False

    def play_game(self):
        """Starts the game loop, initializes players, and manages the game rounds"""
        self.view.display_welcome_message()
        self._set_up()
        while not self.game.check_winner():
            self.game.round_number += 1
            self.view.display_new_round(self.game.round_number)
            self.game.start_round()
            while True:
                if self.take_turn():
                    break
        self.view.display_winner(self.game.players[0].name)
