from PlaylistItem import PlaylistItem, JsonEncoder
from MPDClientWrapper import MPDClientWrapper
import mpd
import json
import threading

class BallotServer:

    mpdHandle = None
    votedPlaylist = None

    """ Returns the playlist position of a file if found, else -1 """
    def getIndexForFile(self, file):
        pl = self.votedPlaylist
        if file == None:
            return -1
        for i in xrange(0, len(pl)):
            if pl[i].file == file:
                return i
        return -1

    def mergeVotePlaylistIntodMpdPlaylist(self):
        mpdPl = self.mpdHandle.playlistid()
        pl = list()

        for plItem in mpdPl:
            artist = plItem.get('artist', "Unkown Artist")
            title = plItem.get('title', plItem['file'])
            file = plItem['file']
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

            pl.append(PlaylistItem(mpdId, votes, operatorPos, artist, title, file))
        return pl

    def updatePlaylist(self):
        self.listLock.acquire()
        self.votedPlaylist = self.mergeVotePlaylistIntodMpdPlaylist()
        self.listLock.release()

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
    Moves the given item from its current position to the one behind another
    song that has equally or more votes.

    If it does so, it returns the new position. If the position remains
    unchanged, -1 is returned
    If it does so, it returns the new position.
    e.g.: (True, 2)
    If the position remains unchanged, -1 is returned
          (True, -1)
    '''
    def moveFromBottomAccordingToVotes(self, plItem):
        pl = self.votedPlaylist
        idx = pl.index(plItem)
        aboveListReversed = pl[1:idx]
        aboveListReversed.reverse()

        if len(aboveListReversed) <= 1:
            return (True, -1)
        lessVotes = aboveListReversed[0]

        for itemAbove in aboveListReversed:
            if itemAbove.votes >= plItem.votes:
                break
            else:
                lessVotes = itemAbove

        idx2 = pl.index(lessVotes)
        pl.insert(idx2, pl.pop(idx))
        self.mpdHandle.moveid(plItem.mpdId, idx2)
        print ("moving track from {0} to playlist position {1}".format(idx, idx2))
        return (True, idx2)

    '''
    Moves an item in the playlist according to its votes.
    If it does so, it returns the new position. If the position remains
    unchanged, -1 is returned
    If it does so, it returns the new position.
    e.g.: (True, 2)
    If the position remains unchanged, -1 is returned
          (True, -1)
    '''
    def voteForMpdId(self, mpdId):
        voteSuccess = (False, -1)
        if self.votedPlaylist == None:
            self.updatePlaylist()
        pl = self.votedPlaylist

        for track in pl:
            if track.mpdId == mpdId:
                track.votes += 1
                voteSuccess = self.moveFromBottomAccordingToVotes(track)
                break
        return voteSuccess

    def getLsInfo(self, path):
        return self.mpdHandle.lsinfo(path)

    def getPlaylist(self):
        return self.votedPlaylist

    def getPlaylistAsJson(self):
        return json.dumps(self.votedPlaylist, cls=JsonEncoder)
        #return json.dumps(self.votedPlaylist.__dict__)

    def getLibrary(self):
        return self.mpdHandle.listallinfo()

    def getLibraryAsJson(self):
        return json.dumps(self.getLibrary(), cls=JsonEncoder)

    """ return value: (bool, int) = (SongQueued, PlaylistPosition) """
    def queueSong(self, path):
        # maybe it's already queued
        index = self.getIndexForFile(path)
        if index != -1:
            return (False, index + 1)
        # try to add it and get the index afterwards
        try:
            self.mpdHandle.add(path)
            self.updatePlaylist()
        except mpd.CommandError:
            (False, -1)
        return (True, self.getIndexForFile(path) + 1)

    def searchFile(self, query):
        return self.mpdHandle.search("file", query)

    def setupTimer(self):
        self.updatePlaylist()
        if not self.timerStop:
            self.timer = threading.Timer(5, self.setupTimer)
            self.timer.start()

    def __init__(self, host, port):
        # Connect to mpd
        print ("Connecting to MPD on {0}:{1}".format(host, port))
        self.mpdHandle = MPDClientWrapper(host, port)
        self.mpdHandle.consume(1)
        self.listLock = threading.Lock()
        print ("Updating playlist".format())
        self.updatePlaylist()
        self.timerStop = False
        self.setupTimer()

    def close(self):
        self.timerStop = True
        self.timer.cancel()
