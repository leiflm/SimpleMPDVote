from PyQt4 import (QtGui, QtCore)
import sys
import SimpleMPDVoteMain

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def exit(self):

        return self.app.exit(0)

    def other(self):
        print("other")
        return 0

    def __init__(self, parent=None):
        self.app = QtGui.QApplication(sys.argv)
        self.w = QtGui.QWidget()
        self.icon = QtGui.QIcon("img/ionic.png")
        self.trayIcon = QtGui.QSystemTrayIcon.__init__(self, self.icon, self.w)
        self.menu = QtGui.QMenu(parent)

        mpdStatus = self.menu.addAction("Disconnected")

        otherAction = self.menu.addAction("other")
        self.connect(otherAction, QtCore.SIGNAL('triggered()'), self.other)
        exitAction = self.menu.addAction("Exit")
        self.setContextMenu(self.menu)
        self.connect(exitAction, QtCore.SIGNAL('triggered()'), self.exit)

    def run(self, app):
        self.connect(self.app, QtCore.SIGNAL('aboutToQuit()'),  app.quit)
        self.show()
        self.app.exec_()

