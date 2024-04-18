from PyQt5.QtCore import pyqtSignal, QObject

class Communicate(QObject):
    user_move = pyqtSignal(int, int)  # Signal to emit user's move
    opponent_move = pyqtSignal(int, int)   # Signal to emit opponent's move
    game_over = pyqtSignal(str)