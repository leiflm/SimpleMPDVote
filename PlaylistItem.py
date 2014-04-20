import sys
import json

class PlaylistItem:

    mpdId = None
    votes = 0
    playlistPosSetByOperator = None
    artist = "Unknown Artist"
    title = "Unkown Title"

    def __init__(self, mpdId, votes, posByOperator, artist, title, file):
        self.mpdId = mpdId
        self.votes = votes
        self.playlistPosSetByOperator = posByOperator
        self.artist = artist
        self.title = title
        self.file = file

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PlaylistItem):
            return {"mpdId" : obj.mpdId, "votes": obj.votes, "artist": obj.artist, "title": obj.title}
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
