/**
 * Created by vladthelittleone on 04.12.15.
 */
var ctrl = angular.module('voting.HomeCtrl', [
    'ionic',
    'ngCordova'
]);

ctrl.controller('HomeCtrl', ['$scope', '$cordovaCamera', function ($scope, $cordovaCamera)
{
    $scope.uploadStatus = "Upload blank";

    $scope.takePhoto = function ()
    {
        var options =
        {
            quality: 50,
            destinationType: Camera.DestinationType.FILE_URL,
            sourceType: Camera.PictureSourceType.CAMERA
        };

        $cordovaCamera.getPicture(options)
            .then(function (imageData)
            {
                $scope.picData = imageData;
            },
            function (err)
            {
                //
            })
    };

    $scope.choosePhoto = function ()
    {
        var options =
        {
            quality: 50,
            destinationType: Camera.DestinationType.FILE_URI,
            sourceType: Camera.PictureSourceType.PHOTOLIBRARY
        };

        $cordovaCamera.getPicture(options)
            .then(function (imageURI)
            {
                window.resolveLocalFileSystemURI(imageURI, function (fileEntry)
                {
                    $scope.picData = fileEntry.nativeURL;
                });
            },
            function (err)
            {
                $scope.uploadStatus = err;
            })
    };

    $scope.uploadPhoto = function ()
    {
        function onUploadSuccess(result)
        {
            $scope.uploadStatus = "RESULT: " + JSON.stringify(result.response);
        }

        function onUploadFail(err)
        {
            $scope.uploadStatus = "ERROR: " + JSON.stringify(err);
        }

        try
        {
            var fileURL = $scope.picData;
            var options = new FileUploadOptions();

            options.fileKey = "file";
            options.fileName = fileURL.substr(fileURL.lastIndexOf('/') + 1);
            options.mimeType = "image/jpeg";
            options.chunkedMode = true;

            var ft = new FileTransfer();
            ft.upload(fileURL, encodeURI("http://localhost:8085/upload"), onUploadSuccess, onUploadFail, options);
        }
        catch (err)
        {
            $scope.uploadStatus = err;
        }
    };
}]);
