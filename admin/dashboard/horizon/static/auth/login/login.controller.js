/**
 * Copyright 2016 Naanal Technologies.
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

  angular.module('horizon.auth.login',[])
    .run(['$rootScope', function($rootScope){
      $rootScope.endpoint = false;
      $rootScope.keystone = false;
    }])
    .controller('hzLoginController', hzLoginController);
    hzLoginController.$inject = [
    'horizon.auth.login.hzLoginService',
    '$rootScope'
    ];
    /**
     * @ngdoc hzLoginController
     * @description
     * controller for determining which
     * authentication method user picked.
     */
    function hzLoginController(hzLoginService,$rootScope) {
      var ctrl = this;
      ctrl.auth_type = 'credentials';
      ctrl.init = init;
        function init(endpoint){

          hzLoginService.getKeystone(endpoint)
          .then(function(response){

              if(response == 200) {
                $rootScope.endpoint = true;
                hzLoginService.validateKeystone(endpoint+'/tokens');
              }


          });

        }
    }

})();
