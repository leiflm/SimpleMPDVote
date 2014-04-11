from PlaylistItem import PlaylistItem
import mpd

class BallotServer:

    mpdHandle = None
    votedPlaylist = None

    def serve(self):
        print "Serving!"

    def mergeVotePlaylistIntodMpdPlaylist(self):
        mpdPl = self.mpdHandle.playlistid()
        pl = list()

        for plItem in mpdPl:
            artist = plItem.get('artist', "Unkown Artist")
            title = plItem.get('title', plItem['file'])
            votes = 0
            operatorPos = None
            found = False
            vitem = None
            mpdId = int(plItem['id'])

            if self.votedPlaylist:
                for vitem in self.votedPlaylist:
                    if vitem.mpdId == mpdId:
                        found = True
                        break

                # This element was in the list
                if found:
                    votes = vitem.votes
                    operatorPos = vitem.playlistPosSetByOperator

            pl.append(PlaylistItem(mpdId, votes, operatorPos, artist, title))
        return pl

    def updatePlaylist(self):
        self.playlist = self.mergeVotePlaylistIntodMpdPlaylist()

        ''' 
            Create new playlist, incorporating operator changes
        for item in mpdPl:
            found = False
            vitem = None
            for lowerItem in mpdPl[mpdPl.index(item):]:
                if vitem.votes < lowerItem.votes:
                # Check whether it was inserted by the operator
        '''

    def swapAccordingToVotes(self, plItem):
        pl = self.playlist
        idx = pl.index(plItem)
        aboveListReversed = pl[:idx]
        aboveListReversed.reverse()

        for itemAbove in aboveListReversed:
            idx = pl.index(plItem)
            if itemAbove.votes < plItem.votes: # more votes -> swap
                idx2 = pl.index(itemAbove)
                if idx2 == 0: # We don't touch the first (playing) element
                    return
                pl[idx], pl[idx2] = pl[idx2], pl[idx]
                continue
            return

    def voteForMpdId(self, mpdId):
        success = False
        if self.playlist == None:
            self.updatePlaylist()

        for plItem in self.playlist:
            if plItem.mpdId != mpdId:
                continue
            plItem.votes += 1
            self.swapAccordingToVotes(plItem)
            success = True
        return success

    def getPlaylist(self):
        return self.playlist

    def __init__(self):
        # Connect to mpd
        print "Connecting to MPD"
        self.mpdHandle = mpd.MPDClient()
        self.mpdHandle.connect("Kellerbar-Desktop.fritz.box", 6600)
        print "Updating playlist"
        self.updatePlaylist()
        
        # Some test voting
        print "id : votes"
        for el in self.getPlaylist():
            print "%d : %d" % (el.mpdId, el.votes)
        self.voteForMpdId(6)
        self.voteForMpdId(6)
        self.voteForMpdId(4)
        self.voteForMpdId(4)
        self.voteForMpdId(6)
        self.voteForMpdId(8)
        self.voteForMpdId(8)
        self.voteForMpdId(8)
        self.voteForMpdId(8)
        print ("voted")
        print "id : votes"
        for el in self.getPlaylist():
            print "%d : %d" % (el.mpdId, el.votes)
        # Test voting end

if __name__ == "__main__":
        bs = BallotServer()
        bs.serve()