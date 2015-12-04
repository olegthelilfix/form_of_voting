/**
 * Created by vladthelittleone on 04.12.15.
 */
var ctrl = angular.module('voting.PhotoCtrl', [
    'ionic',
    'ngCordova'
]);

ctrl.controller('HomeCtrl', ['$scope', '$cordovaCamera', function ($scope, $cordovaCamera)
{
    var photoOptions =
    {
        quality: 75,
        destinationType: Camera.DestinationType.DATA_URL,
        allowEdit: true,
        encodingType: Camera.EncodingType.JPEG,
        targetWidth: 300,
        targetHeight: 300,
        popoverOptions: CameraPopoverOptions,
        saveToPhotoAlbum: false
    };

    $scope.takePhoto = function ()
    {
        photoOptions.sourceType = Camera.PictureSourceType.CAMERA;

        $cordovaCamera.getPicture(photoOptions)
            .then(function (imageData)
            {
                $scope.imgURI = "data:image/jpeg;base64," + imageData;
            },
            function (err)
            {
                // An error occured. Show a message to the user
            });
    };

    $scope.choosePhoto = function ()
    {
        photoOptions.sourceType = Camera.PictureSourceType.PHOTOLIBRARY;

        $cordovaCamera.getPicture(photoOptions)
            .then(function (imageData)
            {
                $scope.imgURI = "data:image/jpeg;base64," + imageData;
            },
            function (err)
            {
                // An error occured. Show a message to the user
            });
    };
}]);
