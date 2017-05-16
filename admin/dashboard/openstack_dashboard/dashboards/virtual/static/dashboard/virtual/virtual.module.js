/*
 *    (c) Copyright 2015 Hewlett-Packard Development Company, L.P.
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

  /**
   * @ngdoc module
   * @ngname horizon.dashboard.virtual
   * @description
   * Dashboard module to host virtual panels.
   */
  angular
    .module('horizon.dashboard.virtual', [
      'horizon.dashboard.virtual.containers',
      'horizon.dashboard.virtual.images',
      'horizon.dashboard.virtual.workflow',
      'horizon.dashboard.virtual.summary',
      'horizon.dashboard.virtual.virtual_machines'
    ])
    .config(config);

  config.$inject = [
    '$provide',
    '$windowProvider'
  ];

  /**
   * @name horizon.dashboard.virtual.basePath
   * @param {Object} $provide
   * @param {Object} $windowProvider
   * @description Base path for the virtual dashboard
   * @returns {undefined} Returns nothing
   */
  function config($provide, $windowProvider) {
    var path = $windowProvider.$get().STATIC_URL + 'dashboard/virtual/';
    $provide.constant('horizon.dashboard.virtual.basePath', path);
  }

})();
