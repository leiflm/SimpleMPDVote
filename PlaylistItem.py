import sys

class PlaylistItem:

    mpdId = None
    playlistRank = sys.maxsize
    playlistRankSetByOperator = None
    artist = "Unknown Artist"
    title = "Unkown Title"

    def __init__(self, mpdId, rank, rankByOperator, artist, title):
        self.mpdId = mpdId
        self.playlistRank = rank
        self.playlistRankSetByOperator = rankByOperator
        self.artist = artist
        self.title = title
