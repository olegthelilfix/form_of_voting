/**
 * Created by vladthelittleone on 04.12.15.
 */
var ctrl = angular.module('voting.TabsCtrl', [
    'ionic'
]);

ctrl.controller('TabsCtrl', ['$scope', '$state', '$http', function ($scope, $state, $http)
{
    $scope.logout = function()
    {
        $http({
            method: 'GET',
            url: "http://13.69.244.156:80/logout",
            headers: {'Content-Type': 'application/json'}
        });

        $state.go('auth');

    };
}]);
