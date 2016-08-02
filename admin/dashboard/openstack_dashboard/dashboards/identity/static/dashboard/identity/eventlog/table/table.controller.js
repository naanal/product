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

  /**
   * @ngdoc identityeventlogTableController
   * @ngController
   *
   * @description
   * Controller for the identity eventlog table.
   * Serve as the focal point for table actions.
   */
  angular
    .module('horizon.dashboard.identity.eventlog')
    .controller('identityeventlogTableController', identityeventlogTableController);

  identityeventlogTableController.$inject = [
    'horizon.framework.widgets.toast.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.app.core.openstack-service-api.adminevent',
    'horizon.framework.widgets.modal-wait-spinner.service',
    '$scope',
    '$rootScope'
  ];

  function identityeventlogTableController(toast, gettext,admineventAPI,Spinner, $scope, $rootScope) {
      
      $rootScope.retieveAdminEvents = function(){
           Spinner.showModalSpinner(gettext("Retrieving Users...."));
        admineventAPI.getAdminevent()
          .then(function(res){
              Spinner.hideModalSpinner();
              $scope.eventlog = res.data;
              $scope.eventcount = $scope.eventlog.length;
              console.log($scope.eventlog)
              console.log($scope.eventcount)
          },function(error){
              Spinner.hideModalSpinner();
          });
      }
      $rootScope.retieveAdminEvents();
  }

})();
