from view.cli_view import CLI
from controller.game_controller import GameController


if __name__ == "__main__":
    view = CLI()
    controller = GameController(view, False)
    controller.play_game()


