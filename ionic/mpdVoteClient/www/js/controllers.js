angular.module('simpleMpdVoteClient.controllers', ['simpleMpdVoteClientServices', 'ivpusic.cookie'])

.controller('AppCtrl', function($scope) {
})

.controller('PlaylistsCtrl', function($scope) {
  $scope.playlists = [
    { title: 'Reggae', id: 1 },
    { title: 'Chill', id: 2 },
    { title: 'Dubstep', id: 3 },
    { title: 'Indie', id: 4 },
    { title: 'Rap', id: 5 },
    { title: 'Cowbell', id: 6 }
  ];
})

.controller('VoteListCtrl', function($scope, $stateParams, ipCookie, MpdVoteServer) {
	$scope.votedList = [];
	$scope.playlist = MpdVoteServer.playlist();
	var cookie = ipCookie('votedList');
	if (cookie !== undefined) {
		var arr = cookie.toString().split(',');
		for (var i = 0; i < arr.length; i++) {
			$scope.votedList.push(parseInt(arr[i]));
		}
	}
	$scope.vote = function(_mpdId) {
	 	MpdVoteServer.vote({mpdId: _mpdId}, function(mpdId) {
	 		$scope.votedId = mpdId;

	 		//append and push
	 		$scope.votedList.push(_mpdId);
	 		ipCookie('votedList', $scope.votedList.join(), { expires: 600, expirationUnit: 'minutes' });

			$scope.playlist = MpdVoteServer.playlist();
	 	});
	}
	$scope.wasVotedFor = function(_mpdId) {
		var arr = $scope.votedList;
		return (arr.indexOf(_mpdId) != -1)
	}
})

.controller('LibraryCtrl', function($scope, $stateParams, ipCookie, MpdVoteServer) {
	$scope.library = MpdVoteServer.library();
	$scope.queue = function(_path) {
	 	MpdVoteServer.queue({path: _path}, function(path) {
	 		;
	 	});
	}
	$scope.libraryItemHasTitle = function(item) {
		return (item.title !== undefined);
	}
});