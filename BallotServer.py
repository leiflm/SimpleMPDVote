from PlaylistItem import PlaylistItem
import mpd

class BallotServer:

    mpdHandle = None
    votedPlaylist = None

    def serve(self):
        print "Serving!"

    def getInitialPlaylist(self):
        pl = list()
        for item in self.mpdHandle.playlistid():
            artist = item.get('artist', "Unkown Artist")
            title = item.get('title', item['file'])
            pl.append(PlaylistItem(item['id'], 100000, None, artist, title))
        return pl

    def updatePlaylist(self):
        pl = self.mpdHandle.playlistid()
        

    def getPlaylist(self):
        # We don't have any playlist yet
        if self.votedPlaylist == None:
            self.votedPlaylist = self.getInitialPlaylist()
        else
            self.updatePlaylist()


    def __init__(self):
        # Connect to mpd
        print "Connecting to MPD"
        self.mpdHandle = mpd.MPDClient()
        self.mpdHandle.connect("Kellerbar-Desktop.fritz.box", 6600)
        print "Fetching playlist"
        self.getPlaylist()

if __name__ == "__main__":
        bs = BallotServer()
        bs.serve()