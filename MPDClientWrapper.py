import mpd

class MPDClientWrapper(mpd.MPDClient):
	"""docstring for MPDClientWrapper"""

	_host = "localhost"
	_port = "6600"

	def __init__(self, MPD_HOST, MPD_PORT):
		super(MPDClientWrapper, self).__init__()
		self._host = MPD_HOST
		self._port = MPD_PORT
		self.connect(MPD_HOST, MPD_PORT)

	def playlistid(self):
		try:
			return super(MPDClientWrapper, self).playlistid()
		except mpd.ConnectionError:
			self.connect(self._host, self._port)
			return super(MPDClientWrapper, self).playlistid()


	def moveid(self, mpdId, pos):
		try:
			return super(MPDClientWrapper, self).moveid(mpdId, pos)
		except mpd.ConnectionError:
			self.connect(self._host, self._port)
			return super(MPDClientWrapper, self).moveid(mpdId, pos)

	def listallinfo(self):
		try:
			return super(MPDClientWrapper, self).listallinfo()
		except mpd.ConnectionError:
			self.connect(self._host, self._port)
			return super(MPDClientWrapper, self).listallinfo()

	def add(self, path):
		try:
			return super(MPDClientWrapper, self).add(path)
		except mpd.ConnectionError:
			self.connect(self._host, self._port)
			return super(MPDClientWrapper, self).add(path)

	def lsinfo(self, path):
		try:
			return super(MPDClientWrapper, self).lsinfo(path)
		except mpd.ConnectionError:
			self.connect(self._host, self._port)
			return super(MPDClientWrapper, self).lsinfo(path)

	def search(self, type, query):
		try:
			return super(MPDClientWrapper, self).search(type, query)
		except mpd.ConnectionError:
			self.connect(self._host, self._port)
			return super(MPDClientWrapper, self).search(type, query)