import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel
from controller import Communicate
from model import Grid
from typing import Tuple
from PyQt5.QtGui import QColor
import time

class Connect4(QWidget):
    def __init__(self):
        super().__init__()
        self.HEIGHT = 6
        self.WIDTH = 7
        self.user_click_enabled = True
        self.communicate = Communicate()
        self.grid = Grid(self.communicate)
        self.communicate.opponent_move.connect(self.updateViewWithOpponentMove)
        self.communicate.game_over.connect(self.displayGameOverMessage)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Connect 4')
        self.setGeometry(100, 100, 400, 400)

        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)

        self.win_label = QLabel('You win!')
        self.lose_label = QLabel('You lose :(')

        self.buttons = []
        self.createButtons()

        # Connect signal for opponent's move
        self.communicate.opponent_move.connect(self.updateViewWithOpponentMove)

    def createButtons(self):
        for row in range(self.HEIGHT)[::-1]:
            row_buttons = []
            for col in range(self.WIDTH):
                button = QPushButton('')
                button.setStyleSheet("background-color: white")
                # update the color of the selected button
                button.clicked.connect(lambda state, row=row, col=col: self.buttonClicked(row, col))
                self.gridLayout.addWidget(button, row+1, col)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def buttonClicked(self, row, col):
        change_made = False
        if not self.user_click_enabled:
            return  # Do nothing if user clicks are disabled
        # Change color of the clicked button
        for row in range(self.HEIGHT):
            button = self.buttons[row][col]
            if button.styleSheet() == "background-color: white":
                button.setStyleSheet("background-color: yellow")
                change_made = True
                break

        if change_made:
            self.communicate.user_move.emit(row, col)

    def updateViewWithOpponentMove(self, row: int, col: int):
        if row is None or col is None:
            return
        button = self.buttons[row][col]
        if button.styleSheet() == "background-color: white":
            button.setStyleSheet("background-color: red")

    def displayGameOverMessage(self, winner: str):
        if winner is None:
            return
        if winner == 'Y':
            self.gridLayout.addWidget(self.win_label, 0, 0, 1, self.WIDTH)
            self.user_click_enabled = False
        if winner == 'R':
            self.gridLayout.addWidget(self.lose_label, 0, 0, 1, self.WIDTH)
            self.user_click_enabled = False



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Connect4()
    window.show()
    sys.exit(app.exec_())

