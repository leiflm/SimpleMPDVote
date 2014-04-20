from BallotServer import BallotServer
import urllib
import json
import sys
from bottle import Bottle, run, get, request, response, static_file, redirect, abort

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404

class SimpleMPDVoteWebServer():

    def __init__(self):
        self.voting_disabled = False
        self.bs = BallotServer('localhost', 6600)
        self.app = Bottle()
        self.setup_routes()

    def setup_routes(self):
        app = self.app


        @app.get('/browse')
        @app.get('/browse/')
        @app.get('/browse/<path:path>')
        def browsePath(path = '/'):
            if self.voting_disabled:
                abort(HTTP_NOT_FOUND, "Sorry voting is currently disabled!")
            response.content_type = 'application/json'
            if sys.version_info < (3, 0, 0):
                path=urllib.unquote(path).decode('utf8')
            else:
                path=urllib.parser.unquote(path, encoding='utf-8')
            listing = self.bs.getLsInfo(path)
            return json.dumps(listing)

        """ Add a file to the playlist """
        @app.get('/queue/<path:path>')
        def queueFile(path = None):
            if self.voting_disabled:
                abort(HTTP_NOT_FOUND, "Sorry voting is currently disabled!")
            if not path:
                abort(HTTP_NOT_FOUND, "The file you tried to queue does not exist!")

            if sys.version_info < (3, 0, 0):
                song_path=urllib.unquote(path).decode('utf8')
            else:
                song_path=urllib.parser.unquote(path, encoding='utf-8')
            (songQueued, playlistPosition) = self.bs.queueSong(song_path)
            if not songQueued and playlistPosition == -1:
                abort(HTTP_NOT_FOUND, "The file you tried to queue does not exist!")
            return { "songQueued": songQueued, "playlistPosition": playlistPosition }


        """ Search in the database """
        @app.get('/search/<path>')
        def searchFile(path = None):
            if self.voting_disabled:
                abort(HTTP_NOT_FOUND, "Sorry voting is currently disabled!")
            if not path:
                abort(HTTP_OK, "[{{}}}]")

            if sys.version_info < (3, 0, 0):
                query=urllib.unquote(path).decode('utf8')
            else:
                query=urllib.parser.unquote(path, encoding='utf-8')
            return json.dumps(self.bs.searchFile(query))

        @app.get('/library.json')
        def playlist():
            if self.voting_disabled:
                abort(HTTP_NOT_FOUND, "Sorry voting is currently disabled!")
            response.content_type = 'application/json'
            return self.bs.getLibraryAsJson()

        @app.get('/playlist.json')
        def playlist():
            if self.voting_disabled:
                abort(HTTP_NOT_FOUND, "Sorry voting is currently disabled!")
            response.content_type = 'application/json'
            return self.bs.getPlaylistAsJson()

        @app.route('/vote/deactivate')
        def deactivate():
            if request.remote_addr != '127.0.0.1' and request.remote_addr != '::1':
                abort(HTTP_FORBIDDEN, "Sorry, you're not allowed to deactivate the voting service!")
            self.voting_disabled = True
            print "Voting disabled"

        @app.route('/vote/activate')
        def deactivate():
            if request.remote_addr != '127.0.0.1' and request.remote_addr != '::1':
                abort(HTTP_FORBIDDEN, "Sorry, you're not allowed to activate the voting service!")
            self.voting_disabled = False
            print "Voting enabled"

        @app.route('/vote/status')
        def vote_status():
            return str(not self.voting_disabled)

        """Process a vote with given id """
        @app.get('/vote/<mpdId:int>')
        def vote(mpdId = -1):
            if self.voting_disabled:
                abort(HTTP_NOT_FOUND, "Sorry voting is currently disabled!")
            (songIdExists, newPosition) = self.bs.voteForMpdId(mpdId)
            if songIdExists:
                return {"newPosition": newPosition}
            else:
                abort(HTTP_NOT_FOUND, "The song with id {0} does not exist".format(mpdId))


        @app.route('/<filename:path>')
        def webapp(filename='index.html'):
            if self.voting_disabled:
                abort(HTTP_NOT_FOUND, "Sorry voting is currently disabled!")
            return static_file(filename, root='ionic/mpdVoteClient/www/')

        @app.route('/')
        def redirect_to_webapp():
            if self.voting_disabled:
                abort(HTTP_NOT_FOUND, "Sorry voting is currently disabled!")
            redirect('/index.html')

    def run(self, host='', port=8080):
        run(self.app, host, port)

if __name__ == '__main__':
    s = SimpleMPDVoteWebServer()
    s.run('', 8080)