from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt


class SideBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border-right: 1px solid #d0d0d0;
            }
        """)
        self.setFixedWidth(250)  
        self.move(-250, 0)  

        sidebar_layout = QVBoxLayout(self)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sidebar_layout.setSpacing(20)