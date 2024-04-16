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
        self.checkIfGameOver()
        # for row in self.grid[::-1]:
        #     print(''.join(row))
        # make opponent move (and update the grid)
        # opponent_row, opponent_col = self.makeRandomOpponentMove()
        _, opponent_col = self.minimax(self.grid)
        print(f'BEST MOVE: {opponent_col}')
        # find the corresponding row and update the grid for the model
        opponent_row = None
        for row in range(self.GRID_HEIGHT):
            if self.grid[row][opponent_col] == ' ':
                self.grid[row][opponent_col] = self.OPPONENT
                opponent_row = row
                break

        self.checkIfGameOver()
        # send the move back to the GUI
        self.communicate.opponent_move.emit(opponent_row, opponent_col)



    def makeStrategicOpponentMove(self) -> None:
        pass

    def minimax(self, state: list, depth: int = 5, maximizing_player=True):
        if depth == 0 or len(self.getValidMoves(state)) == 0:
            if maximizing_player:
                return self.evaluate(state, self.PLAYER), None
            else:
                return self.evaluate(state, self.OPPONENT), None

        valid_moves = self.getValidMoves(state)

        if maximizing_player:
            best_score = float('-inf')
            best_move = None
            for move in valid_moves:
                new_state = self.getNewState(move)
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
                new_state = self.getNewState(move)
                score, _ = self.minimax(new_state, depth - 1, True)
                print(f'minimizing player score: {score}')
                print(f'minimizing player move: {move}')
                if score < best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move

    # def alphaBeta(self, state, depth, alpha=float('-inf'), beta=float('inf'), maximizing_player=True):
    #     if depth == 0 or len(self.getValidMoves(state)) == 0:
    #         return self.evaluate(state), None
    #
    #     valid_moves = self.getValidMoves(state)
    #
    #     if maximizing_player:
    #         best_score = float('-inf')
    #         best_move = None
    #         for move in valid_moves:
    #             new_state = self.getNewState(move)
    #             score, _ = self.alphaBeta(new_state, depth - 1, alpha, beta, False)
    #             print(f'maximizing player score: {score}')
    #             if score > best_score:
    #                 best_score = score
    #                 best_move = move
    #             alpha = max(alpha, score)
    #             if beta <= alpha:
    #                 break
    #         return best_score, best_move
    #     else:
    #         best_score = float('inf')
    #         best_move = None
    #         for move in valid_moves:
    #             new_state = self.getNewState(move)
    #             score, _ = self.alphaBeta(new_state, depth - 1, alpha, beta, True)
    #             print(f'minimizing player score: {score}')
    #             if score < best_score:
    #                 best_score = score
    #                 best_move = move
    #             beta = min(beta, score)
    #             if alpha <= beta:
    #                 break
    #         return best_score, best_move

    def evaluate(self, state: list, player: str):
        # current_player_score = self.evaluate_helper(state, player)
        # current_opponent_score = self.evaluate_helper(state, player)
        # return current_player_score - current_opponent_score
        opponent = self.PLAYER if player == self.OPPONENT else self.OPPONENT
        consecutive_chips_opponent = self.get_consecutive_chips(state, opponent)
        consecutive_chips_player = self.get_consecutive_chips(state, player)
        is_blocking_move: bool = self.get_is_blocked(state, player)

        score = consecutive_chips_player ** 3 - consecutive_chips_opponent ** 3
        if is_blocking_move:
            score += 200
        return score


    def get_consecutive_chips(self, state: list, player: str):
        K = 4  # Number of consecutive chips needed to win
        # eval_value = 0

        max_consecutive = 0

        # Function to check consecutive chips in a line
        def count_consecutive(line):
            max_count = 0
            current_count = 0
            for chip in line:
                if chip == player:
                    current_count += 1
                    max_count = max(max_count, current_count)
                else:
                    current_count = 0
            return max_count

        # Check rows
        for row in state:
            # eval_value += pow(K, count_consecutive(row))
            if count_consecutive(row) > max_consecutive:
                max_consecutive = count_consecutive(row)

        # Check columns
        for j in range(7):
            column = [state[i][j] for i in range(6)]
            # eval_value += pow(K, count_consecutive(column))
            if count_consecutive(column) > max_consecutive:
                max_consecutive = count_consecutive(column)

        # Check diagonals
        for i in range(3):
            for j in range(4):
                diagonal1 = [state[i + k][j + k] for k in range(K)]
                diagonal2 = [state[i + K - k - 1][j + k] for k in range(K)]
                # eval_value += pow(K, count_consecutive(diagonal1))
                # eval_value += pow(K, count_consecutive(diagonal2))
                if count_consecutive(diagonal1) > max_consecutive:
                    max_consecutive = count_consecutive(diagonal1)
                if count_consecutive(diagonal2) > max_consecutive:
                    max_consecutive = count_consecutive(diagonal2)

        return max_consecutive

    def get_is_blocked(self, state: list, player: str) -> bool:
        # returns if the current state will block the user from winning
        opponent = self.OPPONENT if player == self.PLAYER else self.PLAYER

        # figure out how to adjust this code so that if the first token is opponent and the rest are player, is_blocking=True
        # or if the first three are player and the last one is opponent, is_blocking=True
        for col in range(self.GRID_WIDTH):
            for row in range(self.GRID_HEIGHT - 3):
                if (state[row][col] == state[row + 1][col] == state[row + 2][col]) and (state[row][col] == opponent) and (state[row + 3][col] == player):
                    print('BLOCKED VERTICALLY')
                    return True

        # check if game is won horizontally
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH - 3):
                if (state[row][col] == state[row ][col + 1] == state[row][col + 2]) and (state[row][col] == opponent) and (state[row][col + 3] == player):
                    print('BLOCKED VERTICALLY')
                    return True
                if (state[row][col + 1] == state[row ][col + 2] == state[row][col + 3]) and (state[row][col + 1] == opponent) and (state[row][col] == player):
                    print('BLOCKED VERTICALLY')
                    return True

        # check if game is won diagonally (bottom-left to top-right)
        for row in range(self.GRID_HEIGHT - 3):
            for col in range(self.GRID_WIDTH - 3):
                if (state[row][col] == state[row + 1][col+1] == state[row + 2][col+2]) and (state[row][col] == opponent) and (state[row + 3][col+3] == player):
                    print('BLOCKED DIAGONALLY')
                    return True
                if (state[row + 1][col+1] == state[row + 2][col+2] == state[row + 3][col + 3]) and (state[row + 3][col + 3] == opponent) and (state[row][col] == player):
                    print('BLOCKED DIAGONALLY')
                    return True

        # check if game is won diagonally (bottom-right to top-left)
        for row in range(self.GRID_HEIGHT - 3):
            for col in range(3, self.GRID_WIDTH):
                if (state[row][col] == state[row + 1][col-1] == state[row + 2][col-2]) and (state[row][col] == opponent) and (state[row + 3][col-3] == player):
                    print('BLOCKED DIAGONALLY')
                    return True
                if (state[row + 1][col-1] == state[row + 2][col-2] == state[row + 3][col - 3]) and (state[row + 3][col - 3] == opponent) and (state[row][col] == player):
                    print('BLOCKED DIAGONALLY')
                    return True

        return False

    # def evaluate(self, state: list) -> float:
    #     opponent_score = 0
    #     player_score = 0
    #
    #     # Evaluate the score based on horizontal connections
    #     for row in range(self.GRID_HEIGHT):
    #         for col in range(self.GRID_WIDTH - 3):
    #             window = state[row][col:col + 4]
    #             opponent_score += self.evaluateWindow(window, self.OPPONENT)
    #             player_score += self.evaluateWindow(window, self.PLAYER)
    #
    #     # Evaluate the score based on vertical connections
    #     for col in range(self.GRID_WIDTH):
    #         for row in range(self.GRID_HEIGHT - 3):
    #             window = [state[row + i][col] for i in range(4)]
    #             opponent_score += self.evaluateWindow(window, self.OPPONENT)
    #             player_score += self.evaluateWindow(window, self.PLAYER)
    #
    #     # Evaluate the score based on diagonal connections (bottom-left to top-right)
    #     for row in range(self.GRID_HEIGHT - 3):
    #         for col in range(self.GRID_WIDTH - 3):
    #             window = [state[row + i][col + i] for i in range(4)]
    #             opponent_score += self.evaluateWindow(window, self.OPPONENT)
    #             player_score += self.evaluateWindow(window, self.PLAYER)
    #
    #     # Evaluate the score based on diagonal connections (bottom-right to top-left)
    #     for row in range(self.GRID_HEIGHT - 3):
    #         for col in range(3, self.GRID_WIDTH):
    #             window = [state[row + i][col - i] for i in range(4)]
    #             opponent_score += self.evaluateWindow(window, self.OPPONENT)
    #             player_score += self.evaluateWindow(window, self.PLAYER)
    #
    #     return opponent_score - player_score
    #
    # def evaluateWindow(self, window: list, player: str) -> int:
    #     score = 0
    #     opponent = self.OPPONENT if player == self.OPPONENT else self.PLAYER
    #     player = self.PLAYER if player == self.OPPONENT else self.OPPONENT
    #
    #     if window.count(opponent) == 4:
    #         score += 100
    #     elif window.count(opponent) == 3:
    #         score += 5
    #     elif window.count(opponent) == 2:
    #         score += 2
    #
    #     if window.count(player) == 3:
    #         score -= 20
    #     # if window.count(player) == 4:
    #     #     score -= 200
    #
    #     return score

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