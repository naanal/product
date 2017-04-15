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


  /**
   * @ngdoc horizon.dashboard.overview.users
   * @ngModule
   *
   * @description
   * Provides all of the services and widgets required
   * to support and display the overview users panel.
   */
  angular
    .module('horizon.dashboard.overview.user_monitor', ['ui.router'])
    .run(run)
    .config(config);

    run.$inject = [
      '$rootScope'
    ];

    config.$inject = [
      '$provide',
      '$windowProvider',
      '$stateProvider',
      '$urlRouterProvider'
    ];

      function run($rootScope) {
                $rootScope.host = "";
      }

      function config($provide, $windowProvider,$stateProvider, $urlRouterProvider) {
        var path = $windowProvider.$get().STATIC_URL + 'dashboard/overview/user_monitor/';
        $provide.constant('horizon.dashboard.overview.user_monitor.basePath', path);
        $urlRouterProvider.otherwise("/");
        $stateProvider
            .state('users', {
                url: "/",
                templateUrl: path + "views/user_usage_list.html"
            })
            .state('users_detail', {
                url: "/:computer/:username",
                templateUrl: path + "views/user_usage_detail.html"
            })

      }

})();


