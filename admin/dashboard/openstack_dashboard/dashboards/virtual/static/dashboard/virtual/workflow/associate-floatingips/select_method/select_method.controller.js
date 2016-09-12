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
    .module('horizon.dashboard.virtual.workflow.associate-floatingips')
    .controller('selectMethodController', selectMethodController);

  selectMethodController.$inject = [
    'associateFloatingipsModel', '$scope', '$timeout','$log'
  ];

  function selectMethodController(associateFloatingipsModel,$scope,$timeout,$log) {
    var ctrl = this;

    
      ctrl.changedMode = changeMode;
      function changeMode(){
          // if(mapVmsModel.newMappingSpec.autoMap == 'True')
          // {
          //     for(var i =0 ; i < mapVmsModel.newMappingSpec.map.length; i++)
          //      delete  mapVmsModel.newMappingSpec.map[i].computer;

          // }
      }
      
     
      ctrl.ipSearch= ipSearch;
      ctrl.ipTextChange=ipTextChange;
      ctrl.selectedIpChange=selectedIpChange;
      $scope.selectedIps = new Array(associateFloatingipsModel.availableIpsInRange.length);
      function ipSearch (query) {
          var results = query ? associateFloatingipsModel.availableIpsInRange.filter( createFilterForIP(query) ) : associateFloatingipsModel.availableIpsInRange, deferred;
          var newresults = angular.copy(results);
          for (var i=0; i<$scope.selectedIps.length; i++)
          {
            var existIndex = newresults.map(function(e) { return e; }).indexOf($scope.selectedIps[i]);
            if(existIndex != -1)
              newresults.splice(existIndex,1);
          }
          return newresults;
      }
      function createFilterForIP(query) {
              query=query.toUpperCase();
              return function filterFn(ip) {
                  return (ip.indexOf(query) === 0);
               };
      }
      function ipTextChange(text) {
        $log.info('Text changed to ' + text);
      }
      function selectedIpChange(vm,item,index) {
        console.log(index);
        if(item != undefined){
        $scope.selectedIps[index] = item;
         vm.prefered_ip = item;
        $log.info('Item changed to ' + JSON.stringify(item));
        }
        else
        {
          $scope.selectedIps[index]=null;
          ipSearch('');
        }
      } 

  }
})();
