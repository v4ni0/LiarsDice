from Player import Player
from Bot import Bot
import time
from exceptions.InvalidCommandError import InvalidCommandError
from exceptions.InvalidBetError import InvalidBetError


class Game:
    bot_names = ["Ivan", "Georgi", "Petar", "Stefan"]

    def __init__(self, num_players: int = 2):
        self.number_of_players = num_players
        self.current_bet = (0, 1)  # (quantity, face_value)
        self.players = []
        self.current_player_index = 0
        self.round_number = 0
        self.total_dices = self.number_of_players * 5
        self.values_on_table = {i: 0 for i in range(1, 7)}

    # stores the number of faces on the table(including wilds)
    def _count_faces(self):
        self._reset_values_on_table()
        for player in self.players:
            for die in player.get_values():
                self.values_on_table[die] += 1
        for i in range(2, 7):
            self.values_on_table[i] += self.values_on_table[1]

    def _reset_values_on_table(self):
        for i in range(1, 7):
            self.values_on_table[i] = 0

    def initialize_players(self):

        own_name = input("Enter your name: ")
        self.current_player_index = 0
        self.players.append(Player(f"{own_name}(You*)"))

        # Bots
        for i in range(self.number_of_players - 1):
            bot_name = self.bot_names[i % len(self.bot_names)]
            self.players.append(Bot(bot_name))

    # Starts a new round, rolls the dice for each player, and resets the current bet
    def start_round(self):

        print(f"\n--- Round {self.round_number} ---")

        for player in self.players:
            player.roll_dices()

        self._count_faces()

        self.current_bet = (0, 1)



    # Challenges the current bet by checking if the bet is valid
    # returns the index of the loser if not eliminated, otherwise next player index
    def challenge_bet(self) -> int:
        next_player_index = None
        quantity, face_value = self.current_bet
        actual_count = self.values_on_table[face_value]
        eliminated_player = None
        if quantity > actual_count:

            previous_player_index = (self.current_player_index - 1 + self.number_of_players) % self.number_of_players
            print(
                f"Successful challenge! The bet was too high. Player {self.players[previous_player_index].name} loses a die.")
            self.players[previous_player_index].lose_die()

            if self.players[previous_player_index].get_number_of_dices() == 0:
                print(f"Player {self.players[previous_player_index].name} is eliminated.")
                eliminated_player = self.players.pop(previous_player_index)
                self.number_of_players -= 1
            next_player_index = previous_player_index % self.number_of_players

        else:
            print(f"Unsuccessful challenge. Player {self.players[self.current_player_index].name} loses a die.")
            self.players[self.current_player_index].lose_die()
            if self.players[self.current_player_index].get_number_of_dices() == 0:
                print(f"Player {self.players[self.current_player_index].name} is eliminated.")
                eliminated_player = self.players.pop(self.current_player_index)
                self.number_of_players -= 1
            next_player_index = self.current_player_index % self.number_of_players

        self.total_dices -= 1
        if eliminated_player:
            for face_value in eliminated_player.get_values():
                if face_value == 1:
                    for i in range(1, 7):
                        self.values_on_table[i] -= 1
                else:
                    self.values_on_table[face_value] -= 1
        return next_player_index


    # Checks if there is a winner (only one player left)
    # In this case, the game ends
    def check_winner(self) -> bool:

        if self.number_of_players == 1:
            return True

        return False

    def print_active_players(self):
        for player in self.players:
            print(f"Player: {player.name}")

    # Inputs the bet choice from the user
    # Validates the input and returns the choice
    @staticmethod
    def input_bet_choice() -> str:
        print("Choose an option:")
        print("1. Place a bet")
        print("2. Challenge the current bet")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice not in ['1', '2', '3']:
            raise InvalidCommandError("Invalid choice, please enter 1, 2 or 3.")
        if choice == '3':
            print("Exiting the game.")
            exit(0)
        return choice

    # Starts the game loop
    def play_game(self):

        self.initialize_players()
        is_eliminated = False

        while not self.check_winner():
            self.round_number += 1
            self.start_round()

            while True:

                print(f"\nCurrent player: {self.players[self.current_player_index].name}")
                print(f"Current bet: {self.current_bet[0]} dice of value {self.current_bet[1]}")
                print(f"Total dices on the table: {self.total_dices}")
                if (self.current_player_index == 0) and (not is_eliminated):
                    print("Your turn to place a bet.")
                    print("Your dices: ")
                    self.players[0].print_dices()
                    print("Type 1 to place a new bet, or 2 to challenge the current bet.")
                    while True:
                        try:
                            choice = self.input_bet_choice()
                            break
                        except InvalidCommandError as e:
                            print(e)
                            print("Please try again and enter 1, 2 or 3.")
                    if choice == '1':
                        while True:
                            try:
                                new_bet = self.players[0].place_bet(self.current_bet)
                                break
                            except InvalidBetError as e:
                                print(e)
                                print("Please try again with a valid bet.")
                        self.current_bet = new_bet
                        self.current_player_index = (self.current_player_index + 1) % self.number_of_players

                    elif choice == '2':
                        print("You decided to challenge the current bet.")
                        self.current_player_index = self.challenge_bet()
                        if isinstance(self.players[0],Bot):
                            print("You are eliminated from the game.")
                            is_eliminated = True
                        break


                else:
                    print(f"\nBot {self.players[self.current_player_index].name} is thinking.\n")
                    time.sleep(3)
                    will_challenge = self.players[self.current_player_index].decide_to_challenge(self.current_bet,
                                                                                                 self.total_dices)
                    if will_challenge:
                        print(f"Bot {self.players[self.current_player_index].name} challenges the bet.")
                        self.current_player_index = self.challenge_bet()
                        if not is_eliminated and isinstance(Bot):
                            print("You are eliminated from the game.")
                            is_eliminated = True
                        break
                    else:
                        print(f"Bot {self.players[self.current_player_index].name} places a new bet.")
                        self.current_bet = self.players[self.current_player_index].place_bet_bot(self.current_bet,
                                                                                                 self.total_dices)
                        print(f"New bet: {self.current_bet[0]} dice of value {self.current_bet[1]}")
                        self.current_player_index = (self.current_player_index + 1) % self.number_of_players

        print(f"Player {self.players[0].name} wins the game!")
