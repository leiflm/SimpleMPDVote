import sys

class PlaylistItem:

    mpdId = None
    votes = 0
    playlistPosSetByOperator = None
    artist = "Unknown Artist"
    title = "Unkown Title"

    def __init__(self, mpdId, votes, posByOperator, artist, title):
        self.mpdId = mpdId
        self.votes = votes
        self.playlistPosSetByOperator = posByOperator
        self.artist = artist
        self.title = title
