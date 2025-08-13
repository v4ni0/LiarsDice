# LiarsDice
Implementation of the Liar`s Dice game in Python
##Rules
Each player has five standard 6-sided dice.The game is played over multiple rounds.

To begin each round, all players roll their dice simultaneously. Each player looks at their own dice after they roll, keeping them hidden from the other players. (If any dice has landed on top of another, the player must roll all their dice again.)

1 is wild, which means it counts as any dice face. E.g., if you have three 1s and two 5s, you can say you have five 5s.

The first player then states a bid consisting of a face ("1's", "5's", etc.) and a quantity. The quantity represents the player's guess as to how many of each face have been rolled by all the players at the table, including themselves.

For example, a player might bid "five 2's."Each subsequent player can either then make a higher bid of the same face (e.g., "six 2's"), or they can challenge the previous bid.If the player challenges the previous bid, all players reveal their dice. If the bid is matched or exceeded, the bidder wins. Otherwise the challenger wins.If the bidder loses, they remove one of their dice from the game by placing it in front of their dice cup.The loser of the previous round begins the next round.(In the event that the game comes down to two players with only a single dice each, bids are then made on the sum of both dice instead the quantity of faces rolled.)

