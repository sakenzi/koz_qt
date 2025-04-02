import sys
from PyQt5.QtCore import QPropertyAnimation, QPoint, QSequentialAnimationGroup
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt, QPoint, QSequentialAnimationGroup, QPropertyAnimation, QAbstractAnimation
import time


class TimerLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        
        self.setFixedSize(200, 50)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #343c42;
                color: white;
                border-radius: 15px;
                padding: 12px;
                font-size: 16px;
                border: none;
            }
            QLabel: hover {
                background-color: #195c1c;
            }
            QLabel: pressed {
                background-color: #166e1a;
            }
        """)

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1000, 1000)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #343c42;
                color: white;
                border-radius: 15px;
                padding: 12px;
                font-size: 16px;
                border: none;
            }
            QLabel: hover {
                background-color: #195c1c;
            }
            QLabel: pressed {
                background-color: #166e1a; 
            }
        """)

class ExamWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Экзамен алаңы")
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

        self.blue_widget = QWidget(self)
        self.blue_widget.resize(700, 1300)
        self.blue_widget.setStyleSheet("background-color: #252c30;")
        self.blue_widget.move(-700, -700)

        self.total_time = 200
        self.start_time = time.time()

        self.timer_label = TimerLabel(f"Тайминг: {self.total_time // 60}:{self.total_time % 60:02d}", self.central_widget)
        self.timer_label.move(230, 10)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        self.sidebar_button = QPushButton(" Тапсырмалар", self)
        self.sidebar_button.setIcon(QIcon('icons/show-sidebar-horiz.svg'))
        self.sidebar_button.setGeometry(10, 10, 200, 50)
        self.sidebar_button.setStyleSheet("""
            QPushButton {
                background-color: #343c42;
                color: white;
                border-radius: 15px;
                padding: 12px;
                font-size: 16px;
                border: none;
            }
            QPushButton: hover {
                background-color: #195c1c;
            }
            QPushButton: pressed {
                background-color: #166e1a;
            }
        """)
        self.sidebar_button.clicked.connect(self.sidebar_blue_widget)

    def sidebar_blue_widget(self):
        anim_group = QSequentialAnimationGroup(self)

        if self.blue_widget.x() < 0:
            anim = QPropertyAnimation(self.blue_widget, b"pos")
            anim.setDuration(700)
            anim.setStartValue(QPoint(-700, 0))
            anim.setEndValue(QPoint(0, 0))
            anim_group.addAnimation(anim)
        else:
            anim = QPropertyAnimation(self.blue_widget, b"pos")
            anim.setDuration(700)
            anim.setStartValue(QPoint(0, 0))
            anim.setEndValue(QPoint(-700, 0))
            anim_group.addAnimation(anim)

        anim_group.start(QPropertyAnimation.DeleteWhenStopped)

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        remaining_time = self.total_time - elapsed
        if remaining_time >= 0:
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            self.timer_label.setText(f"Тайминг: {minutes}:{seconds:02d}")
        else:
            self.timer_label.setText("Тайминг: 0:00")
            self.timer.stop()


app = QApplication(sys.argv)
window = ExamWindow()
window.show()
app.exec()