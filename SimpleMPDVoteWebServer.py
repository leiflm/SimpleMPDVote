import time
import sys
if sys.version_info < (3, 0, 0):
    from BaseHTTPServer import HTTPServer as BaseHTTPServer
    import SimpleHTTPServer as HTTPServer
else:
    import http.server as HTTPServer
from BallotServer import BallotServer


# Host name, for localhost leave name empty
VOTE_HOST_NAME = ''
VOTE_PORT_NUMBER = 6601

class VoteHandler(HTTPServer.SimpleHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    """Respond to a GET request."""
    def do_GET(s):
        def make_header(s, response=404):
            s.send_response(response)
            s.send_header("Content-type", "text/html")
            s.end_headers()

        def make_html_title(s):
            s.wfile.write("<html><head><title>Vote for Songs.</title></head>".encode('utf-8'))
            
        """Send file content of path"""
        def send_file(s, fpath):
            try:
                f = open(fpath)
                make_header(s, 200)
                for line in f:
                    s.wfile.write(line.encode('utf-8'))
                f.close
            except IOError:
                make_header(s, 404)
                make_html_title(s)
                s.wfile.write("<body><p>404 Not found.</p></body></html>".encode('utf-8'))
            return

        def get_song_id(path):
            song_id_str = path.replace("/vote/", "")
            return int(float(song_id_str))

        """http API"""

        """return playlist as json """
        if s.path.startswith("/playlist.json"):
            s.send_response(200)
            s.send_header("Content-type", "application/json")
            s.end_headers()
            s.wfile.write(bs.getPlaylistAsJson().encode('utf-8'))
            return
            
        """Process a vote with given id """
        if s.path.startswith("/vote/"):
            try:
                song_id = int(float(s.path.replace("/vote/", "")))
                bs.voteForMpdId(song_id)

                make_header(s, 200)
                make_html_title(s)
                s.wfile.write("<body>".encode('utf-8'))
                s.wfile.write("<p>You voted: {0}</p>".format(song_id).encode('utf-8'))
                s.wfile.write("</body></html>".encode('utf-8'))
            except ValueError:
                make_header(s, 400)

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
    
    bs = BallotServer()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print ("{0} Server Stops - {1}:{2}".format(time.asctime(), VOTE_HOST_NAME, VOTE_PORT_NUMBER))
