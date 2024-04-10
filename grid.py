import random

class Grid:
    def __init__(self):
        self.grid = [
            ['|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|'],
            ['|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|'],
            ['|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|'],
            ['|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|'],
            ['|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|'],
            ['|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|'],
        ]
        self.column_map = {'COL1': 1, 'COL2': 3, 'COL3': 5, 'COL4': 7, 'COL5': 9, 'COL6': 11, 'COL7': 13}

        self.PLAYER = "Y"
        self.OPPONENT = "R"

        self.GRID_HEIGHT = 6
        self.GRID_WIDTH = 7

    def getValidMoves(self) -> list:
        valid_moves = []
        for col in range(self.GRID_WIDTH):
            actual_col = self.column_map[f'COL{col + 1}']
            for row in range(self.GRID_HEIGHT):
                if self.grid[row][actual_col] == ' ':
                    valid_moves.append(col + 1)
                    break
        print(valid_moves)
        return valid_moves

    def updateGridWithUserMove(self, move: str) -> None:
        col = self.column_map[move]
        update_made = False
        for i in range(self.GRID_HEIGHT):
            if self.grid[i][col] == ' ':
                self.grid[i][col] = self.PLAYER
                update_made = True
                break

        if not update_made:
            raise IndexError('Invalid move. Column is already full.')

    def makeStrategicOpponentMove(self) -> None:
        pass

    def makeRandomOpponentMove(self) -> None:
        valid_moves = self.getValidMoves()
        rand_index = random.randint(0, len(valid_moves) - 1)
        move = valid_moves[rand_index]
        col = self.column_map[f'COL{move}']
        update_made = False
        for i in range(self.GRID_HEIGHT - 1):
            if self.grid[i][col] == ' ':
                self.grid[i][col] = self.OPPONENT
                update_made = True
                break

        if not update_made:
            raise IndexError('Invalid move. Column is already full.')

    def checkIfGameOver(self) -> bool:
        # check if game is won vertically
        for col in range(self.GRID_WIDTH):
            previous_color = None
            num_continuous = 1
            actual_col = self.column_map[f'COL{col + 1}']
            for row in range(self.GRID_HEIGHT):
                if previous_color is None:
                    previous_color = self.grid[row][actual_col]
                    continue
                token = self.grid[row][actual_col]
                if token != ' ':
                    if token == previous_color:
                        num_continuous += 1
                        if num_continuous == 4:
                            return True
                    else:
                        num_continuous = 1
                    previous_color = token
                else:
                    break

        # check if game is won horizontally
        for row in range(self.GRID_HEIGHT):
            previous_color = None
            num_continuous = 1
            for col in range(self.GRID_WIDTH):
                actual_col = self.column_map[f'COL{col + 1}']
                if previous_color is None:
                    previous_color = self.grid[row][actual_col]
                    continue
                token = self.grid[row][actual_col]
                if token != ' ':
                    if token == previous_color:
                        num_continuous += 1
                        if num_continuous == 4:
                            return True
                    else:
                        num_continuous = 1
                    previous_color = token
                else:
                    previous_color = None
                    continue

        # check if game is won diagonally

        # Check diagonals from bottom-left to top-right
        # for start_row in range(self.GRID_HEIGHT - 3):
        #     for start_col in range(self.GRID_WIDTH - 3):
        #         if (self.grid[start_row][start_col] == self.PLAYER and
        #                 self.grid[start_row + 1][start_col + 1] == self.PLAYER and
        #                 self.grid[start_row + 2][start_col + 2] == self.PLAYER and
        #                 self.grid[start_row + 3][start_col + 3] == self.PLAYER):
        #             game_won = True
        #
        # # Check diagonals from top-left to bottom-right
        # for start_row in range(3, self.GRID_HEIGHT):
        #     for start_col in range(self.GRID_WIDTH - 3):
        #         if (self.grid[start_row][start_col] == self.PLAYER and
        #                 self.grid[start_row - 1][start_col + 1] == self.PLAYER and
        #                 self.grid[start_row - 2][start_col + 2] == self.PLAYER and
        #                 self.grid[start_row - 3][start_col + 3] == self.PLAYER):
        #             game_won = True
        return False