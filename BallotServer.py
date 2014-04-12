from PlaylistItem import PlaylistItem, JsonEncoder
from MPDClientWrapper import MPDClientWrapper
import mpd
import json
import threading

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

    '''
    Moves an item in the playlist according to its votes.
    If it does so, it returns the new position. If the position remains
    unchanged, -1 is returned
    If it does so, it returns the new position.
    e.g.: (True, 2)
    If the position remains unchanged, -1 is returned
          (False, -1)
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
            return -1
            return (False, -1)
        idx2 = pl.index(lessVotes)
        pl.insert(idx2, pl.pop(idx))
        self.mpdHandle.moveid(plItem.mpdId, idx2)
        print ("Swapping to playlist position {0}".format( idx2 ))
        return idx2
        return (True, idx2)

    def voteForMpdId(self, mpdId):
        newPos = -1
        newPos = (False, -1)
        if self.playlist == None:
            self.updatePlaylist()

        for plItem in self.playlist:
            if plItem.mpdId != mpdId:
                continue
            plItem.votes += 1
            newPos = self.swapAccordingToVotes(plItem)
        return newPos

    def getPlaylist(self):
        return self.playlist

    def getPlaylistAsJson(self):
        return json.dumps(self.playlist, cls=JsonEncoder)
        #return json.dumps(self.playlist.__dict__)

    def getLibrary(self):
        return self.mpdHandle.listallinfo()

    def getLibraryAsJson(self):
        return json.dumps(self.getLibrary(), cls=JsonEncoder)

    def queueSong(self, path):
        return self.mpdHandle.add(path)

    def setupTimer(self):
        self.updatePlaylist()
        threading.Timer(5, self.setupTimer).start()

    def __init__(self):
        # Connect to mpd
        print ("Connecting to MPD".format())
        self.mpdHandle = MPDClientWrapper(MPD_HOST, MPD_PORT)
        self.mpdHandle.consume(1)
        self.updatePlaylist()
        self.setupTimer()