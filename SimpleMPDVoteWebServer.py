
import time
import sys
if sys.version_info < (3, 0, 0):
    from BaseHTTPServer import HTTPServer as BaseHTTPServer
    import SimpleHTTPServer as HTTPServer
else:
    import http.server as HTTPServer
from BallotServer import BallotServer
import urllib
import QtTrayMenu
import threading


# Host name, for localhost leave name empty
#VOTE_HOST_NAME = '192.168.178.44'
VOTE_HOST_NAME = ''
VOTE_PORT_NUMBER = 6601
MPD_HOST = "Kellerbar-Desktop.fritz.box"
MPD_PORT = 6600

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404

class VoteHandler(HTTPServer.SimpleHTTPRequestHandler):

    def make_header(s, response=HTTP_NOT_FOUND, content_type="text/html"):
        s.send_response(response)
        s.send_header("Content-type", content_type)
        s.end_headers()

    def do_HEAD(s):
        s.make_header(HTTP_OK, "text/html")

    """Respond to a GET request."""
    def do_GET(s):
        def get_song_id(path):
            song_id_str = path.replace("/vote/", "")
            return int(float(song_id_str))

        """http API"""
        """return playlist as json """
        if s.path.startswith("/playlist.json"):
            s.make_header(HTTP_OK, "application/json")
            s.wfile.write(bs.getPlaylistAsJson().encode('utf-8'))
            return
            
        """Process a vote with given id """
        if s.path.startswith("/vote/"):
            try:
                song_id = int(float(s.path.replace("/vote/", "")))
                (songIdExists, newPosition) = bs.voteForMpdId(song_id)
                if songIdExists:
                    s.make_header(HTTP_OK, "application/json")
                    s.wfile.write("{{ \"newPosition\": {0} }}".format(newPosition).encode('utf-8'))
                else:
                    s.send_response(HTTP_NOT_FOUND)
            except ValueError:
                s.make_header(HTTP_BAD_REQUEST, "application/json")
            return

        """http API"""
        """return playlist as json """
        if s.path.startswith("/library.json"):
            s.make_header(HTTP_OK, "application/json")
            s.wfile.write(bs.getLibraryAsJson().encode('utf-8'))
            return

        """Process a vote with given id """
        if s.path.startswith("/queue/"):
            try:
                url = s.path.replace("/queue/", "")
                if sys.version_info < (3, 0, 0):
                    song_path=urllib.unquote(url).decode('utf8')
                else:
                    song_path=urllib.parser.unquote(url, encoding='utf-8')

                bs.queueSong(song_path)
                s.make_header(HTTP_OK, "application/json")
                s.wfile.write("<body>".encode('utf-8'))
                s.wfile.write("<p>You queued: {0}</p>".format(song_path).encode('utf-8'))
                s.wfile.write("</body></html>".encode('utf-8'))
            except ValueError:
                s.make_header(HTTP_BAD_REQUEST, "application/json")
            return

        """As default let SimpleHTTPServer look for the file. """
        HTTPServer.SimpleHTTPRequestHandler.do_GET(s)
        return

class SimpleMPDVoteWebServer():
    def close(self):
        self.httpd.shutdown()
        print ("{0} Server Stops - {1}:{2}".format(time.asctime(), VOTE_HOST_NAME, VOTE_PORT_NUMBER))

    def run(self):
        if sys.version_info < (3, 0, 0):
            server_class = BaseHTTPServer
        else:
            server_class = HTTPServer.HTTPServer
        self.httpd = server_class((VOTE_HOST_NAME, VOTE_PORT_NUMBER), VoteHandler)
        print ("{0} Server Starts - {1}:{2}".format(time.asctime(), VOTE_HOST_NAME, VOTE_PORT_NUMBER))
        self.httpd.serve_forever(poll_interval=0.5)

if __name__ == '__main__':

    bs = BallotServer(MPD_HOST, MPD_PORT)
    httpd = SimpleMPDVoteWebServer()

    httpd_th = threading.Thread(target=httpd.run).start()

    stm = QtTrayMenu.SystemTrayIcon()
    # start main loop
    stm.run()

    httpd.close()
