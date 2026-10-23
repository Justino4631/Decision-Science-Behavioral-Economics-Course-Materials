"""

model.py

The model class for a connect 4 gameboard

author: Kevin Brewer
date: 1 Feb 2021 - Spring 2023, Spring 2024
version: 3.8.3 64-bit

"""

import copy


class Model:
    """Connect 4 model."""

    def __init__(self, num_rows=6, num_cols=7) -> None:
        """
        Initialize the Model class for Connect 4 with a certain number of rows and columns
        """
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.player_ids = [1, 2]
        self.board = []
        self.last_action = None
        self.last_player = 2  # player 1 will go first
        self.reset()

    def num_pieces_on_board(self) -> int:
        """
        Provide the number of pieces on the gameboard
        """

        count = 0
        for row in self.board:
            for item in row:
                if item != 0:
                    count += 1
        return count

    def get_num_columns(self) -> int:
        """
        Provide the number of columns in the gameboard
        """
        return self.num_cols

    def get_gb_size(self) -> int:
        """
        Provide the number of cells in the gameboard
        """
        return self.num_cols * self.num_rows

    def reset(self) -> None:
        """
        Reset the gameboard to an empty board
        """
        self.board = []
        self.last_action = None
        self.last_player = 2  # player 1 will go first
        # self.board[row][column]
        for i in range(self.num_rows):
            row = [0 for j in range(self.num_cols)]
            self.board.append(row)

    def return_game_board(self) -> list[list[int]]:
        """
        Provide board as list of list of integers
        The result is ordered by rows, from top to bottom.
        result[1][4] is the value of the cell in the second row from top and fifth column from left.
        Values are 0 = empty, 1 = player 1, 2 = player 2.
        """
        return copy.deepcopy(self.board)

    def set_game_board(self, input_board: list[list[int]]) -> None:
        """
        Set the entire gameboard to input_board.
        """
        if input_board is None:
            self.reset()
        else:
            self.board = copy.deepcopy(input_board)
            self._update_last_player_from_board()
    
    def _update_last_player_from_board(self) -> None:
        """
        Update last_player based on the current board state.
        """
        count1 = 0
        count2 = 0
        for row in self.board:
            for cell in row:
                if cell == 1:
                    count1 += 1
                elif cell == 2:
                    count2 += 1
        
        # If equal pieces, player 2 went last (since player 1 goes first)
        # If player 1 has more pieces, player 1 went last
        if count1 > count2:
            self.last_player = 1
        elif count2 > count1:
            self.last_player = 2
        else:
            self.last_player = 2  # Equal means player 2 went last

    def add_piece(self, column: int, playerID: int) -> int:
        """
        Add a piece to a column, return success flag as what row piece landed. Returns -1 if not successful.
        """
        col = self._get_column(column)
        for i in range(self.num_rows):
            if col[i] == 0:
                self.board[self.num_rows - i - 1][column] = playerID
                self.last_action = column
                self.last_player = playerID
                return self.num_rows - i - 1
        return -1

    def _get_column(self, c: int) -> list[int]:
        """
        PRIVATE METHOD: return a list with column data, ordered from bottom to top.
        """
        result = []
        for row in self.board:
            result.append(row[c])
        result.reverse()
        return result

    def valid_moves(self) -> list[int]:
        """
        Return a list with column numbers that have space for a move.
        """
        result = []
        for c in range(self.num_cols):
            column = self._get_column(c)
            for r in range(self.num_rows):
                if column[r] == 0:
                    result.append(c)
                    break
        return result
    
    def get_valid_moves(self, player_id: int) -> list[int]:
        """
        Return a list with column numbers that have space for a move
        player_id parameter is included for compatibility but not used in Connect4.
        """
        return self.valid_moves()

    def is_full_board(self) -> bool:
        """
        Return boolean if board is full or not.
        """
        for row in self.board:
            for item in row:
                if item == 0:
                    return False
        return True

    def game_over(self) -> bool:
        """
        Determine if game is over (either a winner or a full board).
        """
        if self.is_winner(1):
            return True
        elif self.is_winner(2):
            return True
        elif self.is_full_board():
            return True
        return False

    def is_winner(self, playerID: int, print_flag: bool = False) -> bool:
        """
        Determine if a particular player is a winner.
        """
        # checks if there is four in a row of a specific player on the gameboard
        piece = playerID  # get value of piece
        height = self.num_rows
        width = self.num_cols

        # check horizontal spaces
        for y in range(height):  # by rows
            for x in range(width - 3):  # by columns
                if (
                    self.board[y][x] == piece
                    and self.board[y][x + 1] == piece
                    and self.board[y][x + 2] == piece
                    and self.board[y][x + 3] == piece
                ):
                    if print_flag:
                        print("Horizontal win")
                    return True

        # check vertical spaces
        for x in range(width):  # by columns
            for y in range(height - 3):  # by rows
                if (
                    self.board[y][x] == piece
                    and self.board[y + 1][x] == piece
                    and self.board[y + 2][x] == piece
                    and self.board[y + 3][x] == piece
                ):
                    if print_flag:
                        print("Vertical win")
                    return True

        # check / diagonal spaces
        for x in range(width - 3):
            for y in range(3, height):
                if (
                    self.board[y][x] == piece
                    and self.board[y - 1][x + 1] == piece
                    and self.board[y - 2][x + 2] == piece
                    and self.board[y - 3][x + 3] == piece
                ):
                    if print_flag:
                        print("Diagonal / win")
                    return True

        # check \ diagonal spaces
        for x in range(width - 3):
            for y in range(height - 3):
                if (
                    self.board[y][x] == piece
                    and self.board[y + 1][x + 1] == piece
                    and self.board[y + 2][x + 2] == piece
                    and self.board[y + 3][x + 3] == piece
                ):
                    if print_flag:
                        print("Diagonal \\ win")
                    return True

        return False


def main() -> None:
    newClass = Model()

if __name__ == "__main__":
    main()