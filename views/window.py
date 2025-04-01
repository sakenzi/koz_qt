import sys
from PyQt5.QtCore import QPropertyAnimation, QPoint, QSequentialAnimationGroup
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 300)
        self.setStyleSheet("background-color: #F5F5F5;")

        self.blue_widget = QWidget(self)
        self.blue_widget.resize(200, 300)
        self.blue_widget.setStyleSheet("background-color: #D3D3D3;")
        self.blue_widget.move(-200, 0)

        self.button = QPushButton("Toggle", self)
        self.button.setGeometry(10, 10, 80, 30)
        self.button.clicked.connect(self.toggle_blue_widget)

    def toggle_blue_widget(self):
        anim_group = QSequentialAnimationGroup(self)

        if self.blue_widget.x() < 0:
            anim = QPropertyAnimation(self.blue_widget, b"pos")
            anim.setDuration(200)
            anim.setStartValue(QPoint(-200, 0))
            anim.setEndValue(QPoint(0, 0))
            anim_group.addAnimation(anim)
        else:
            anim = QPropertyAnimation(self.blue_widget, b"pos")
            anim.setDuration(200)
            anim.setStartValue(QPoint(0, 0))
            anim.setEndValue(QPoint(-200, 0))
            anim_group.addAnimation(anim)

        anim_group.start(QPropertyAnimation.DeleteWhenStopped)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())