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
    .module('horizon.dashboard.virtual.workflow.recreate-instances')
    .controller('selectErrorVmsController', selectErrorVmsController);

  selectErrorVmsController.$inject = [
    'recreateInstancesModel', '$scope', '$timeout'
  ];

  function selectErrorVmsController(recreateInstancesModel,$scope,$timeout) {
    var ctrl = this;
   console.log("hiiiiiiiiiii");
   console.log(recreateInstancesModel.recreateInstancesSpec.selectedInstances.length);
    $scope.toggleVmsLists = function (item, list) {
      var idx = list.indexOf(item);
      if (idx > -1) {
        list.splice(idx, 1);
      }
      else {
        list.push(item);
      }
       

    };
    
    $scope.download_json = function () {
      console.log("download json");
    }
  
    $scope.exists = function (item, list) {
      return list.indexOf(item) > -1;
    };

    $scope.isIndeterminate = function() {
      return (recreateInstancesModel.recreateInstancesSpec.selectedInstances.length !== 0 &&
          recreateInstancesModel.recreateInstancesSpec.selectedInstances.length !== recreateInstancesModel.allErrorInstances.length);
    };

    $scope.isChecked = function() {
      return recreateInstancesModel.recreateInstancesSpec.selectedInstances.length === recreateInstancesModel.allErrorInstances.length;
    };

    $scope.toggleAll = function() {
      if (recreateInstancesModel.recreateInstancesSpec.selectedInstances.length === recreateInstancesModel.allErrorInstances.length) {
        recreateInstancesModel.recreateInstancesSpec.selectedInstances = [];
      } else if (recreateInstancesModel.recreateInstancesSpec.selectedInstances.length === 0 || recreateInstancesModel.recreateInstancesSpec.selectedInstances.length > 0) {
        recreateInstancesModel.recreateInstancesSpec.selectedInstances = recreateInstancesModel.allErrorInstances.slice(0);
      }
    };

   

  }
})();
