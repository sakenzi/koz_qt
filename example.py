import sys
from PyQt5.QtWidgets import (QApplication ,QWidget, QPushButton,
                             QComboBox, QGridLayout, QLabel)
from PyQt5.QtCore    import QSize, Qt, pyqtSlot, QTranslator, QEvent

class MainWindow(QWidget):
    def __init__(self, chooseLang, parent=None):
        super().__init__(parent)
        self.chooseLang = chooseLang

        self.initUI()

    def initUI(self):
        self.resize(550, 370)

        self.combo = QComboBox()
        self.combo.currentIndexChanged.connect(self.unit_choice)

        self.label = QLabel(alignment=Qt.AlignCenter)

        self.but1 = QPushButton(self, minimumSize=QSize(140, 50))
        self.but2 = QPushButton(self, minimumSize=QSize(140, 50))
        self.but3 = QPushButton(self, minimumSize=QSize(140, 50))
        self.but4 = QPushButton(self, minimumSize=QSize(140, 50))

        self.trans = QTranslator(self)

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.combo, 0, 1, alignment=Qt.AlignRight)
        self.grid.setRowStretch(1, 1)
        self.grid.addWidget(self.label, 2, 0, 1, 2, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.but1,  3, 0, alignment=Qt.AlignLeft)
        self.grid.addWidget(self.but2,  4, 0, alignment=Qt.AlignLeft)
        self.grid.addWidget(self.but3,  5, 0, alignment=Qt.AlignLeft)
        self.grid.addWidget(self.but4,  6, 0, alignment=Qt.AlignLeft)
        self.grid.setRowStretch(7, 1)

        options = ([('English',   ''), 
                    ('Italian',   'eng-it' ), 
                    ('Russian',   'eng-ru'), 
                    ('Ukrainian', 'eng-uk'),])

        for i, (text, lang) in enumerate(options):
            self.combo.addItem(text)
            self.combo.setItemData(i, lang)
        self.retranslateUi()

    @pyqtSlot(int)
    def unit_choice(self, index):
        data = self.combo.itemData(index)
        if data:
            self.trans.load(data)
            QApplication.instance().installTranslator(self.trans)
        else:
            QApplication.instance().removeTranslator(self.trans)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        super(MainWindow, self).changeEvent(event)

    def retranslateUi(self):
        self.setWindowTitle(QApplication.translate('MainWindow', 'Product calculation'))
        self.but1.setText(QApplication.translate('MainWindow',  'Create calculation'))
        self.but2.setText(QApplication.translate('MainWindow',  'Search a calculation'))
        self.but3.setText(QApplication.translate('MainWindow',  'Settings'))
        self.but4.setText(QApplication.translate('MainWindow',  'About program'))
        self.label.setText(QApplication.translate('MainWindow', 'Hello, World'))


ChooseLang = ["English", "Italian", "Russian", "Ukrainian"]

if __name__== '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(ChooseLang)
    window.show()
    sys.exit(app.exec_())