/**
 * @since 04.12.15
 * @author Skurishin Vladislav
 */
var ctrl = angular.module('voting.LoadsCtrl', [
    'ionic'
]);

ctrl.controller('LoadsCtrl', ['$scope', '$http', function ($scope, $http)
{
    $http({
        method: 'GET',
        url: "http://localhost:8085/check_status"
    }).
    success(function(token)
    {
        $scope.token = token;
    });
}]);
