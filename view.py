import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
from controller import Communicate
from model import Grid
from typing import Tuple
from PyQt5.QtGui import QColor

class Connect4(QWidget):
    def __init__(self):
        super().__init__()
        self.HEIGHT = 6
        self.WIDTH = 7
        self.user_click_enabled = True
        self.communicate = Communicate()
        self.grid = Grid(self.communicate)
        self.communicate.opponent_move.connect(self.updateViewWithOpponentMove)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Connect 4')
        self.setGeometry(100, 100, 400, 400)

        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)

        self.buttons = []
        self.createButtons()

        # Connect signal for opponent's move
        self.communicate.opponent_move.connect(self.updateViewWithOpponentMove)

    def createButtons(self):
        for row in range(self.HEIGHT):
            row_buttons = []
            for col in range(self.WIDTH):
                button = QPushButton('')
                button.setStyleSheet("background-color: white")
                # update the color of the selected button
                button.clicked.connect(lambda state, row=row, col=col: self.buttonClicked(row, col))
                self.gridLayout.addWidget(button, row, col)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def buttonClicked(self, row, col):
        if not self.user_click_enabled:
            return  # Do nothing if user clicks are disabled
        # Change color of the clicked button
        for row in range(self.HEIGHT)[::-1]:
            button = self.buttons[row][col]
            if button.styleSheet() == "background-color: white":
                button.setStyleSheet("background-color: yellow")
                break

        self.user_click_enabled = False
        # Make opponent's move (you need to implement this part)
        # self.makeOpponentMove()  # Placeholder for making opponent's move
        # Enable user clicks after opponent's move is made
        self.user_click_enabled = True
        self.communicate.user_move.emit(row, col)

    def updateViewWithOpponentMove(self, row: int, col: int):
        button = self.buttons[row][col]
        if button.styleSheet() == "background-color: white":
            button.setStyleSheet("background-color: red")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Connect4()
    window.show()
    sys.exit(app.exec_())
