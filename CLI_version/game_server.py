import time
from grid import Grid


def main():
    # Your code to initialize the game or any other setup
    game_grid = Grid()
    while True:
        # Get the input from the command line and validate
        user_input = input("Enter your move (a number from 1 to 7): ")
        if user_input.lower() == "quit":
            break
        valid_moves = game_grid.getValidMoves()
        if not user_input.isdigit() or len(user_input) > 1 or int(user_input) not in valid_moves:
            print('Invalid input. Please try again.')
            continue

        # update the grid with the user's input
        move = f'COL{user_input}'
        game_grid.updateGridWithUserMove(move)
        for row in game_grid.grid[::-1]:
            print(''.join(row))
        time.sleep(1)

        # check to see if the game is over
        isGameOver = game_grid.checkIfGameOver()
        if isGameOver:
            print('YOU WON THE GAME! :)')
            break

        # make opponent move (by the agent using minimax alphabeta pruning and heuristic function)
        game_grid.makeRandomOpponentMove()
        for row in game_grid.grid[::-1]:
            print(''.join(row))

        # check to see if the game is over
        isGameOver = game_grid.checkIfGameOver()
        if isGameOver:
            print('YOU LOST THE GAME :(')
            break


if __name__ == "__main__":
    main()
