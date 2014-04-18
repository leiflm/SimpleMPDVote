from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QApplication, QWidget, QSystemTrayIcon, QMenu, QIcon
import sys
import SimpleMPDVoteMain

class SystemTrayIcon(QSystemTrayIcon):

    def exit(self):

        return self.app.exit(0)

    def other(self):
        print("other")
        return 0

    def __init__(self, parent=None):
        self.app = QApplication(sys.argv)
        self.w = QWidget()
        self.icon = QIcon("img/ionic.png")
        self.trayIcon = QSystemTrayIcon.__init__(self, self.icon, self.w)
        self.menu = QMenu(parent)

        mpdStatus = self.menu.addAction("Disconnected")

        otherAction = self.menu.addAction("other")
        self.connect(otherAction, SIGNAL('triggered()'), self.other)
        exitAction = self.menu.addAction("Exit")
        self.setContextMenu(self.menu)
        self.connect(exitAction, SIGNAL('triggered()'), self.exit)

    def run(self, app):
        self.connect(self.app, SIGNAL('aboutToQuit()'),  app.quit)
        self.show()
        self.app.exec_()

