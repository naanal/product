/*
 *    (c) Copyright 2016 Rackspace US, Inc
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
   * @ngdoc controller
   *
   * @name horizon.dashboard.overview.virtual_monitor.VirtualMonitorController
   *
   * @description
   * Controller for the interface around a list of virtual_monitor for a single account.
   */
  angular
    .module('horizon.dashboard.overview.virtual_monitor')
    .controller('horizon.dashboard.overview.virtual_monitor.VirtualMonitorController', VirtualMonitorController);

  VirtualMonitorController.$inject = [
    'horizon.framework.widgets.toast.service',
    '$scope',
    'horizon.app.core.openstack-service-api.nova',
    'horizon.framework.widgets.modal-wait-spinner.service',
    'VMInfluxService',
    '$interval'
  ];

  function VirtualMonitorController(toast, $scope,novaAPI,Spinner,VMInfluxService, $interval)
  {
      Spinner.showModalSpinner(gettext("Monitoring Vms...."));
      $scope.retriveVMMetrics = function () {

        VMInfluxService.getVMState()
          .then(function(res){
              Spinner.hideModalSpinner();
              $scope.machines = res.vms;
              for(var i=0; i< $scope.machines.length; i++){
                
                if($scope.machines[i].health ==1 || ($scope.machines[i].ping_status == true && $scope.machines[i].rdp_status == false))
                {
                  var c_computer = $scope.machines[i].instance_name;
                  var query = 'SELECT last(Percent_Processor_Time) AS CPU_Proc, last(Percent_User_Time) AS CPU_User, last(Available_Bytes) AS RAM_Available, last(Disk_Bytes_persec) as disktotal, last(Disk_Read_Bytes_persec) as diskread, last(Disk_Write_Bytes_persec) as diskwrite, last(Percent_Disk_Time) AS Disk_Perc, last("Avg._Disk_sec/Transfer") AS Disk_Sec, last(Current_Disk_Queue_Length) AS Disk_Queue_Length, last(Bytes_Received_persec) AS NW_Received, last(Bytes_Sent_persec) as NW_Sent, last(Bytes_Total_persec) as NW_Total, last(Active_Sessions) as Active_Sessions FROM winn where time > now() - 1m AND host = \'' + c_computer + '\' GROUP BY host';
                  VMInfluxService.getVMData(query,$scope.machines[i]).then(function(response) {

                  });
                }
              }
          },function(error){
              Spinner.hideModalSpinner();
          });
      }

      var theInterval = $interval(function(){
          $scope.retriveVMMetrics();
      }.bind(this), 5000);
      $scope.retriveVMMetrics();
  }
})();