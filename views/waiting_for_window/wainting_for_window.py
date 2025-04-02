import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5 import QtGui


class WaitingForWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Күту зонасы")
        self.setGeometry(50, 50, 1850, 950)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0c1214;
                border: thick double #32a1ce;
                border-radius: 20px;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.loading_label = QLabel(self.central_widget)
        self.loading_gif_path = ("images/ZZ5H.gif")
        self.loading_gif = QtGui.QMovie(self.loading_gif_path)
        if not self.loading_gif.isValid():
            self.loading_label.setText("Ошибка: GIF не найден или поврежден")
        else:
            self.loading_label.setMovie(self.loading_gif)
            self.loading_gif.start()

        self.loading_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.loading_label)

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.close)
        # self.timer.start(5000)

app = QApplication(sys.argv)      

window = WaitingForWindow()
window.show()

app.exec()