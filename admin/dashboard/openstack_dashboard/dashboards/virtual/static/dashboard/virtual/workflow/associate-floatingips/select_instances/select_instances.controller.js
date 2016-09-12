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
    .controller('selectInstancesController', selectInstancesController);

  selectInstancesController.$inject = [
    'associateFloatingipsModel', '$scope', '$timeout'
  ];

  function selectInstancesController(associateFloatingipsModel,$scope,$timeout) {
    var ctrl = this;

    $scope.toggleVmsLists = function (item, list) {
      var idx = list.indexOf(item);
      if (idx > -1) {
        list.splice(idx, 1);
      }
      else {
        list.push(item);
      }
    };

    $scope.exists = function (item, list) {
      return list.indexOf(item) > -1;
    };

    $scope.isIndeterminate = function() {
      return (associateFloatingipsModel.newspec.selectedInstances.length !== 0 &&
          associateFloatingipsModel.newspec.selectedInstances.length !== associateFloatingipsModel.vmHadNoIps.length);
    };

    $scope.isChecked = function() {
      return associateFloatingipsModel.newspec.selectedInstances.length === associateFloatingipsModel.vmHadNoIps.length;
    };

    $scope.toggleAll = function() {
      if (associateFloatingipsModel.newspec.selectedInstances.length === associateFloatingipsModel.vmHadNoIps.length) {
        associateFloatingipsModel.newspec.selectedInstances = [];
      } else if (associateFloatingipsModel.newspec.selectedInstances.length === 0 || associateFloatingipsModel.newspec.selectedInstances.length > 0) {
        associateFloatingipsModel.newspec.selectedInstances = associateFloatingipsModel.vmHadNoIps.slice(0);
      }
    };

  }
})();
