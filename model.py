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

    def getValidMoves(self, grid: list[list[str]]) -> list:
        valid_moves = []
        for col in range(self.GRID_WIDTH):
            for row in range(self.GRID_HEIGHT):
                if grid[row][col] == ' ':
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
        self.checkIfGameOver()
        # send the move back to the GUI
        self.communicate.opponent_move.emit(opponent_row, opponent_col)

    def makeStrategicOpponentMove(self) -> None:
        pass

    def minimax(self, state, depth, maximizing_player=True):
        if depth == 0 or len(self.getValidMoves(state)) == 0:
            return self.evaluate(state), None

        valid_moves = self.getValidMoves(state)

        if maximizing_player:
            best_score = float('-inf')
            best_move = None
            for move in valid_moves:
                new_state = self.getNewState(move)
                score, _ = self.minimax(new_state, depth - 1, False)
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for move in valid_moves:
                new_state = self.getNewState(move)
                score, _ = self.minimax(new_state, depth - 1, True)
                if score < best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move

    def alphaBeta(self, state, depth, alpha=float('-inf'), beta=float('inf'), maximizing_player=True):
        if depth == 0 or len(self.getValidMoves(state)) == 0:
            return self.evaluate(state), None

        valid_moves = self.getValidMoves(state)

        if maximizing_player:
            best_score = float('-inf')
            best_move = None
            for move in valid_moves:
                new_state = self.getNewState(move)
                score, _ = self.alphaBeta(new_state, depth - 1, alpha, beta, False)
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
                new_state = self.getNewState(move)
                score, _ = self.alphaBeta(new_state, depth - 1, alpha, beta, True)
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, score)
                if alpha <= beta:
                    break
            return best_score, best_move
    def heuristicFunction(self) -> float:
        opponent_score = 0
        player_score = 0

        # Evaluate the score based on horizontal connections
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH - 3):
                window = self.grid[row][col:col + 4]
                opponent_score += self.evaluateWindow(window, self.PLAYER)
                player_score += self.evaluateWindow(window, self.OPPONENT)

        # Evaluate the score based on vertical connections
        for col in range(self.GRID_WIDTH):
            for row in range(self.GRID_HEIGHT - 3):
                window = [self.grid[row + i][col] for i in range(4)]
                opponent_score += self.evaluateWindow(window, self.PLAYER)
                player_score += self.evaluateWindow(window, self.OPPONENT)

        # Evaluate the score based on diagonal connections (bottom-left to top-right)
        for row in range(self.GRID_HEIGHT - 3):
            for col in range(self.GRID_WIDTH - 3):
                window = [self.grid[row + i][col + i] for i in range(4)]
                opponent_score += self.evaluateWindow(window, self.PLAYER)
                player_score += self.evaluateWindow(window, self.OPPONENT)

        # Evaluate the score based on diagonal connections (bottom-right to top-left)
        for row in range(self.GRID_HEIGHT - 3):
            for col in range(3, self.GRID_WIDTH):
                window = [self.grid[row + i][col - i] for i in range(4)]
                opponent_score += self.evaluateWindow(window, self.PLAYER)
                player_score += self.evaluateWindow(window, self.OPPONENT)

        return opponent_score - player_score

    def evaluateWindow(self, window: list, player: str) -> int:
        score = 0
        opponent = self.PLAYER if player == self.OPPONENT else self.OPPONENT
        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(' ') == 1:
            score += 5
        elif window.count(player) == 2 and window.count(' ') == 2:
            score += 2

        if window.count(opponent) == 3 and window.count(' ') == 1:
            score -= 4

        return score

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

    def getNewState(self, move: int):
        new_state = copy.deepcopy(self.grid)
        for row in range(self.GRID_HEIGHT):
            if new_state[row][move] == ' ':
                new_state[row][move] = self.OPPONENT
                break
        return new_state

    def checkIfGameOver(self) -> Union[str, None]:
        # returns the self.PLAYER or self.OPPONENT to tell who won (or None if game is not over yet)
        # check if game is won vertically
        for col in range(self.GRID_WIDTH):
            previous_color = None
            num_continuous = 1
            for row in range(self.GRID_HEIGHT):
                if previous_color is None:
                    previous_color = self.grid[row][col]
                    continue
                token = self.grid[row][col]
                if token != ' ':
                    if token == previous_color:
                        num_continuous += 1
                        if num_continuous == 4:
                            print('WON VERTICALLY')
                            self.communicate.game_over.emit(token)
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
                    previous_color = self.grid[row][col]
                    continue
                token = self.grid[row][col]
                if token != ' ':
                    if token == previous_color:
                        num_continuous += 1
                        if num_continuous == 4:
                            print('WON HORIZONTALLY')
                            self.communicate.game_over.emit(token)
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
                if (self.grid[row][col] == self.grid[row + 1][col+1] == self.grid[row + 2][col+2] == self.grid[row + 3][col+3]) and (self.grid[row][col] != ' '):
                    print('WON DIAGONALLY')
                    self.communicate.game_over.emit(self.grid[row][col])
                    return self.grid[row][col]

        # check if game is won diagonally (bottom-right to top-left)
        for row in range(self.GRID_HEIGHT - 3):
            for col in range(3, self.GRID_WIDTH):
                if (self.grid[row][col] == self.grid[row + 1][col-1] == self.grid[row + 2][col-2] == self.grid[row + 3][col-3]) and (self.grid[row][col] != ' '):
                    print('WON DIAGONALLY')
                    self.communicate.game_over.emit(self.grid[row][col])
                    return self.grid[row][col]

        self.communicate.game_over.emit(None)