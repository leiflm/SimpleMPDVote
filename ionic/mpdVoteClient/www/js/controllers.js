angular.module('simpleMpdVoteClient.controllers', ['simpleMpdVoteClientServices'])

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

.controller('VoteListCtrl', function($scope, $stateParams, MpdVoteServer) {
	$scope.playlist = MpdVoteServer.playlist();
})

.controller('VoteCtrl', function($scope, $stateParams, MpdVoteServer) {
 	MpdVoteServer.vote({mpdId: $routeParams.mpdId}, function(mpdId) {
 		$scope.votedId = mpdId;
 	});
});