from PlaylistItem import PlaylistItem, JsonEncoder
import mpd
import json

MPD_HOST = "Kellerbar-Desktop.fritz.box"
MPD_PORT = 6600
class BallotServer:

    mpdHandle = None
    votedPlaylist = None

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
        aboveListReversed = pl[1:idx]
        aboveListReversed.reverse()
        lessVotes = None

        for itemAbove in aboveListReversed:
            if itemAbove.votes > plItem.votes:
                break
            lessVotes = itemAbove

        if lessVotes == None:
            return
        idx2 = pl.index(lessVotes)
        pl.insert(idx2, pl.pop(idx))
        self.mpdHandle.moveid(plItem.mpdId, idx2)
        #print "Swapping to playlist position %i" % idx2
        print ("Swapping to playlist position {0}".format( idx2 ))

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

    def getPlaylistAsJson(self):
        return json.dumps(self.playlist, cls=JsonEncoder)
        #return json.dumps(self.playlist.__dict__)

    def __init__(self):
        # Connect to mpd
        print ("Connecting to MPD".format())
        self.mpdHandle = mpd.MPDClient()
        self.mpdHandle.connect(MPD_HOST, MPD_PORT)
        print ("Updating playlist".format())
        self.updatePlaylist()
        
