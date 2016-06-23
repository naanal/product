/**
 * Copyright 2015 IBM Corp.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */
(function() {
  'use strict';

  angular
    .module('horizon.auth.login')
    .factory('horizon.auth.login.hzLoginService', hzLoginService)
    
    hzLoginService.$inject = [
    '$http', '$window', '$rootScope'
    ];

    function hzLoginService($http,$window, $rootScope) {
        var obj = {};

        obj.getKeystone = function(endpoint) {
            return $http({
                method: "GET",
                url: endpoint,
            }).then(function(response) { //returns a call back
                return response.status;
            }, function errorCallback(response) {
                $window.location.href = "/seriouserror/endpointnotfound/"
            });
        }
        obj.validateKeystone = function(endpoint) {
            return $http({
                method: "POST",
                url: endpoint,
                data: '{"auth": {"tenantName": "admin", "passwordCredentials": {"username": "admin", "password": "ADMI"}}}',
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(function(response) { //returns a call back
                return response;
            }, function errorCallback(response){
                window.stop();
                if(response.status == 401)
                     $rootScope.keystone = true;
                 else
                    $window.location.href = "/seriouserror/keystone_malfunctioned/"
            });
            
        }
        return obj;
    }

})();
