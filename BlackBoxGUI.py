# Author: Karen Black
# Date: 8/25/2020
# Description: Single-player implementation of the logic and strategy game 'Black Box'.
#               Main file for game play.

import pygame
from random import sample
from itertools import product
from Board import GameBoard

class BlackBoxGame:
    """Implementation of the Black Box game. Contains method to create a GameBoard instance with indicated atom
    placement. Contains methods to shoot rays, adjust the game score, guess atom locations, get the current score,
    and get how many atoms are left to guess."""

    def __init__(self):
        self._atom_list = sample(list(product(range(1,9), repeat=2)), k=5)  # initialize random list of atom locations
        self._gameB = GameBoard(self._atom_list)        # initialize a game board with the atom list
        self._board = self._gameB.get_board()           # get the game board for calculating ray path
        self._score = 25                                # initialize the starting points for the game
        self._ray_locations = []                        # empty list to store ray entry/exit squares
        self._wrong_atom_guesses = []                   # empty list to store incorrect atom guesses
        self._correct_atom_guesses = []                 # empty list to store correct atom guesses
        self._ray_status = None
        self._ray_row = None
        self._ray_column = None
        self._screen = pygame.display.set_mode((600, 800))
        self._font = pygame.font.Font('freesansbold.ttf', 36)
        self.background = pygame.image.load('board_grid.png')
        self.background = pygame.transform.scale(self.background, (600, 600))
        self._game_status = True
        self._ray_color = None

    def shoot_ray(self, row, column):
        """Accepts as parameters a row and column that designates the entry point of a ray. Simulates the ray path
        with appropriate hit, detours and/or reflections. Returns 'False' if the entry row and column are not legal
        plays (non-corner border squares). Returns 'None' if the play is a hit. Returns a tuple of exit square row and
        column if the play exits the game black box. Deducts from the player's score: 1 point for ray entry and 1 point
        for ray exit, if the squares have not already been used."""

        # check if ray is being shot from corner square
        if (row == 0 or row == 9) and (column == 0 or column == 9):
            return False

        # check if ray is being shot from non-border square
        if row in range(1, 9) and column in range(1, 9):
            return False

        if self._ray_color is None:
            self._ray_color = 0
        else:
            self._ray_color += 1

        self.adjust_score(row, column, self._ray_color)                                  # adjust score for entry ray position
        self._ray_status = 'Play'                                       # set flag variable for ray status

        if column == 0 or column == 9:                                  # if shooting from horizontal position
            if column == 0:                                             # if ray is moving to the right
                self.horiz_move_right(row, column)
            elif column == 9:                                           # if ray is moving to the left
                self.horiz_move_left(row, column)

        if row == 0 or row == 9:                                        # if shooting from vertical position
            if row == 0:                                                # if ray is moving down
                self.vert_move_down(row, column)
            elif row == 9:                                              # if ray is moving up
                self.vert_move_up(row, column)

        if self._ray_status == "Hit":                                   # if ray hits an atom
            return None

        elif self._ray_status == "Exit":                                # if ray is a miss
            self.adjust_score(self._ray_row, self._ray_column, self._ray_color)          # adjust score with exit ray position
            return self._ray_row, self._ray_column

    def horiz_move_right(self, ray_path_r, ray_path_c):
        """Accepts as parameters the current row and column of the ray path. Calculates the next square of
        a horizontal ray path to the right and determines if there are any atoms resulting in a hit or detour.
        Adjusts ray status variable if there is a Hit or Exit. Returns nothing."""

        self._ray_row = ray_path_r
        self._ray_column = ray_path_c

        while self._ray_status == "Play":                       # continue ray path determination while still in "play"

            # check for edge case reflection
            if ray_path_c == 0 and self._ray_column == 0:
                if (self._board[ray_path_r+1][ray_path_c+1]) or (self._board[ray_path_r-1][ray_path_c+1]) == 'A':
                    self._ray_column -=1
                    self._ray_status = "Exit"

            self._ray_column += 1                               # move ray path one square to the right

            # check if ray is exiting 'black box'
            if self._ray_column == 9:
                self._ray_status = "Exit"

            # check for hit
            elif self._board[self._ray_row][self._ray_column] == 'A':  # if atom is in next ray path square
                self._ray_status = "Hit"

            # check for reflection
            elif (self._board[self._ray_row+1][self._ray_column]) and (self._board[self._ray_row-1][self._ray_column]) == 'A':
                self._ray_column -=1
                self.horiz_move_left(self._ray_row, self._ray_column)

            # check for detour (change ray path to 'up)
            elif self._board[self._ray_row + 1][self._ray_column] == 'A':
                self._ray_column -=1
                self.vert_move_up(self._ray_row, self._ray_column)

            # check for detour (change ray path to 'down)
            elif self._board[self._ray_row-1][self._ray_column] == 'A':
                self._ray_column -=1
                self.vert_move_down(self._ray_row, self._ray_column)

    def horiz_move_left(self, ray_path_r, ray_path_c):
        """Accepts as parameters the current row and column of the ray path. Calculates the next square of
        a horizontal ray path moving to the left and determines if there are any atoms resulting in a hit or detour.
        Adjusts ray status variable if there is a Hit or Exit. Returns nothing."""

        self._ray_row = ray_path_r
        self._ray_column = ray_path_c

        while self._ray_status == "Play":                      # continue ray path determination while still in "play"

            # check for edge case reflection
            if ray_path_c == 9 and self._ray_column == 9:
                if (self._board[ray_path_r+1][ray_path_c-1]) or (self._board[ray_path_r-1][ray_path_c-1]) == 'A':
                    self._ray_column +=1
                    self._ray_status = "Exit"

            self._ray_column -= 1                              # move ray path one square to the left

            # check for exit
            if self._ray_column == 0:
                self._ray_status = "Exit"

            # check for hit
            elif self._board[self._ray_row][self._ray_column] == 'A':  # if atom is in next ray path square
                self._ray_status = "Hit"

            # check for reflection
            elif (self._board[self._ray_row+1][self._ray_column]) and (self._board[self._ray_row-1][self._ray_column]) == 'A':
                self._ray_column += 1
                self.horiz_move_right(self._ray_row, self._ray_column)

            # check for detour (change to 'up' direction)
            elif self._board[self._ray_row + 1][self._ray_column] == 'A':
                self._ray_column +=1
                self.vert_move_up(self._ray_row, self._ray_column)

            # check for detour (change to 'down' direction)
            elif self._board[self._ray_row-1][self._ray_column] == 'A':
                self._ray_column +=1
                self.vert_move_down(self._ray_row, self._ray_column)

    def vert_move_down(self, ray_path_r, ray_path_c):
        """Accepts as parameters the current row and column of the ray path. Calculates the next square of a vertical
        ray path moving down and determines if there are any atoms resulting in a hit or detour. Adjusts ray status
        variable if there is a Hit or Exit. Returns nothing."""

        self._ray_row = ray_path_r
        self._ray_column = ray_path_c

        while self._ray_status == "Play":                       # continue ray path determination while still in "play"

            # check for edge case reflection
            if ray_path_r == 0 and self._ray_row == 0:
                if (self._board[ray_path_r+1][ray_path_c+1]) or (self._board[ray_path_r+1][ray_path_c-1]) == 'A':
                    self._ray_row -=1
                    self._ray_status = "Exit"

            self._ray_row += 1                                 # adjust ray path one square 'down'

            # check for exit
            if self._ray_row == 9:
                self._ray_status = "Exit"

            # check for hit
            elif self._board[self._ray_row][self._ray_column] == 'A':  # if atom is in next ray path square
                self._ray_status = "Hit"

            # check for reflection
            elif (self._board[self._ray_row][self._ray_column+1]) and (self._board[self._ray_row][self._ray_column-1]) == 'A':
                self._ray_row -=1
                self.vert_move_up(self._ray_row, self._ray_column)

            # check for detour (change direction to 'left' direction)
            elif self._board[self._ray_row][self._ray_column +1] == 'A':
                self._ray_row -= 1
                self.horiz_move_left(self._ray_row, self._ray_column)

            # check for detour (change direction to 'right' direction
            elif self._board[self._ray_row][self._ray_column-1] == 'A':
                self._ray_row -= 1
                self.horiz_move_right(self._ray_row, self._ray_column)

    def vert_move_up(self, ray_path_r, ray_path_c):
        """Accepts as parameters the current row and column of the ray path. Calculates the next square of a vertical
        ray path moving up and determines if there are any atoms resulting in a hit or detour. Adjusts ray status
        variable if there is a Hit or Exit. Returns nothing."""

        self._ray_row = ray_path_r
        self._ray_column = ray_path_c

        while self._ray_status == "Play":                       # continue ray path determination while still in "play"

            # check for edge case reflection
            if ray_path_r == 9 and self._ray_row == 9:
                if (self._board[ray_path_r-1][ray_path_c+1]) or (self._board[ray_path_r-1][ray_path_c-1]) == 'A':
                    self._ray_row +=1
                    self._ray_status = "Exit"

            self._ray_row -= 1                                  # adjust ray path one square in 'up' direction

            # check for exit
            if self._ray_row == 0:
                self._ray_status = "Exit"

            # check for hit
            elif self._board[self._ray_row][self._ray_column] == 'A':  # if atom is in next ray path square
                self._ray_status = "Hit"

            # check for reflection
            elif (self._board[self._ray_row][self._ray_column+1]) and (self._board[self._ray_row][self._ray_column-1]) == 'A':
                # self._ray_row +=1
                self.vert_move_down(self._ray_row, self._ray_column)

            # check for detour (change direction to 'left' direction)
            elif self._board[self._ray_row][self._ray_column +1] == 'A':
                self._ray_row += 1
                self.horiz_move_left(self._ray_row, self._ray_column)

            # check for detour (change direction to 'right' direction)
            elif self._board[self._ray_row][self._ray_column-1] == 'A':
                self._ray_row += 1
                self.horiz_move_right(self._ray_row, self._ray_column)

    def update_game_status(self):
        """Update the game status for game win or loss. Display message to screen."""

        # update for a game loss, score below 0
        if self._score <= 0:  # check if game is over (score of 0 or less)
            game_loss = self._font.render('YOU LOSE!   FINAL SCORE: ' + str(self._score), True, (0, 0, 0))
            self._screen.blit(game_loss, (10, 750))
            for atom in self._atom_list:
                self.draw_marker((0, 0, 0), atom)
            pygame.display.update()

        if len(self._atom_list) == 0:                       # once all atoms are guessed, the game is over
            game_win = self._font.render('YOU WIN!   FINAL SCORE: ' + str(self._score), True, (0, 0, 0))
            self._screen.blit(game_win, (10, 750))

    def adjust_score(self, row, column, color, atom_guess=None):
        """Accepts as parameters a row and column and assignment for the variable atom_guess (default
        argument of None). If the method call initiates from shoot_ray method, the default argument of None is used
        and decrements the player's score by 1 point if the entry/exit square has not already been used. If the method
        call originates from the guess_atom method, the atom_guess default argument is utilized and 5 points are
        deducted from the player's score if the guess is not a previous guess. Does not return anything."""

        # decrement the score for a ray entry/exit point
        if atom_guess is None:
            if (row, column) not in self._ray_locations:
                self._ray_locations.append((row, column, color))           # add to ray locations list
                self._gameB.update_ray_points(row, column)          # update the used ray location to game board visual
                self._score -= 1                                    # decrement the score by 1 point

        # decrement the score for an atom guess
        if atom_guess is True:
            if (row, column) not in self._wrong_atom_guesses:
                self._wrong_atom_guesses.append((row, column))            # add to atom_guesses list
                self._score -= 5                                          # decrement the score by 5 points

    def guess_atom(self, row, column):
        """Accepts as parameters a row and column that represents the player's guess for an atom location. Returns True
        if the guess is correct. If the guess is incorrect, decrements the player's score and returns False."""

        if (row, column) in self._atom_list:
            self._atom_list.remove((row, column))               # if guess is in atom list, remove from list
            self._correct_atom_guesses.append((row, column))    # add to correct atom guess list
            return True

        else:
            # if guess is incorrect, send the guess to adjust_score and include parameter 'True' to indicate atom guess
            self.adjust_score(row, column, None, True)
            return False

    def atoms_left(self):
        """Accepts no parameters and returns the number of atoms that haven't been guessed."""
        atoms_left = self._font.render('Atoms Left: ' + str(len(self._atom_list)), True, (0, 0, 0))
        self._screen.blit(atoms_left, (10, 670))

    def get_score(self):
        current_score = self._font.render('Score: ' + str(self._score), True, (0, 0, 0))
        self._screen.blit(current_score,(10, 610))

    def calculate_square(self, coord):
        """Accepts as a parameter the x- y- coordinates of a mouse click and calculates the corredsponding row and column
        of the board game square. The x- coordinate is equivalent to the column and the y-coordinate is equivalent to
        the column"""
        col = (coord[0] // 60)
        row = (coord[1] // 60)
        return col, row

    def check_events(self):
        """Accepts no parameters. Checks the events of the pygame. Quits game when necessary. Otherwise, checks
        detection of mouseclick, gets the x-y coordinates of mouseclick, sends to function to calculate corresponding
        square on game board. Sends square to shoot_ray or guess_atom function."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_status = False

            # get coordinates of mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos_tup = self.calculate_square(pos)  # change x-y coord to square of row, column
                row = pos_tup[0]
                column = pos_tup[1]
                if (row == 0 or row == 9) or (column == 0 or column == 9):
                    self.shoot_ray(row, column)
                elif 0 < row < 9 and 0 < column < 9:
                    self.guess_atom(row, column)

    def update_screen(self):
        """Update display screen with ray locations, atom location, current score, and atoms left to guess"""

        color_list = [(91, 109, 212), (237, 210, 159), (195, 124, 242),
                      (182, 252, 251), (45, 51, 237), (247, 243, 2), (123, 31, 181),
                      (237, 104, 2), (242, 124, 226), (62, 47, 135), (106, 33, 122)]

        self._screen.fill((240, 240, 240))
        self._screen.blit(self.background, (0, 0))
        self.get_score()
        self.atoms_left()
        for ray in self._ray_locations:
            self.draw_marker(color_list[ray[2]], (ray[0], ray[1]))
        for atom in self._wrong_atom_guesses:
            self.draw_marker((255,0,0), atom)
        for atom in self._correct_atom_guesses:
            self.draw_marker((20, 255, 3), atom)

        self.update_game_status()

        pygame.display.update()

    def draw_marker(self, color, pos):
        """Accepts a color as a parameter. Draws a marker at the indicated position (x-y coordinates)"""

        x_coord = pos[1]*60 + 30
        y_coord = pos[0]*60 + 30
        pygame.draw.circle(self._screen, color, (y_coord, x_coord), 20, 50)

    def get_game_status(self):
        return self._game_status



def main():
    """Main game play code"""

    pygame.init()  # initialize pygame

    # Colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    purple = (214, 3, 255)
    pink = (255, 51, 255)
    aqua = (3, 248, 255)
    green = (20, 255, 3)
    red = (255, 0, 0)

    # Title
    pygame.display.set_caption("Black Box Game")

    current_game = BlackBoxGame()

    # Game loop

    while current_game.get_game_status():
        current_game.check_events()
        current_game.update_screen()

    pygame.quit()


if __name__ == '__main__':
    main()

