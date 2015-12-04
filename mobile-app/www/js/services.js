/**
 * Created by vladthelittleone on 04.12.15.
 */
angular.module('starter.services', [])
/**
 * The forms factory handles saving and loading forms
 * from local storage, and also lets us save and load the
 * last active form index.
 */
    .factory('forms', function ()
    {
        return {
            all: function ()
            {
                var formString = window.localStorage['forms'];
                if (formString)
                {
                    return angular.fromJson(formString);
                }
                return [];
            },
            save: function (forms)
            {
                window.localStorage['forms'] = angular.toJson(forms);
            },
            newForm: function (formTitle)
            {
                // Add a new form
                return {
                    title: formTitle,
                    tasks: []
                };
            },
            getLastActiveIndex: function ()
            {
                return parseInt(window.localStorage['lastActiveForm']) || 0;
            },
            setLastActiveIndex: function (index)
            {
                window.localStorage['lastActiveForm'] = index;
            }
        }
    });
