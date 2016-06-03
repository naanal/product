/**
 * Copyright 2015, Rackspace, US, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the 'License'); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */
(function () {
  'use strict';

  angular
    .module('horizon.app.core.openstack-service-api')
    .factory('horizon.app.core.openstack-service-api.rally', rallyAPI);

  rallyAPI.$inject = [
    'horizon.framework.util.http.service',
    'horizon.framework.widgets.toast.service',
    'horizon.dashboard.overview.workflow.rally-test.basePath'
  ];

  /**
   * @ngdoc service
   * @name rallyAPI
   * @param {Object} apiService
   * @param {Object} toastService
   * @description Provides direct pass through to Swift with NO abstraction.
   * @returns {Object} The service
   */
  function rallyAPI(apiService, toastService, basePathOfJsonFile) {
    var service = {
      rallyTasksScenarios: rallyTasksScenarios,
      rallyStartTest : rallyStartTest,
      rallyViewHtml: rallyViewHtml
    };

    return service;

    /**
     * @name getInfo
     * @description
     * Lists the activated capabilities for this version of the OpenStack
     * Object Storage API.
     *
     * @returns {Object} The result of the object passed to the Swift /info/ call.
     *
     */
    function rallyTasksScenarios() {
      return apiService.get(basePathOfJsonFile+'scenario/scenarios.json')
        .error(function () {
          toastService.add('error', gettext('Unable to get Sample Scenarios.'));
        });
    }

    function rallyStartTest(taskdata) {
      return apiService.post('/api/rally/task/', taskdata)
        .error(function () {
          toastService.add('error', gettext('Unable to Run The Task.'));
        });
    }

    function rallyViewHtml() {
      return apiService.get('/api/rally/html/')
        .error(function () {
          toastService.add('error', gettext('Unable to View Html.'));
        });
    }

  }
}());
