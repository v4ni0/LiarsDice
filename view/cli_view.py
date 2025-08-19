import time
from view.view_interface import ViewInterface


class CLI(ViewInterface):
    """Command Line Interface implementation for Liar's Dice game."""

    # === Helper methods for formatting ===
    @staticmethod
    def _print_banner(message: str, char: str = "+", pad: int = 6):
        """Prints a banner with surrounding symbols for emphasis."""
        print(f"{char * pad}{message}{char * pad}\n")

    # === Input methods ===
    def enter_bet_choice(self):
        print()
        print("Choose an option:")
        print("1. Place a bet")
        print("2. Challenge the current bet (if not the first bet of the round)")
        print("3. Exit")
        print("4. Leave the game and spectate")
        return input("Enter your choice: ")

    def enter_player_name(self) -> str:
        return input("Enter your name: ").strip()

    def enter_number_of_players(self, min_players=2, max_players=6) -> str:
        return input(f"Enter the number of players ({min_players}-{max_players}): ")

    def enter_bet(self):
        quantity = input("Enter the quantity of dice: ")
        face_value = input("Enter the face value of the dice (1-6): ")
        return quantity, face_value

    # === Display methods ===
    @staticmethod
    def display_dice_on_table(names: list[str], dice: list[str], values: dict[int, int]):
        print("Revealing dice on the table:")
        for name, hand in zip(names, dice):
            print(f"{name}: {' '.join(hand)}")
        print("Face values on the table:")
        for face_value, count in values.items():
            print(f"{face_value}: {count}")
        print()

    def show_error(self, message):
        """Prints an error message consistently."""
        print(f"⚠️  Error: {message}")

    def display_bot_thinking(self, bot_name, max_dots=6, delay=1):
        print()
        print(f"{bot_name} is thinking", end='', flush=True)
        for i in range(1, max_dots + 1):
            print(f"\r{bot_name} is thinking{'.' * i}", end='', flush=True)
            time.sleep(delay)
        print()

    def display_winner(self, name: str):
        self._print_banner(f"{name} wins!", "+")

    def display_new_bet(self, new_bet: tuple, name: str):
        print(f"{name} placed new bet: {new_bet[0]} of {new_bet[1]}\n")

    def display_turn_info(self, name, current_bet, total_dice):
        self._print_banner("New turn")
        print(f"Current player: {name}")
        print(f"Current bet: {current_bet[0]} of {current_bet[1]}")
        print(f"Total dice in play: {total_dice}")
        print()

    def display_new_round(self, round_number):
        self._print_banner(f"Round {round_number}")

    def display_challenge(self, challenger: str, challenged: str, success: bool, names: list[str], dice: list[str],
                          values: dict[int, int]):
        print(f"Player {challenger} makes a challenge.")
        self.display_dice_on_table(names, dice, values)
        if success:
            print(f"✅ Successful challenge! {challenger} wins and {challenged} loses a die.\n")
        else:
            print(f"❌ Unsuccessful challenge! {challenger} loses a die.\n")

    def display_welcome_message(self):
        self._print_banner("Welcome to the Liar's Dice game!", "+")

    def display_player_eliminated(self, name):
        print(f"☠️  Player {name} is eliminated.")

    def display_player_dice(self, dice: list[str]):
        """Displays the dice of the player."""
        print("Your dice: " + " ".join(dice) + "\n")
