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
    .factory('horizon.app.core.openstack-service-api.backup', backupAPI);

  backupAPI.$inject = [
    'horizon.framework.util.http.service',
    'horizon.framework.widgets.toast.service'
  ];

  /**
   * @ngdoc service
   * @name backupAPI
   * @param {Object} apiService
   * @param {Object} toastService
   */
  function backupAPI(apiService, toastService) {
    var service = {
      getClientdetails:getClientdetails,
      backupClient:backupClient,
      restoreClient:restoreClient,
    };

    return service;

    ///////////////

    // Eventlog

    /**
     * @name getadminEvent
     * @description
     * Get all Event performed by admin users
     *
     * @param none
     *
     * @returns {Object} The result of the API call
     */
    function getClientdetails() {
      return apiService.get('/api/backup/list/')
        .error(function () {
          toastService.add('error', gettext('Unable to retrieve cilent detatils.'));
        });
    }



    function backupClient(data) {
      console.log("inside backup api");
      console.log(data);

      return apiService.post('/api/backup/list/',data)
        .error(function () {
          toastService.add('error', gettext('Unable to Create backup.'));
        });
    }


        function restoreClient(data) {
      console.log("inside restore api");
      console.log(data);

      return apiService.post('/api/restore/list/',data)
        .error(function () {
          toastService.add('error', gettext('Unable to Restore backup.'));
        });
    }


  }
}());

