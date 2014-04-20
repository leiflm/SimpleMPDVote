angular.module('simpleMpdVoteClient.controllers', ['simpleMpdVoteClientServices', 'ivpusic.cookie'])

.controller('AppCtrl', function($scope) {
})

.controller('BrowseCtrl', function($scope, $stateParams, MpdVoteServer) {
	var _path = '';

	if ($stateParams.mpdPath !== undefined)
		_path = $stateParams.mpdPath;
	_path = _path.replace(/\//, "");

	$scope.listing = MpdVoteServer.browse({path: _path});

	$scope.getType = function(item) {
		if (item['directory'] !== undefined)
			return "directory";
		else if (item['file'] !== undefined)
			return "file";
	}
	$scope.queue = function(_path) {
	 	MpdVoteServer.queue({path: _path}, function (response) {
	 		if (!response.songQueued && (response.playlistPosition != -1)) {
	 			alert('This song is already in the playlist! (#' + response.playlistPosition + ')');
	 		}
	 	});
	}
	$scope.libraryItemHasTitle = function(item) {
		return (item.title !== undefined);
	}
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
    $scope.getIndexForMpdId = function(mpdId) {
        for (var i = 0; i < $scope.playlist.length; i++) {
            if ($scope.playlist[i].mpdId == mpdId)
                return i;
        }
        return -1;
    }
	$scope.vote = function(_mpdId) {
	 	MpdVoteServer.vote({mpdId: _mpdId}, function(response) {
            var newPosition = response['newPosition'];
            var idx = $scope.getIndexForMpdId(_mpdId);
            var plItem = $scope.playlist[idx];

	 		//append and push
	 		$scope.votedList.push(_mpdId);
	 		ipCookie('votedList', $scope.votedList.join(), { expires: 600, expirationUnit: 'minutes' });

            if (newPosition == "-1") {
                // didn't move, so just return
                return;
            }

            //update playlist
            $scope.playlist.splice(idx, 1);
            $scope.playlist.splice(newPosition, 0, plItem);
	 	}, function(fail_response) {
            var newPosition = response['newPosition'];
            var idx = $scope.getIndexForMpdId(_mpdId);
            if (idx == -1) {
                // vote request was sent and in the meanwhile the playlist was refreshed or similar
                return;
            }
            if (newPosition == "-1") {
                alert('Sorry, that song is not in the playlist any longer :-/');
                $scope.playlist.splice(idx,1)
                return;
            }
        });
	}
	$scope.wasVotedFor = function(_mpdId) {
		var arr = $scope.votedList;
		return (arr.indexOf(_mpdId) != -1)
	}
})

.controller('SearchCtrl', function($scope, MpdVoteServer) {
	$scope.queryString = "";
	$scope.resultset = [];

	$scope.queue = function(_path) {
	 	MpdVoteServer.queue({path: _path}, function(path) {
	 		;
	 	});
	}
	$scope.itemHasTitle = function(item) {
		return (item.title !== undefined);
	}
	$scope.query = function(_queryString) {
		$scope.resultset = MpdVoteServer.searchFile({query: _queryString});
	}

	$scope.queue = function(_path) {
	 	MpdVoteServer.queue({path: _path}, function (response) {
	 		if (!response.songQueued && (response.playlistPosition != -1)) {
	 			alert('This song is already in the playlist! (#' + response.playlistPosition + ')');
	 		}
	 	});
	}
});