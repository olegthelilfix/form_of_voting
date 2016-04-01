/**
 * @since 04.12.15
 * @author Skurishin Vladislav
 */
var ctrl = angular.module('voting.LoadsCtrl', [
    'ionic'
]);

ctrl.controller('LoadsCtrl', ['$scope', '$http', '$interval', function ($scope, $http, $interval)
{
    $scope.token = ['asdasd', 'asdasdad', 'asdasdasd'];

    function fn ()
    {
        $http({
            method: 'GET',
            url: "http://localhost:8085/check_status",
            headers: {'Content-Type': 'application/json'}
        }).
        success(function(token)
        {
            $scope.token = token;
            $scope.$apply();
        }).
        error(function(err)
        {
            $scope.token = [ err ];
            $scope.$apply();
        });
    }

    fn();

    $interval(fn, 10000);
}]);
