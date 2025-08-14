# LiarsDice
Implementation of the Liar`s Dice game in Python
## Rules
-Each player has five standard 6-sided dice.The game is played over multiple rounds.

-To begin each round, all players roll their dice simultaneously. Each player looks at their own dice after they roll, keeping them hidden from the other players. 

-1 is wild, which means it counts as any dice face. E.g., if you have three 1s and two 5s, you can say you have five 5s.

-Every player then states a bid consisting of a face ("1's", "5's", etc.) and a quantity. The quantity represents the player's guess as to how many of each face have been rolled by all the players at the table, including themselves.

-The first bet is 0 dices of 1 .(because it has 100% probability)

-The player who is on turn has 2 options: raise the bet, or challenge the previous one. Raising the bid means that the player may bid a higher quantity of any face value, or the same quantity of a higher face. If the current player challenges the previous bid, all dice are revealed. If the bid is valid (there are at least as many of the face value as were bid), the bidder wins. Otherwise, the challenger wins. The player who loses a round loses one of their dice. The last player to still retain a die is the winner. The loser of the last round starts the bidding on the next round. If the loser of the last round was eliminated, the next player starts the new round.

### IDE:PyCharm
### Version:Python 3.13.2
