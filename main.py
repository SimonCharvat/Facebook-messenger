
# TODO:
# - Add docstrings
# - Detect new notifications
# - Set icon for task bar
# - Keep app running in tray (refactor/fix closeEvent function)
# - Show notifications in system tray and taks bar icon
# - Allow option to be kept logged in even after closing
# - Export app as compiled/installable software

# Standard libraries
import sys

# Third-party libraries
from PyQt6 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets

# Local modules
pass

MESSENGER_URL = "https://www.facebook.com/messages"

class MessengerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Messenger")
        self.resize(1000, 720)

        # Web view
        self.webview = QtWebEngineWidgets.QWebEngineView()
        self.webview.setUrl(QtCore.QUrl(MESSENGER_URL))
        self.setCentralWidget(self.webview)

        # System tray
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        icon = QtGui.QIcon("icon.ico")
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("Messenger")

        # Tray menu
        tray_menu = QtWidgets.QMenu()
        open_action = tray_menu.addAction("Open Messenger")
        open_action.triggered.connect(self.show_window)
        tray_menu.addSeparator()
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(QtWidgets.QApplication.quit)
        self.tray_icon.setContextMenu(tray_menu)

        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

        # Notification for first run
        self.tray_icon.showMessage("Messenger", "Running in system tray.", QtWidgets.QSystemTrayIcon.MessageIcon.Information, 3000)

    def closeEvent(self, event):
        """Hide window instead of closing, keep app running in tray."""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("Messenger", "Still running in tray.", QtWidgets.QSystemTrayIcon.MessageIcon.NoIcon, 2000)

    def show_window(self):
        self.show()
        self.activateWindow()

    def on_tray_activated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger:
            if self.isHidden():
                self.show_window()
            else:
                self.hide()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MessengerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
