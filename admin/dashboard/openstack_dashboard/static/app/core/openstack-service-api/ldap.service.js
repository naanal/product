/**
 * Copyright 2016, Naanal Technologies Pvt Limited.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function () {
  'use strict';

  angular
    .module('horizon.app.core.openstack-service-api')
    .factory('horizon.app.core.openstack-service-api.ldap', ldapAPI);

  ldapAPI.$inject = [
    'horizon.framework.util.http.service',
    'horizon.framework.widgets.toast.service'
  ];

  /**
   * @ngdoc service
   * @name ldap
   * @param {Object} apiService
   * @param {Object} toastService
   * @description Provides direct pass through to LDAP with NO abstraction.
   * @returns {Object} The service
   */
  function ldapAPI(apiService, toastService) {
    var service = {
      getUsers: getUsers,
      getAvailableUsers: getAvailableUsers,
      createUsers: createUsers,
      disableUsers: disableUsers,
      getComputers: getComputers,
      getAvailableComputers: getAvailableComputers,
      mapUserToVm: mapUserToVm,
      editUsersAttributes: editUsersAttributes
    };

    return service;

    ///////////////

    // Users

    /**
     * @name getUsers
     * @description
     * Get all Users of AD
     *
     * @param none
     *
     * @returns {Object} The result of the API call
     */
    function getUsers() {
      return apiService.get('/api/ldap/users/')
        .error(function () {
          toastService.add('error', gettext('Unable to retrieve Users.'));
        });
    }

    /**
     * @name getAvailableUsers
     * @description
     * Get all available Users of AD
     *
     * @param none
     *
     * @returns {Object} The result of the API call
     */
    function getAvailableUsers() {
      return apiService.get('/api/ldap/available_users/')
        .error(function () {
          toastService.add('error', gettext('Unable to retrieve Available Users.'));
        });
    }
    /**
     * @name createUsers
     * @description
     * Create a new users. This returns the new user object on success.
     *
     * @param {array of object} users
     * The users to create
     *
     * @param {string} username
     * Name of the user. Required.
     *
     * @param {string} password
     * Password of the user. Required.
     *
     * @param {string} ou
     * Organizational Unit of User. Required.
     *
     * @param {string} dns
     * Domain Name Seriver of AD. Required.
     *
     * @returns {Object} The result of the API call
     **/
    function createUsers(data) {
      return apiService.post('/api/ldap/users/',data)
        .error(function () {
          toastService.add('error', gettext('Unable to create the User.'));
        });
    }



    /**
     * @name diableUsers
     * @description
     * Disable List of Users.
     *
     * @param {array of object} users
     * Users to delete.
     *
     * @param {string} dn
     * Distinguished name of the user
     *
     * @returns {Object} The result of the API call
     */
    function disableUsers(data) {
      return apiService.delete('/api/ldap/users/',data)
        .error(function () {
          toastService.add('error', gettext('Unable to disable the User.'));
        });
    }

    
     // Computers

    /**
     * @name getComputers
     * @description
     * Get all computers from AD
     *
     * @param none
     *
     * @returns {Object} The result of the API call
     */
    function getComputers() {
      return apiService.get('/api/ldap/computers/')
        .error(function () {
          toastService.add('error', gettext('Unable to retrieve Computers.'));
        });
    }

    /**
     * @name getAvailableComputers
     * @description
     * Get all available computers (not mapped to the users) from AD
     *
     * @param none
     *
     * @returns {Object} The result of the API call
     */

    function getAvailableComputers() {
      return apiService.get('/api/ldap/available_computers/')
        .error(function () {
          toastService.add('error', gettext('Unable to retrieve Available Computers.'));
        });
    }

    // Map

    /**
     * @name map
     * @description
     * Map a user to available computers
     *
     * Manual Assign - Explicitly pass Available computer
     *
     * @param {array of object} map
     * @param {string} user_dn
     * @param {string} computer
     * @param {boolean} autoMap
     *
     * Auto Assign - Automatically assign Available computer
     *
     * @param {array of userdn} map
     * @param {boolean} autoMap
     *
     * @returns {Object} The result of the API call
     */
    function mapUserToVm(data) {
      return apiService.post('/api/ldap/map/',data)
        .error(function () {
          toastService.add('error', gettext('Unable to map user to computer.'));
        });
    }

    // Edit the user Attributes

    /**
     * @users{array of users}
     * @change_password=true -->For reset the selected user password
     * @change_computer=true -->For change the selected user working machine from available computers
     * @change_commonName=true --> For change selected user DN 
     * @password
     *
     * @returns {Object} The result of the API call
     */
    function editUsersAttributes(data) {
      return apiService.patch('/api/ldap/users/',data)
        .error(function () {
          toastService.add('error', gettext('Unable to Edit user Details..'));
        });
    }

  }
}());
