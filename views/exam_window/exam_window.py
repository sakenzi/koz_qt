from PyQt6.QtWidgets import (QVBoxLayout, QWidget, QLabel, QLineEdit, QApplication, 
                             QPushButton, QMainWindow, QHBoxLayout)
from PyQt6.QtCore import QTimer, Qt, QPoint, QSequentialAnimationGroup, QPropertyAnimation
import sys
import time
from system.timer import update_reverse_timer
from system.sidebar import SideBarWidget


class TimerLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        
        self.setFixedSize(200, 50)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #FFFFFF;
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #E0E0E0;
                font-size: 16px;
                color: #333333;
            }
        """)
        # self._dragging = False
        # self._offset = QPoint()

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         self._dragging = True
    #         self._offset = event.pos()

    # def mouseMoveEvent(self, event):
    #     if self._dragging:
    #         self.move(self.mapToParent(event.pos() - self._offset))

    # def mouseReleaseEvent(self, event):
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         self._dragging = False

class ExamWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Экзамен алаңы")
        self.setGeometry(250, 50, 1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #a3c0f0;
                border: thick double #32a1ce;
                border-radius: 20px;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = SideBarWidget(self.central_widget)
        self.main_layout.addWidget(self.sidebar)

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: #ffffff;")
        self.main_layout.addWidget(self.content_widget)

        self.total_time = 200
        self.start_time = time.time()

        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)

        self.reverse_timer_label = TimerLabel(f"Тайминг: {self.total_time // 60}:{self.total_time % 60:02d}")
        self.reverse_timer_label.setParent(self.central_widget)  
        self.reverse_timer_label.move(0, 0)

        self.sidebar_button = QPushButton("sss", self.content_widget)
        self.sidebar_button.setGeometry(10, 60, 80, 30)
        self.sidebar_button.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                padding: 5px;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        self.sidebar_button.clicked.connect(self.button_sidebar)

        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: update_reverse_timer(self))
        self.timer.start(1000)

    def button_sidebar(self):
        anim_group = QSequentialAnimationGroup(self)

        if self.sidebar.x() < 0:  
            anim = QPropertyAnimation(self.sidebar, b"pos")
            anim.setDuration(200)
            anim.setStartValue(QPoint(-250, 0))
            anim.setEndValue(QPoint(0, 0))
            anim_group.addAnimation(anim)
        else:  
            anim = QPropertyAnimation(self.sidebar, b"pos")
            anim.setDuration(200)
            anim.setStartValue(QPoint(0, 0))
            anim.setEndValue(QPoint(-250, 0))
            anim_group.addAnimation(anim)

        anim_group.start(QPropertyAnimation.DeletionPolicy. DeleteWhenStopped)

app = QApplication(sys.argv)

window = ExamWindow()
window.show()

app.exec()