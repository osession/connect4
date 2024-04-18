import random
from PyQt5.QtCore import QObject
from typing import Tuple, Union
import copy


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

    def getValidMoves(self, grid: list) -> list:
        valid_moves = []
        for col in range(self.GRID_WIDTH):
            for row in range(self.GRID_HEIGHT):
                if grid[row][col] == ' ':
                    valid_moves.append(col)
                    break
        return valid_moves

    def receiveUserMoveAndEmitOpponentMove(self, user_row: int, user_col: int) -> None:
        # update the grid with the user move
        self.grid[user_row][user_col] = self.PLAYER

        winning_piece = self.checkIfGameOver(self.grid)
        if winning_piece:
            self.communicate.game_over.emit(winning_piece)

        # opponent_row, opponent_col = self.makeRandomOpponentMove()
        _, opponent_col = self.minimax(self.grid, 3)
        # _, opponent_col = self.alphabeta(self.grid)
        print(f'BEST MOVE: {opponent_col}')
        # find the corresponding row and update the grid for the model
        opponent_row = None
        if opponent_col is not None:
            for row in range(self.GRID_HEIGHT):
                if self.grid[row][opponent_col] == ' ':
                    self.grid[row][opponent_col] = self.OPPONENT
                    opponent_row = row
                    break
            # send the move back to the GUI
            self.communicate.opponent_move.emit(opponent_row, opponent_col)

        winning_piece = self.checkIfGameOver(self.grid)
        if winning_piece:
            self.communicate.game_over.emit(winning_piece)

    def minimax(self, state: list, depth: int = 3, maximizing_player=True):
        valid_moves = self.getValidMoves(state)
        winning_piece = self.checkIfGameOver(state)
        is_terminal = True if len(valid_moves) == 0 or winning_piece is not None else False
        if depth == 0 or is_terminal:
            if is_terminal:
                if winning_piece == self.OPPONENT:
                    return (100000000000000, None)
                elif winning_piece == self.PLAYER:
                    return (-10000000000000, None)
                else:  # Game is over, no more valid moves
                    return (0, None)
            else:  # Depth is zero
                return (self.evaluate(state, self.OPPONENT), None)

        if maximizing_player:
            best_score = float('-inf')
            best_move = None
            for move in valid_moves:
                new_state = self.getNewState(move, copy.deepcopy(state))
                score, _ = self.minimax(new_state, depth - 1, False)
                print(f'maximizing player score: {score}')
                print(f'maximizing player move: {move}')
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for move in valid_moves:
                new_state = self.getNewState(move, copy.deepcopy(state))
                score, _ = self.minimax(new_state, depth - 1, True)
                print(f'minimizing player score: {score}')
                print(f'minimizing player move: {move}')
                if score < best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move

    def alphabeta(self, state: list, depth: int = 3, alpha=float('-inf'), beta=float('inf'), maximizing_player=True):
        valid_moves = self.getValidMoves(state)
        winning_piece = self.checkIfGameOver(state)
        is_terminal = True if len(valid_moves) == 0 or winning_piece is not None else False
        if depth == 0 or is_terminal:
            if is_terminal:
                if winning_piece == self.OPPONENT:
                    return (100000000000000, None)
                elif winning_piece == self.PLAYER:
                    return (-10000000000000, None)
                else:  # Game is over, no more valid moves
                    return (0, None)
            else:  # Depth is zero
                return (self.evaluate(state, self.OPPONENT), None)

        if maximizing_player:
            best_score = float('-inf')
            best_move = None
            for move in valid_moves:
                new_state = self.getNewState(move, copy.deepcopy(state))
                score, _ = self.alphabeta(new_state, depth - 1, alpha, beta, False)
                print(f'maximizing player score: {score}')
                print(f'maximizing player move: {move}')
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for move in valid_moves:
                new_state = self.getNewState(move, copy.deepcopy(state))
                score, _ = self.alphabeta(new_state, depth - 1, alpha, beta, True)
                print(f'minimizing player score: {score}')
                print(f'minimizing player move: {move}')
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, score)
                if alpha <= beta:
                    break
            return best_score, best_move

    def evaluate(self, board, piece):
        score = 0
        WINDOW_LENGTH = 4
        ## Score center column
        center_array = [token for token in list(board[:][self.GRID_WIDTH // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(self.GRID_HEIGHT):
            row_array = [token for token in list(board[r][:])]
            for c in range(self.GRID_WIDTH - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(self.GRID_WIDTH):
            # col_array = [token for token in list(board[:][c])] # This is not a numpy array
            col_array = []
            for i in range(self.GRID_HEIGHT):
                col_array.append(board[i][c])
            for r in range(self.GRID_HEIGHT - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(self.GRID_HEIGHT - 3):
            for c in range(self.GRID_WIDTH - 3):
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(self.GRID_HEIGHT - 3):
            for c in range(self.GRID_WIDTH - 3):
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.OPPONENT if piece == self.PLAYER else self.PLAYER

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(' ') == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(' ') == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(' ') == 1:
            score -= 4

        return score

    def makeRandomOpponentMove(self) -> Tuple[int, int]:
        valid_moves = self.getValidMoves(self.grid)
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

    def getNewState(self, move: int, copy: list):
        for row in range(self.GRID_HEIGHT):
            if copy[row][move] == ' ':
                copy[row][move] = self.OPPONENT
                break
        return copy

    def checkIfGameOver(self, state) -> Union[str, None]:
        # returns the self.PLAYER or self.OPPONENT to tell who won (or None if game is not over yet)
        # check if game is won vertically
        for col in range(self.GRID_WIDTH):
            previous_color = None
            num_continuous = 1
            for row in range(self.GRID_HEIGHT):
                if previous_color is None:
                    previous_color = state[row][col]
                    continue
                token = state[row][col]
                if token != ' ':
                    if token == previous_color:
                        num_continuous += 1
                        if num_continuous == 4:
                            print('WON VERTICALLY')
                            return token
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
                if previous_color is None:
                    previous_color = state[row][col]
                    continue
                token = state[row][col]
                if token != ' ':
                    if token == previous_color:
                        num_continuous += 1
                        if num_continuous == 4:
                            print('WON HORIZONTALLY')
                            return token
                    else:
                        num_continuous = 1
                    previous_color = token
                else:
                    previous_color = None
                    continue

        # check if game is won diagonally (bottom-left to top-right)
        for row in range(self.GRID_HEIGHT - 3):
            for col in range(self.GRID_WIDTH - 3):
                if (state[row][col] == state[row + 1][col+1] == state[row + 2][col+2] == state[row + 3][col+3]) and (state[row][col] != ' '):
                    print('WON DIAGONALLY')
                    return state[row][col]

        # check if game is won diagonally (bottom-right to top-left)
        for row in range(self.GRID_HEIGHT - 3):
            for col in range(3, self.GRID_WIDTH):
                if (state[row][col] == state[row + 1][col-1] == state[row + 2][col-2] == state[row + 3][col-3]) and (state[row][col] != ' '):
                    print('WON DIAGONALLY')
                    return state[row][col]

        return None