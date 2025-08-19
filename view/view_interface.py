from abc import ABC, abstractmethod


class ViewInterface(ABC):
    """
    Abstract base class for view interfaces.
    Defines the methods that any view must implement.
    """

    @abstractmethod
    def enter_bet_choice(self):
        pass

    @abstractmethod
    def enter_player_name(self):
        pass

    @abstractmethod
    def enter_bet(self):
        pass

    @abstractmethod
    def enter_number_of_players(self, min_players=2, max_players=6) -> str:
        pass

    @abstractmethod
    def show_error(self, message):
        pass

    @abstractmethod
    def display_player_eliminated(self, name):
        pass

    @abstractmethod
    def display_challenge(self, challenger: str, loser: str, challenged: bool, names: list[str], dice: list[str], values: dict[int, int]):
        pass


    @abstractmethod
    def display_new_round(self, round_number):
        pass

    @abstractmethod
    def display_welcome_message(self):
        pass

    @abstractmethod
    def display_turn_info(self, name, current_bet, total_dice):
        pass

    @abstractmethod
    def display_winner(self, name: str):
        pass

    @abstractmethod
    def display_bot_thinking(self, bot_name, max_dots=3, delay=0.5):
        pass

    @abstractmethod
    def display_new_bet(self, new_bet: tuple, name: str):
        pass

    @abstractmethod
    def display_player_dice(self, dice: list[str]):
        pass

