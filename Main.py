

from Game import Game
from Bot import Bot



if __name__ == "__main__":

    number_of_players = int(input("Enter the number of players (2-5): "))
    if number_of_players < 2 or number_of_players > 5:
        print("Invalid number of players. The game will start with 3 players.")
        number_of_players = 5
    game = Game(number_of_players)
    game.play_game()
    #print(Bot.binomial_probability(2, 5, 1/3))


    
   