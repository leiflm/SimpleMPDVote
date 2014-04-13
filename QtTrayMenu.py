from PyQt4 import (QtGui, QtCore)
import sys

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
        menu = QtGui.QMenu(parent)
        otherAction = menu.addAction("other")
        exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)
        self.connect(exitAction, QtCore.SIGNAL('triggered()'), self.exit)
        self.connect(otherAction, QtCore.SIGNAL('triggered()'), self.other)
        self.menu = menu

    def run(self):
        self.show()
        self.app.exec_()

