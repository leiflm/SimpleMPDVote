angular.module('simpleMpdVoteClient.controllers', ['simpleMpdVoteClientServices', 'ngCookies'])

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

.controller('VoteListCtrl', function($scope, $stateParams, $cookies, MpdVoteServer) {
	$scope.playlist = MpdVoteServer.playlist();
	if ($cookies.votedList !== undefined)
		$scope.votedList = decodeURIComponent($cookies.votedList).split(",");
	else
		$scope.votedList = [];
	$scope.vote = function(_mpdId) {
	 	MpdVoteServer.vote({mpdId: _mpdId}, function(mpdId) {
	 		$scope.votedId = mpdId;

	 		//append and push
	 		$scope.votedList.push(_mpdId);
	 		$cookies.votedList = $scope.votedList.join();

			$scope.playlist = MpdVoteServer.playlist();
	 	});
	}
	$scope.wasVotedFor = function(_mpdId) {
		var arr = $scope.votedList;
		return (arr.indexOf(_mpdId.toString()) != -1)
	}
});