var simpleMpdVoteClientServices = angular.module('simpleMpdVoteClientServices', ['ngResource']);
 
simpleMpdVoteClientServices.factory('MpdVoteServer', ['$resource',
  function($resource){
    return $resource('/', {}, {
      browse: {url: '/browse/:path', method:'GET', isArray:true, params:{path:'path'}},
      playlist: {url: 'playlist.json', method:'GET', isArray:true},
      vote: {url: '/vote/:mpdId', method:'GET', isArray:false, params:{mpdId:'mpdId'}},
      library: {url: '/library.json', method:'GET', isArray:true},
      queue: {url: '/queue/:path', method:'GET', isArray:false, params:{path:'path'}}
    });
  }]);