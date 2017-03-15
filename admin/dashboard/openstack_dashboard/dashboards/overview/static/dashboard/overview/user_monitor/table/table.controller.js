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
   * @ngdoc overviewUsersMonitorController
   * @ngController
   *
   * @description
   * Controller for the overview user_monitor table.
   * Serve as the focal point for table actions.
   */
  angular
    .module('horizon.dashboard.overview.user_monitor')
    .factory('influxdb',influxdb)
    .controller('overviewUsersMonitorController', overviewUsersMonitorController);
    
    influxdb.$inject = ['$resource','$http'];

    overviewUsersMonitorController.$inject = [
      'horizon.framework.widgets.toast.service',
      'horizon.framework.util.i18n.gettext',
      'horizon.framework.widgets.modal-wait-spinner.service',
      '$scope',
      '$rootScope',
      'influxdb',
      '$interval'
    ];

  function influxdb($resource,$http){
     // return $resource('http://192.168.30.51:8086/query?q=select * from windows&db=mydb&u=root&p=root').get();
     delete $http.defaults.headers.common["X-Requested-With"]
          return {
            query: function(query, db){
              var url =
                'http' + '://' + '192.168.30.51' + ':' + '8086' +
                '/query?q=' + query + '&db=' + db +
                '&u=' + 'root' + '&p=' + 'root';
              return $resource(url).get();
            }
          };
    }

  function overviewUsersMonitorController(toast, gettext,Spinner, $scope, $rootScope,influxdb,$interval) {

      $scope.selected = [];
      $scope.timeperiod = "5m";
        $scope.processquery = {
          order: 'time',
          limit: 15,
          page: 1
        };
       
        $scope.computers = ["All","vm-1","vm-2","vm-3"];
        $scope.computer = "All";
        $scope.user = "All";
        $scope.users = ["All","raja","gopal"];
    
       $scope.customFilter = function (data) {
          if (data.status === $scope.selectedOption) {
            return true;
          } else if($scope.selectedOption == 'all') {
              return true;
          } else {
            return false;
          }
        };  

      // $rootScope.$on("callretieveProcessMetrics", function(){
      //      $rootScope.retieveProcessMetrics();
      //   });

      $rootScope.retieveProcessMetrics = function(){

        //Spinner.showModalSpinner(gettext("Retrieving Process...."));
        // var db ="mydb";
        // var host="192.168.30.51";
        // var port = "8086"
        // var query_str = "select mean(cpu) from windows group by process_name";
        // var username = "root";
        // var password = "root";
        // influxdb.query(query_str, db)
        //  .$promise.then(function (result) {
        //     Spinner.hideModalSpinner();
        //     $scope.processes=result.toJSON().results;
        //      $scope.processcount = $scope.processes.length;
        //  });
      //   $scope.processes=[];
      // $scope.processcount = $scope.processes.length;
        //  $scope.processes=influxdb.get();
               influxdb.query('select * from windows where time > now() - 1d', 'mydb')
         .$promise.then(function (result) {
            $scope.processes=result.results[0].series[0].values;
             $scope.processcount = $scope.processes.length;
         });
         
         

      }

      var theInterval = $interval(function(){
          $rootScope.retieveProcessMetrics();
       }.bind(this), 5000);    

      $scope.$on('$destroy', function () {
          $interval.cancel(theInterval)
      });

      $rootScope.retieveProcessMetrics();
  }

})();
