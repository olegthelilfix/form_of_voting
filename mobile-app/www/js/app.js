// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
angular.module('voting', [
    'starter.services',
    'ionic',
    'ngCordova'
])
.run(function ($ionicPlatform)
{
    $ionicPlatform.ready(function ()
    {
        // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
        // for form inputs)
        if (window.cordova && window.cordova.plugins.Keyboard)
        {
            cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
        }
        if (window.StatusBar)
        {
            StatusBar.styleDefault();
        }
    });
})
.controller('VotingCtrl', [
    '$scope',
    '$timeout',
    '$ionicSideMenuDelegate',
    '$cordovaCamera',
    'forms',
    function ($scope, $timeout, $ionicSideMenuDelegate, $cordovaCamera, forms)
    {

        // A utility function for creating a new form
        // with the given formTitle
        var createForm = function (formTitle)
        {
            var newForm = forms.newForm(formTitle);
            $scope.forms.push(newForm);
            forms.save($scope.forms);
            $scope.selectForm(newForm, $scope.forms.length - 1);
        };

        var photoOptions =
        {
            quality: 75,
            destinationType: Camera.DestinationType.DATA_URL,
            sourceType: Camera.PictureSourceType.CAMERA,
            allowEdit: true,
            encodingType: Camera.EncodingType.JPEG,
            targetWidth: 300,
            targetHeight: 300,
            popoverOptions: CameraPopoverOptions,
            saveToPhotoAlbum: false
        };

        // Load or initialize forms
        $scope.forms = forms.all();

        // Grab the last active, or the first form
        $scope.activeForm = $scope.forms[forms.getLastActiveIndex()];

        $scope.takePhoto = function ()
        {
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

            $cordovaCamera.getPicture(options)
                .then(function (imageData)
                {
                    $scope.imgURI = "data:image/jpeg;base64," + imageData;
                },
                function (err)
                {
                    // An error occured. Show a message to the user
                });
        };

        // Called to create a new form
        $scope.newForm = function ()
        {
            var formTitle = prompt('Form name');
            if (formTitle)
            {
                createForm(formTitle);
            }
        };

        // Called to select the given form
        $scope.selectForm = function (form, index)
        {
            $scope.activeForm = form;
            forms.setLastActiveIndex(index);
            $ionicSideMenuDelegate.toggleLeft(false);
        };

        $scope.toggleSideBar = function ()
        {
            $ionicSideMenuDelegate.toggleLeft();
        };


        // Try to create the first form, make sure to defer
        // this by using $timeout so everything is initialized
        // properly
        $timeout(function ()
        {
            if ($scope.forms.length == 0)
            {
                while (true)
                {
                    var formTitle = prompt('Your first form title:');
                    if (formTitle)
                    {
                        createForm(formTitle);
                        break;
                    }
                }
            }
        });

    }
]);
