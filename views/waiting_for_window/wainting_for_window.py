import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore


class WaitingForWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Күту зонасы")
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setGeometry(50, 50, 1850, 950)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0c1214;
                border: thick double #32a1ce;
                border-radius: 20px;
            }
        """)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        loading_layout = QVBoxLayout(self.central_widget)
        loading_layout.setContentsMargins(10, 10, 10, 800)

        self.loading_label = QLabel(self.central_widget)
        self.loading_gif_path = "images/ZZ5H.gif"
        self.loading_gif = QtGui.QMovie(self.loading_gif_path)
        if not self.loading_gif.isValid():
            self.loading_label.setText("Ошибка: GIF не найден или поврежден")
        else:
            self.loading_gif.setScaledSize(QtCore.QSize(100, 100))
            self.loading_label.setMovie(self.loading_gif)
            self.loading_gif.start()

        self.loading_label.setAlignment(Qt.AlignCenter)
        
        loading_layout.addWidget(self.loading_label)
        loading_layout.setAlignment(Qt.AlignCenter)  

if __name__ == "__main__":
    app = QApplication(sys.argv)      
    window = WaitingForWindow()
    window.show()
    sys.exit(app.exec())