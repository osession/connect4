import random
from PyQt5.QtCore import QObject
from controller import Communicate
from typing import Tuple

class Grid(QObject):
    def __init__(self, communicate):
        super().__init__()
        self.communicate = communicate
        self.communicate.user_move.connect(self.receiveUserMoveAndEmitOpponentMove)
        self.grid = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ]

        self.PLAYER = "Y"
        self.OPPONENT = "R"

        self.GRID_HEIGHT = 6
        self.GRID_WIDTH = 7

    def getValidMoves(self) -> list:
        valid_moves = []
        for col in range(self.GRID_WIDTH):
            for row in range(self.GRID_HEIGHT):
                if self.grid[row][col] == ' ':
                    valid_moves.append(col)
                    break
        print(valid_moves)
        return valid_moves

    def receiveUserMoveAndEmitOpponentMove(self, user_row: int, user_col: int) -> None:
        # update the grid with the user move
        self.grid[user_row][user_col] = self.PLAYER
        for row in self.grid[::-1]:
            print(''.join(row))
        # make opponent move (and update the grid)
        opponent_row, opponent_col = self.makeRandomOpponentMove()
        # send the move back to the GUI
        self.communicate.opponent_move.emit(opponent_row, opponent_col)
    def makeStrategicOpponentMove(self) -> None:
        pass

    def makeRandomOpponentMove(self) -> Tuple[int, int]:
        valid_moves = self.getValidMoves()
        rand_index = random.randint(0, len(valid_moves) - 1)
        col = valid_moves[rand_index]
        update_made = False
        row = None
        for row in range(self.GRID_HEIGHT):
            if self.grid[row][col] == ' ':
                self.grid[row][col] = self.OPPONENT
                update_made = True
                break

        if not update_made:
            raise IndexError('Invalid move. Column is already full.')

        return row, col
    #
    # def checkIfGameOver(self) -> bool:
    #     # check if game is won vertically
    #     for col in range(self.GRID_WIDTH):
    #         previous_color = None
    #         num_continuous = 1
    #         actual_col = self.column_map[f'COL{col + 1}']
    #         for row in range(self.GRID_HEIGHT):
    #             if previous_color is None:
    #                 previous_color = self.grid[row][actual_col]
    #                 continue
    #             token = self.grid[row][actual_col]
    #             if token != ' ':
    #                 if token == previous_color:
    #                     num_continuous += 1
    #                     if num_continuous == 4:
    #                         return True
    #                 else:
    #                     num_continuous = 1
    #                 previous_color = token
    #             else:
    #                 break
    #
    #     # check if game is won horizontally
    #     for row in range(self.GRID_HEIGHT):
    #         previous_color = None
    #         num_continuous = 1
    #         for col in range(self.GRID_WIDTH):
    #             actual_col = self.column_map[f'COL{col + 1}']
    #             if previous_color is None:
    #                 previous_color = self.grid[row][actual_col]
    #                 continue
    #             token = self.grid[row][actual_col]
    #             if token != ' ':
    #                 if token == previous_color:
    #                     num_continuous += 1
    #                     if num_continuous == 4:
    #                         return True
    #                 else:
    #                     num_continuous = 1
    #                 previous_color = token
    #             else:
    #                 previous_color = None
    #                 continue
    #
    #     # check if game is won diagonally (bottom-left to top-right)
    #     for row in range(self.GRID_HEIGHT - 3):
    #         for col in range(self.GRID_WIDTH - 3):
    #             actual_col = self.column_map[f'COL{col + 1}']
    #             next_col1 = self.column_map[f'COL{col + 2}']
    #             next_col2 = self.column_map[f'COL{col + 3}']
    #             next_col3 = self.column_map[f'COL{col + 4}']
    #             if (self.grid[row][actual_col] == self.grid[row + 1][next_col1] == self.grid[row + 2][next_col2] == self.grid[row + 3][next_col3]) and (self.grid[row][actual_col] != ' '):
    #                 return True
    #
    #     # check if game is won diagonally (bottom-right to top-left)
    #     for row in range(self.GRID_HEIGHT - 3):
    #         for col in range(3, self.GRID_WIDTH):
    #             actual_col = self.column_map[f'COL{col + 1}']
    #             next_col1 = self.column_map[f'COL{col}']
    #             next_col2 = self.column_map[f'COL{col - 1}']
    #             next_col3 = self.column_map[f'COL{col - 2}']
    #             if (self.grid[row][actual_col] == self.grid[row + 1][next_col1] == self.grid[row + 2][next_col2] == self.grid[row + 3][next_col3]) and (self.grid[row][actual_col] != ' '):
    #                 return True
    #
    #     return False