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
   * @ngdoc identityUsersTableController
   * @ngController
   *
   * @description
   * Controller for the identity users table.
   * Serve as the focal point for table actions.
   */
  angular
    .module('horizon.dashboard.identity.users')
    .controller('identityUsersTableController', identityUsersTableController);

  identityUsersTableController.$inject = [
    'horizon.framework.widgets.toast.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.app.core.openstack-service-api.ldap',
      'horizon.framework.widgets.modal-wait-spinner.service',
    '$scope',
    '$rootScope'
  ];

  function identityUsersTableController(toast, gettext, ldapAPI,Spinner, $scope, $rootScope) {

      $scope.selected = [];
        $scope.query = {
          order: 'username',
          limit: 5,
          page: 1
        };

      $rootScope.retieveLdapUsers = function(){
           Spinner.showModalSpinner(gettext("Retrieving Users...."));
        ldapAPI.getUsers()
          .then(function(res){
              Spinner.hideModalSpinner();
              $scope.ldapusers = res.data;
              $scope.ldapuserscount = $scope.ldapusers.length;
          },function(error){
              Spinner.hideModalSpinner();
          });
      }
      $rootScope.retieveLdapUsers();
  }

})();
