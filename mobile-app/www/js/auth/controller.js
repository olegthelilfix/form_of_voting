/**
 * Created by vladthelittleone on 04.12.15.
 */
var ctrl = angular.module('voting.AuthCtrl', [
    'ionic'
]);

ctrl.controller('AuthCtrl', ['$scope', '$state', '$http', function ($scope, $state, $http)
{
    $scope.signIn = function(user)
    {
        $state.go('tabs.home');

        $http({
            method: 'POST',
            url: "http://13.69.244.156:80/auth",
            data: {
                username: user.username,
                password: user.password
            },
            headers: {'Content-Type': 'application/json'}
        }).
        success(function(status)
        {
            if (status == "OK")
            {
                $state.go('tabs.home');
            }
        }).
        error(function(error)
        {

        });
    };
}]);
