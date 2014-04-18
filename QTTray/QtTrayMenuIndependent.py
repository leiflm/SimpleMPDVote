from PyQt4.QtCore import SIGNAL, QCoreApplication
from PyQt4.QtNetwork import QHttp
from PyQt4.QtGui import QApplication, QWidget, QIcon, QMenu, QSystemTrayIcon
import sys

HOSTNAME = 'localhost'
PORT     = 8080

class VoteServerTrayIcon(QSystemTrayIcon):
    voting_enabled = True
    def __init__(self, app, parent=None):
        QSystemTrayIcon.__init__(self, parent)
        self.app = app
        self.vote_server_request = QHttp(HOSTNAME, PORT, self)
        self.setIcon(QIcon("voting-active.png"))
        self.get_status()

        self.menu = QMenu(parent)
        exitAction = self.menu.addAction("Close Tray Icon")
        self.connect(exitAction, SIGNAL('triggered()'), self.exit)
        self.setContextMenu(self.menu)

        self.activated.connect(self.click_trap)

    def click_trap(self, value):
        if value == self.Trigger: #left click!
            if self.voting_enabled:
                self.deactivate()
            else:
                self.activate()

    def get_status(self):
        self.vote_server_request.get("/vote/status")
        self.connect(self.vote_server_request, SIGNAL("requestFinished(int, bool)"), self.status_cb)

    def status_cb(self, requestId, error):
        if error:
            print "Failed to query the voting server's status. Is it even running on this host?!"
            return
        resp_data = self.vote_server_request.readAll()
        print resp_data
        if resp_data == "True":
            self.voting_enabled = True
        else:
            self.voting_enabled = False
        self.update_ui()

    def activate(self):
        self.vote_server_request.get("/vote/activate")
        self.connect(self.vote_server_request, SIGNAL("requestFinished(int, bool)"), self.activated_cb)

    def activated_cb(self, requestId, error):
        if error:
            print "Failed to activate the voting server. Is it even running on this host?!"
            return
        self.voting_enabled = True
        self.update_ui()

    def deactivate(self):
        self.vote_server_request.get("/vote/deactivate")
        self.connect(self.vote_server_request, SIGNAL("requestFinished(int, bool)"), self.deactivated_cb)

    def deactivated_cb(self, requestId, error):
        if error:
            print "Failed to deactivate the voting server. Is it even running on this host?!"
            return
        self.voting_enabled = False
        self.update_ui()

    def update_ui(self):
        if self.voting_enabled:
            self.setIcon(QIcon("voting-active.png"))
        else:
            self.setIcon(QIcon("voting-inactive.png"))

    def exit(self):
        return self.app.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tray = VoteServerTrayIcon(app)
    tray.show()
    sys.exit(app.exec_())