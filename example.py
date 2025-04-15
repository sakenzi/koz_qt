from PyQt5 import QtCore, QtGui, QtWidgets

class CustomButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(15, 21)
        
        self.color_1 = "65,69,245"
        self.opacity_1 = 50
        self.opacity_1a = 170
        
        self.color_2 = "172,174,251"
        self.opacity_2 = 40
        self.opacity_2a = 100

        self.anim_1 = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate_1,
            startValue=self.opacity_1,
            endValue=self.opacity_1a,
            duration=175
            )

        self.anim_2 = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate_2,
            startValue=self.opacity_2,
            endValue=self.opacity_2a,
            duration=175
            )

        self.anim_group = QtCore.QParallelAnimationGroup()
        self.anim_group.addAnimation(self.anim_1)
        self.anim_group.addAnimation(self.anim_2)

    def _animate_1(self, value):
        self.opa_1_prog = value

    def _animate_2(self,value):
        qss = """
            font: 9;
            color: rgb(255, 255, 255);
            border: none;
            border-radius: 8px;
        """
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba({color_1}, {opacity_1}),stop: 1.0 rgba({color_2},{opacity_2}));".format(
            opacity_1=int(self.opa_1_prog), color_1=self.color_1, opacity_2=int(value), color_2 = self.color_2
            )
        #print(grad)
        qss += grad
        self.setStyleSheet(qss)

    def enterEvent(self, event):
        self.anim_group.setDirection(QtCore.QAbstractAnimation.Forward)
        self.anim_group.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim_group.setDirection(QtCore.QAbstractAnimation.Backward)
        self.anim_group.start()
        super().enterEvent(event)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window_container = QtWidgets.QWidget()
    window_container.setWindowTitle("Buttons")
    window_container.setMinimumSize(200,125)

    button_container = QtWidgets.QWidget()
    button_container.setObjectName("button_container")

    Button_1 = CustomButton()
    Button_2 = CustomButton()

    button_layout = QtWidgets.QVBoxLayout()
    button_layout.addWidget(Button_1)
    button_layout.addWidget(Button_2)

    button_container.setLayout(button_layout)

    window_layout = QtWidgets.QHBoxLayout()
    window_container.setLayout(window_layout)

    Spacing_1 = QtWidgets.QSpacerItem(25,25)

    window_layout.addItem(Spacing_1)
    window_layout.addWidget(button_container)
    window_layout.addItem(Spacing_1)

    window_container.show()
    sys.exit(app.exec_())