import urllib
import threading
import signal

import QtTrayMenu
from BallotServer import BallotServer
import SimpleMPDVoteWebServer as WebServer 

# Host name, for localhost leave name empty
VOTE_HOST_NAME = ''
VOTE_PORT_NUMBER = 6601
MPD_HOST = "leifs-air"
MPD_PORT = 6600


class SimpleMPDVoteApp():

    mpd_host = MPD_HOST
    mpd_port = MPD_PORT
    web_host = VOTE_HOST_NAME
    web_port = VOTE_PORT_NUMBER
    bs = None
    httpd = None
    stm = None

    def connect_mpd(self):
        try:
            self.bs = BallotServer(self.mpd_host, self.mpd_port)
            print ("Connect to MPD at {0}:{1}".format(self.mpd_host, self.mpd_port))
        except:
            print ("Could not connect to MPD at {0}:{1}".format(self.mpd_host, self.mpd_port))

    def start_web_server(self):
        self.httpd_th = threading.Thread(target=self.httpd.run, args=(self.web_host, self.web_port, self.bs))
        self.httpd_th.start()

    def stop_web_server(self):
        th_q = threading.Thread(target=self.httpd.close)
        th_q.start()
        th_q.join()

    def __init__(self):
        self.stm = QtTrayMenu.SystemTrayIcon()
        self.connect_mpd()
        self.httpd = WebServer.SimpleMPDVoteWebServer()

    def run(self):
        self.start_web_server();
        self.stm.run(self)

    def quit(self):
        if self.bs:
            self.bs.close()
        self.stop_web_server()
        self.stm.exit()

if __name__ == '__main__':

    # catch ctrl-c signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = SimpleMPDVoteApp() 

    # start main loop
    app.run()

