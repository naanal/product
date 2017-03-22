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
    .factory('horizon.app.core.openstack-service-api.ha', haAPI);

  haAPI.$inject = [
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
  function haAPI(apiService, toastService) {
    var service = {
      createStartMigrate: createStartMigrate
      
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
    function createStartMigrate() {
      return apiService.get('/api/ha/high_availability/')
        .error(function () {
          toastService.add('error', gettext('Unable to start Migrate.'));
        });
    }

  }
}());
