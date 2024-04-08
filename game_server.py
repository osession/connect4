import sys


def main():
    # Your code to initialize the game or any other setup

    while True:
        # Get the input from the command line
        user_input = input("Enter your move: ")

        # Process the input or perform any necessary validation
        # For example, if you're playing Connect Four, you might validate that the input is a valid column number

        # Your logic to handle the user's move
        # For example, update the game state and print the updated board

        # Break the loop if a certain condition is met, such as reaching the end of the game
        # For example, if someone wins or if the user decides to quit

        # Alternatively, you can exit the loop by typing a specific command, such as "quit"
        if user_input.lower() == "quit":
            break


if __name__ == "__main__":
    main()