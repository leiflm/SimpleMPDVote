var simpleMpdVoteClientServices = angular.module('simpleMpdVoteClientServices', ['ngResource']);
 
simpleMpdVoteClientServices.factory('MpdVoteServer', ['$resource',
  function($resource){
    return $resource('playlist.json', {}, {
      playlist: {url: 'playlist.json', method:'GET', isArray:true},
      vote: {url: '/vote/:mpdId', method:'GET', params:{mpdId:'mpdId'}},
      library: {url: '/library.json', method:'GET', isArray:true},
      queue: {url: '/queue/:path', method:'GET', params:{path:'path'}}
    });
  }]);