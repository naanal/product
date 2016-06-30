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
    'mapVmsModel'
  ];

  function MapVmsComputersController(mapVmsModel) {
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

  }
})();
