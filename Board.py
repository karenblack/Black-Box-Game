class GameBoard:
    """Implementation of a game board consisting of a 10 x 10 grid to be used in the Black Box game. Contains an init
    method that accepts a list of atoms as a parameter, initializes the board, places the  atoms on the game board.
    Contains an update ray points method to visualize where entry and exit rays throughout game play, a get board
    method that returns the game board, and a print board method to print the game board to the game console."""

    def __init__(self, atom_list):
        """Initializes an empty board game with a total of 10 rows and 10 columns. The inner 8 rows and 8 columns
        represent the black box containing the atoms. The border squares represent ray entry and exit points. The
        corner squares cannot be utilized in game play. Accepts as a parameter a list of tuples designating atom
        positions on the board and sets the game board with those locations. Returns nothing."""

        self._board = [['' for row in range(0, 10)] for column in range(0, 10)]
        for row_a, column_a in atom_list:
            self._board[row_a][column_a] = 'A'

    def update_ray_points(self, row, column):
        """Accepts as parameters a row and column that represents a ray entry or exit square. Places an 'X' symbol
        in the square to indicate the square has been used. Does not return anything."""

        self._board[row][column] = 'X'

    def get_board(self):
        """Accepts no parameters. Returns the current game board state."""
        return self._board

    def print_board(self):
        """Prints the current status of the game board to the console window. Does not return anything."""

        for row in self._board:
            print(row)

# class Markers:
#
#     def __init
#
#     def draw_marker(self, color, pos):
#         """Accepts a color as a parameter. Draws a circle using built in
#         pygame.draw.circle(screen, color, (x-y coord), radius, thickness)"""
#         x_coord = pos[1]*60 + 30
#         y_coord = pos[0]*60 + 30
#         pygame.draw.circle(self._screen, color, (y_coord, x_coord), 20, 50)