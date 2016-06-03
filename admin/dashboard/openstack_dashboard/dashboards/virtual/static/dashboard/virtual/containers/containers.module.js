/**
 *    (c) Copyright 2015 Rackspace, US, Inc.
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
   * @ngdoc overview
   * @ngname horizon.dashboard.virtual.containers
   *
   * @description
   * Provides the services and widgets required
   * to support and display the virtual containers panel.
   */
  angular
    .module('horizon.dashboard.virtual.containers', ['ngRoute'])
    .config(config);

  config.$inject = [
    '$provide',
    '$routeProvider',
    '$windowProvider'
  ];

  /**
   * @name horizon.dashboard.virtual.containers.basePath
   * @description Base path for the virtual dashboard
   */
  function config($provide, $routeProvider, $windowProvider) {
    var path = $windowProvider.$get().STATIC_URL + 'dashboard/virtual/containers/';
    $provide.constant('horizon.dashboard.virtual.containers.basePath', path);

    var baseRoute = 'virtual/containers/';
    $provide.constant('horizon.dashboard.virtual.containers.baseRoute', baseRoute);

    var containerRoute = baseRoute + 'container/';
    $provide.constant('horizon.dashboard.virtual.containers.containerRoute', containerRoute);

    $routeProvider
      .when('/' + baseRoute, {
        templateUrl: path + 'select-container.html'
      })
      .when('/' + containerRoute + ':container', {
        templateUrl: path + 'objects.html'
      })
      .when('/' + containerRoute + ':container/:folder*', {
        templateUrl: path + 'objects.html'
      });
  }
})();
