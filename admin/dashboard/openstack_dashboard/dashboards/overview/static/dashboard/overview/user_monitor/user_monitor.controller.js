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
   * @ngdoc UserMonitorController
   * @ngController
   *
   * @description
   * Controller for the overview user_monitor table.
   * Serve as the focal point for table actions.
   */
  angular
    .module('horizon.dashboard.overview.user_monitor')
    .controller('overviewUsersMonitorController', overviewUsersMonitorController)
    .controller('UserMonitorController', UserMonitorController)
    .filter('trusted', ['$sce', function ($sce) {
        return function(url) {
            return $sce.trustAsResourceUrl(url);
        };
    }])
    .controller('UserMonitorDetailedController', UserMonitorDetailedController);
    

    UserMonitorController.$inject = [
      '$scope',
      '$rootScope',
      'InfluxService',
      '$interval',
      '$state'
    ];

    UserMonitorDetailedController.$inject = [
      '$scope',
      '$rootScope',
      'InfluxService',
      '$interval',
      '$stateParams'
    ];

    overviewUsersMonitorController.$inject = [
      '$rootScope',
      '$state',
      '$scope',
      'InfluxService',
      '$interval',
      '$q'
    ];

    function overviewUsersMonitorController($rootScope,$state,$scope,InfluxService,$interval,$q) {
      $rootScope.process_group_by = "title";
      $scope.$state=$state;

    $rootScope.retieveUserStatus = function(){

        var query = 'select "user",computer, status, clientname, clientip, last(isloggedin) from usersessions where time > now() - 1m GROUP BY "computer","user"';
        
         InfluxService.getSessionData(query).then(function(response) {
            $rootScope.user_session_status=response;
            u_length = $scope.user_session_status.length;
            var i = 0;
            for( i = 0; i < u_length; i++)
            {
               var c_user = $rootScope.user_session_status[i].tags.user;
               var c_computer = $rootScope.user_session_status[i].tags.computer;
               var query = "select last(cpu_proc_per) as cpu_proc_per ,last(cpu_user_per) as cpu_user_per, last(ram) as ram, last(readops) as readops, last(writeops) as writeops from users_metrics where time > now() - 1m AND \"user\" = '"+ c_user+"' AND computer = '"+c_computer+"'";
              InfluxService.getUserData(query,$rootScope.user_session_status[i]).then(function(response) {
              });

            }

        });
         

      }

      var theInterval = $interval(function(){
          $rootScope.retieveUserStatus();
       }.bind(this), 10000);    

      $scope.$on('$destroy', function () {
          $interval.cancel(theInterval)
      });

      $rootScope.retieveUserStatus();

    }

  function UserMonitorController($scope, $rootScope,InfluxService,$interval,$state) {

      $rootScope.selected = [];
      $rootScope.timeperiod = "1m";
      
      $scope.list_query = {
        order: 'metric.tags.user',
        limit: 15,
        page: 1
      };
       

      $rootScope.retieveUserMetrics = function(){

        var group_by = '"user",computer';
        var query = "select mean(cpu_proc_per) as cpu_proc_per, mean(cpu_user_per) as cpu_user_per, mean(ram) as ram, sum(diskread) as diskread, sum(diskwrite) as diskwrite, sum(readops) as readops, sum(writeops) as writeops from users_metrics where time > now() - " + $rootScope.timeperiod + " GROUP BY " + group_by
        
         InfluxService.getData(query).then(function(response) {
             $scope.user_metrics=response;
             $scope.user_metrics_count = $scope.user_metrics.length;
             $rootScope.selected = [];
        });
         

      }

      var theInterval = $interval(function(){
          $rootScope.retieveUserMetrics();
       }.bind(this), 5000);    

      $scope.$on('$destroy', function () {
          $interval.cancel(theInterval)
      });

      $rootScope.retieveUserMetrics();


    

      $rootScope.retieveTopUserMetrics = function(){  

        var query = 'select+top(cpu_proc_per%2C5)+as+cpu_proc_per+%2Ccomputer%2C"user"%2Ccpu_user_per%2Cram%2Cdiskread%2Cdiskwrite%2Creadops%2Cwriteops+from+users_metrics+where+time+>+now()+-+'+$rootScope.timeperiod+'%3B+select+top(cpu_user_per%2C5)+as+cpu_user_per+%2Ccomputer%2C"user"%2Ccpu_proc_per%2Cram%2Cdiskread%2Cdiskwrite%2Creadops%2Cwriteops+from+users_metrics+where+time+>+now()+-+'+$rootScope.timeperiod+'%3B+select+top(ram%2C5)+as+ram+%2Ccomputer%2C"user"%2Ccpu_user_per%2Ccpu_proc_per%2Cdiskread%2Cdiskwrite%2Creadops%2Cwriteops+from+users_metrics+where+time+>+now()+-+'+$rootScope.timeperiod+'%3B+select+top(diskread%2C5)+as+diskread+%2Ccomputer%2C"user"%2Ccpu_user_per%2Ccpu_proc_per%2Cram%2Cdiskwrite%2Creadops%2Cwriteops+from+users_metrics+where+time+>+now()+-+'+$rootScope.timeperiod+'%3B++select+top(diskwrite%2C5)+as+diskwrite+%2Ccomputer%2C"user"%2Ccpu_user_per%2Ccpu_proc_per%2Cram%2Cdiskread%2Creadops%2Cwriteops+from+users_metrics+where+time+>+now()+-+'+$rootScope.timeperiod+'%3B+select+top(readops%2C5)+as+readops+%2Ccomputer%2C"user"%2Ccpu_user_per%2Ccpu_proc_per%2Cram%2Cdiskread%2Cdiskwrite%2Cwriteops+from+users_metrics+where+time+>+now()+-+'+$rootScope.timeperiod+'%3B+select+top(writeops%2C5)+as+writeops+%2Ccomputer%2C"user"%2Ccpu_user_per%2Ccpu_proc_per%2Cram%2Cdiskread%2Cdiskwrite%2Creadops+from+users_metrics+where+time+>+now()+-+'+$rootScope.timeperiod+';';
         InfluxService.getTopData(query).then(function(response) {
             $scope.top_metrics=response;
        });
         

      }

      var theInterval2 = $interval(function(){
          $rootScope.retieveTopUserMetrics();
       }.bind(this), 8000);    

      $scope.$on('$destroy', function () {
          $interval.cancel(theInterval2)
      });

      $rootScope.retieveTopUserMetrics();

  }


  function UserMonitorDetailedController($scope, $rootScope,InfluxService,$interval,$stateParams) {

    $rootScope.selected = [];
      
      $scope.current_computer = $stateParams.computer;
      $scope.current_user = $stateParams.username;
      $scope.url = "http://192.168.30.200:3000/dashboard/db/user-monitoring?refresh=5s&orgId=1&from=now-5m&to=now&var-vm=" + $scope.current_computer +"&var-user="+ $scope.current_user;
      $scope.list_query = {
        order: 'metric.tags.user',
        limit: 15,
        page: 1
      };

      $rootScope.retieveUserDetailedMetrics = function(){
        var query = "select mean(cpu_proc_per) as cpu_proc_per, mean(cpu_user_per) as cpu_user_per, mean(ram) as ram, sum(diskread) as diskread, sum(diskwrite) as diskwrite, sum(readops) as readops, sum(writeops) as writeops from windows where \"user\" = '"+$scope.current_user+"' AND computer = '"+$scope.current_computer+"' AND time > now() - " + $rootScope.timeperiod + " GROUP BY " + $rootScope.process_group_by;
         InfluxService.getData(query).then(function(response) {
             $scope.user_detailed_metrics=response;
             $scope.user_metrics_count = $scope.user_detailed_metrics.length;
             $rootScope.selected = [];
        });
         

      }

      var theInterval = $interval(function(){
          $rootScope.retieveUserDetailedMetrics();
       }.bind(this), 5000);    

      $scope.$on('$destroy', function () {
          $interval.cancel(theInterval)
      });

      $rootScope.retieveUserDetailedMetrics();

  }

})();
