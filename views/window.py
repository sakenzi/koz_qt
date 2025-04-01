import sys
from PyQt5.QtCore import QPropertyAnimation, QPoint, QSequentialAnimationGroup
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt, QPoint, QSequentialAnimationGroup, QPropertyAnimation, QAbstractAnimation


# class TimerLabel(QLabel):
#     def __init__(self, text):
#         super().__init__(text)
        
#         self.setFixedSize(200, 50)
#         self.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.setStyleSheet("""
#             QLabel {
#                 background-color: #FFFFFF;
#                 padding: 10px;
#                 border-radius: 8px;
#                 border: 1px solid #E0E0E0;
#                 font-size: 16px;
#                 color: #333333;
#             }
#         """)

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

        self.blue_widget = QWidget(self)
        self.blue_widget.resize(700, 1300)
        self.blue_widget.setStyleSheet("background-color: #252c30;")
        self.blue_widget.move(-700, -700)

        self.sidebar_button = QPushButton(" Тапсырмалар", self)
        self.sidebar_button.setIcon(QIcon('exam_window/icons/show-sidebar-horiz.svg'))
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


app = QApplication(sys.argv)
window = ExamWindow()
window.show()
app.exec()
