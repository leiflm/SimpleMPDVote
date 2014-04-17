from BallotServer import BallotServer
import urllib
from bottle import Bottle, run, get, request, response, static_file, redirect, abort

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404

class SimpleMPDVoteWebServer():

    def __init__(self):
        app = Bottle()
        
        @app.get('/library.json')
        def playlist():
            if self.voting_disabled:
                abort(HTTP_NOT_FOUND, "Sorry voting is currently disabled!")
            response.content_type = 'application/json'
            return self.bs.getLibraryAsJson().encode('utf-8')

        @app.get('/playlist.json')
        def playlist():
            if self.voting_disabled:
                abort(HTTP_NOT_FOUND, "Sorry voting is currently disabled!")
            response.content_type = 'application/json'
            return self.bs.getPlaylistAsJson().encode('utf-8')

        @app.route('/vote/deactivate')
        def deactivate():
            if request.remote_address != '127.0.0.1': #watchout, this is IPv4 :-/
                abort(HTTP_FORBIDDEN, "Sorry, you're not allowed to deactivate the voting service!")
            self.voting_disabled = True
            print "Voting disabled"

        @app.route('/vote/activate')
        def deactivate():
            if request.remote_address != '127.0.0.1': #watchout, this is IPv4 :-/
                abort(HTTP_FORBIDDEN, "Sorry, you're not allowed to activate the voting service!")
            self.voting_disabled = False
            print "Voting enabled"

        """Process a vote with given id """
        @app.get('/vote/<mpdId:int>')
        def vote(mpdId = -1):
            if self.voting_disabled:
                abort(HTTP_NOT_FOUND, "Sorry voting is currently disabled!")
            (songIdExists, newPosition) = self.bs.voteForMpdId(mpdId)
            if songIdExists:
                return str(newPosition)
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

        """ Finally set up instance """
        self.voting_disabled = False
        self.bs = BallotServer('localhost', 6600)
        self.app = app

    def close(self):
        self.httpd.shutdown()
        print ("{0} Server Stops - {1}:{2}".format(time.asctime(), self.host, self.port))

    def run(self, host, port):
        run(self.app, host='localhost', port=8080)

if __name__ == '__main__':
    s = SimpleMPDVoteWebServer()
    s.run('localhost', 8080)