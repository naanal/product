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

  angular
    .module('horizon.dashboard.identity.workflow.map-vms')
    .controller('MapVmsComputersController', MapVmsComputersController);

  MapVmsComputersController.$inject = [
    'mapVmsModel',
    '$scope',
    '$log'
  ];

  function MapVmsComputersController(mapVmsModel,$scope,$log) {
      var ctrl = this;
      ctrl.availableCom = mapVmsModel.availableComputers;
      ctrl.changedMode = changeMode;
      function changeMode(){
          if(mapVmsModel.newMappingSpec.autoMap == 'True')
          {
              for(var i =0 ; i < mapVmsModel.newMappingSpec.map.length; i++)
               delete  mapVmsModel.newMappingSpec.map[i].computer;

          }
      }
      
     
      ctrl.computerSearch= computerSearch;
      ctrl.computerTextChange=computerTextChange;
      ctrl.selectedComputerChange=selectedComputerChange;
      $scope.selectedVms = new Array(mapVmsModel.availableComputers.length);
      function computerSearch (query) {
          var results = query ? mapVmsModel.availableComputers.filter( createFilterForComputer(query) ) : mapVmsModel.availableComputers, deferred;
          var newresults = angular.copy(results);
          for (var i=0; i<$scope.selectedVms.length; i++)
          {
            var existIndex = newresults.map(function(e) { return e.computername; }).indexOf($scope.selectedVms[i]);
            if(existIndex != -1)
              newresults.splice(existIndex,1);
          }
          return newresults;
      }
      function createFilterForComputer(query) {
              query=query.toUpperCase();
              return function filterFn(computer) {
                  return (computer.computername.indexOf(query) === 0);
               };
      }
      function computerTextChange(text) {
        $log.info('Text changed to ' + text);
      }
      function selectedComputerChange(user,item,index) {
        console.log(index);
        if(item != undefined){
        $scope.selectedVms[index] = item.computername;
        user.computer = item.computername;
        $log.info('Item changed to ' + JSON.stringify(item));
        }
        else
        {
          $scope.selectedVms[index]=null;
          computerSearch('');
        }
      } 

  }
})();
