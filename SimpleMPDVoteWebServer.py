import time
import sys
if sys.version_info < (3, 0, 0):
    from BaseHTTPServer import HTTPServer as BaseHTTPServer
    import SimpleHTTPServer as HTTPServer
else:
    import http.server as HTTPServer
from BallotServer import BallotServer
import urllib


# Host name, for localhost leave name empty
VOTE_HOST_NAME = ''
VOTE_PORT_NUMBER = 6601
MPD_HOST = "Kellerbar-Desktop.fritz.box"
MPD_PORT = 6600

HTML_OK = 200
HTML_BAD_REQUEST = 400
HTML_NOT_FOUND = 404

class VoteHandler(HTTPServer.SimpleHTTPRequestHandler):

    def make_header(s, response=HTML_NOT_FOUND, content_type="text/html"):
        s.send_response(response)
        s.send_header("Content-type", content_type)
        s.end_headers()

    def do_HEAD(s):
        s.make_header(HTML_OK, "text/html")

    """Respond to a GET request."""
    def do_GET(s):
        def get_song_id(path):
            song_id_str = path.replace("/vote/", "")
            return int(float(song_id_str))

        """http API"""
        """return playlist as json """
        if s.path.startswith("/playlist.json"):
            s.make_header(HTML_OK, "application/json")
            s.wfile.write(bs.getPlaylistAsJson().encode('utf-8'))
            return
            
        """Process a vote with given id """
        if s.path.startswith("/vote/"):
            try:
                song_id = int(float(s.path.replace("/vote/", "")))
                bs.voteForMpdId(song_id)
                s.make_header(HTML_OK, "application/json")
                s.wfile.write("<body>".encode('utf-8'))
                s.wfile.write("<p>You voted: {0}</p>".format(song_id).encode('utf-8'))
                s.wfile.write("</body></html>".encode('utf-8'))
            except ValueError:
                s.make_header(HTML_BAD_REQUEST, "application/json")
            return

        """http API"""
        """return playlist as json """
        if s.path.startswith("/library.json"):
            s.make_header(HTML_OK, "application/json")
            s.wfile.write(bs.getLibraryAsJson().encode('utf-8'))
            return

        """Process a vote with given id """
        if s.path.startswith("/queue/"):
            try:
                url = s.path.replace("/queue/", "")
                song_path=urllib.unquote(url).decode('utf8') 
                bs.queueSong(song_path)
                s.make_header(HTML_OK, "application/json")
                s.wfile.write("<body>".encode('utf-8'))
                s.wfile.write("<p>You queued: {0}</p>".format(song_path).encode('utf-8'))
                s.wfile.write("</body></html>".encode('utf-8'))
            except ValueError:
                s.make_header(HTML_BAD_REQUEST, "application/json")
            return

        """As default let SimpleHTTPServer look for the file. """
        HTTPServer.SimpleHTTPRequestHandler.do_GET(s)
        return


if __name__ == '__main__':

    if sys.version_info < (3, 0, 0):
        server_class = BaseHTTPServer
    else:
        server_class = HTTPServer.HTTPServer
    httpd = server_class((VOTE_HOST_NAME, VOTE_PORT_NUMBER), VoteHandler)
    print ("{0} Server Starts - {1}:{2}".format(time.asctime(), VOTE_HOST_NAME, VOTE_PORT_NUMBER))
    
    bs = BallotServer(MPD_HOST, MPD_PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print ("{0} Server Stops - {1}:{2}".format(time.asctime(), VOTE_HOST_NAME, VOTE_PORT_NUMBER))
