# Liar's Dice

A Python implementation of the classic dice game **Liar's Dice** for multiple players.

## Game Overview

Liar's Dice is a bluffing game where players roll dice in secret and try to outguess or challenge each other's bids. The game continues over multiple rounds until only one player remains.

## Rules

1. **Setup**
   - Each player has **five standard 6-sided dice**.
   - All players roll their dice simultaneously at the start of each round, keeping their rolls hidden.

2. **Wild Dice Mode**
   - **1 is wild**: it counts as any dice face.
   - Example: If you roll three 1s and two 5s, you can claim **five 5s**.

3. **Bidding**
   - Each player states a **bid**: a quantity and a face value.
   - The quantity represents the total number of that face among all players’ dice.
   - The **first bet** is always `0 dices of 1`.

4. **Player Actions**
   - On their turn, a player can:
     1. **Raise the bid** – increase the quantity or choose a higher face value at the same quantity.
     2. **Challenge** the previous bid.

5. **Resolution**
   - If a bid is challenged, all dice are revealed:
     - If the bid is valid (enough dice match the face value, including wilds), the **bidder wins**.
     - Otherwise, the **challenger wins**.
   - The **loser** of the round loses one die.

6. **Winning the Game**
   - The game continues until only one player has dice remaining. That player is the **winner**.
   - The loser of a round starts the next round’s bidding, unless they are eliminated. In that case, the next available player begins.

## Software

1. **Python 3.13.2**.
2. IDE-PyCharm
   
