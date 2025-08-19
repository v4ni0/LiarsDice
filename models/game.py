from models.exceptions.empty_name_error import EmptyNameError
from models.human import Human
from models.bot import Bot
from models.exceptions.invalid_number_of_players_error import InvalidNumberOfPlayersError


class Game:
    BOT_NAMES = ["Ivan", "Georgi", "Petar", "Stefan"]
    MIN_PLAYERS: int = 2
    MAX_PLAYERS: int = 6

    def __init__(self, num_players: int = 2, is_wild: bool = False):
        if num_players < self.MIN_PLAYERS or num_players > self.MAX_PLAYERS:
            raise InvalidNumberOfPlayersError("Number of players must be between 2 and 6.")
        self.is_wild = is_wild
        self.number_of_players = num_players
        self.current_bet = (0, 1)  # (quantity, face_value)
        self.players = []
        self.current_player_index = 0
        self.round_number = 0
        self.total_dice = self.number_of_players * 5
        self.values_on_table = {i: 0 for i in range(1, 7)}
        self.is_human_eliminated = False

    def count_faces(self) -> None:
        """stores the number of faces on the table(including wilds)"""
        self._reset_values_on_table()
        for player in self.players:
            for face_value, quantity in player.get_values().items():
                self.values_on_table[face_value] += quantity

    def _reset_values_on_table(self) -> None:
        for i in range(1, 7):
            self.values_on_table[i] = 0

    def initialize_bots(self) -> None:
        for i in range(self.number_of_players - 1):
            bot_name = "Bot " + self.BOT_NAMES[i % len(self.BOT_NAMES)]
            self.players.append(Bot(bot_name, self.is_wild))

    def check_winner(self) -> bool:
        """Checks if there is a winner (only one player left)"""
        return self.number_of_players == 1

    def initialize_player(self, name: str) -> None:
        """Initializes player with name"""
        if not name.strip():
            raise EmptyNameError("Human name cannot be empty.")
        self.players.append(Human(f"{name}(You*)", self.is_wild))

    def set_number_of_players(self, number_of_players: str) -> None:
        """Sets the number of players and initializes bots if necessary"""
        num_players = int(number_of_players)
        if num_players < self.MIN_PLAYERS or num_players > self.MAX_PLAYERS:
            raise InvalidNumberOfPlayersError(
                f"Number of players must be between {self.MIN_PLAYERS} and {self.MAX_PLAYERS}.")
        self.number_of_players = num_players
        self.total_dice = num_players * 5

    def is_first_bet(self) -> bool:
        """Checks if the current bet is the first bet of the round"""
        return self.current_bet == (0, 1)

    def start_round(self) -> None:
        """Starts a new round, rolls the dice for each player, and resets the current bet"""
        for player in self.players:
            player.roll_dice()
        self.count_faces()
        self.current_bet = (0, 1)

    def is_human_player_turn(self) -> bool:
        return not self.is_human_eliminated and self.current_player_index == 0

    def spectate_game(self) -> None:
        """Removes the human player from the game and lets them spectate the left bots"""
        for _ in range(self.players[0].get_number_of_dice()):
            self.players[0].lose_die()
            self.total_dice -= 1
        self.players.pop(0)
        self.number_of_players -= 1
        self.is_human_eliminated = True
