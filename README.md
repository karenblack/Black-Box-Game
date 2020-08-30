# Black-Box-Game

Python implemenation of the logic-based board game 'Black Box'.

## How to play:

All files must be downloaded to play. Run 'BlackBoxGUI.py' to initiate the game.

Complete game instructions can be found:
https://en.wikipedia.org/wiki/Black_Box_(game)

This implementation is a single-player game where 5 atoms are randomly assigned within the 'black box'. A player starts with 25 points. 1 point is deducted per ray entry and exit point. 5 points are deducted for each incomplete atom guess. 

#### Shoot Rays
The player 'shoots rays' from the appropriate border squares into the 'back box' and uses the results of the 'ray shots' to deduce atom locations. Ray entry and exit locations are couple by the same color pairing per 'ray shot'. A 'ray shot' with an etnry location, but no exit location would indicate a 'hit'.

#### Guess Atoms
An atom guess can be placed at any time by clicking the designated interior square. A green marker indicates a correct atom guess. A red marker indicates an incorrect atom guess. 

#### Win or Loss
The game is over when the player correctly guesses all atoms (win) in the 'black box' or the player score reaches zero (lost). If the player loses, the remaining atom locations are revealed. 

## Continued improvements
I am continuing to organize my code into more efficient classes and functions. 
I am also continuing to update player-game features including:
  * A feature to restart a game after a win/loss without closing the program
  * The ability to play a 2-person game with one player manually entering atom locations
  * Designating a ray 'hit' or 'reflection' with a different color scheme than entry/exit locations
