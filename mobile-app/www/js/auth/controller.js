/**
 * Created by vladthelittleone on 04.12.15.
 */
var ctrl = angular.module('voting.AuthCtrl', [
    'ionic'
]);

ctrl.controller('AuthCtrl', ['$scope', '$state', function ($scope, $state)
{
    $scope.signIn = function(user) {
        console.log('Sign-In', user);
        $state.go('tabs.home');
    };
}]);
