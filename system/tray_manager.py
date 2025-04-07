from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QAction
from PyQt5.QtGui import QIcon


class TrayManager:
    def __init__(self, parent):
        self.parent = parent

        self.tray_icon = QSystemTrayIcon(parent)
        self.tray_icon.setIcon(QIcon('icons/11003355.png'))

        self.setup_tray()

    def setup_tray(self):
        tray_menu = QMenu()
        show_action = QAction("Көрсету", self.parent)
        quit_action = QAction("Шығу", self.parent)
        show_action.triggered.connect(self.parent.show)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_clicked)

    def tray_clicked(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.parent.show()

    def quit_app(self):
        self.parent.logs.stop()
        QApplication.quit()

    
