/*
 * Copyright 2016 Naanal technologies Pvt Limited
 * (c) Copyright 2015 ThoughtWorks Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
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
   * @name RallyTestScenariosController
   * @description
   * The `RallyTestScenariosController` controller provides functions for
   * configuring the Scenarios step of the Launch Instance Wizard.
   *
   */
  angular
    .module('horizon.dashboard.overview.workflow.rally-test')
    .controller('RallyTestScenariosController', RallyTestScenariosController);

  RallyTestScenariosController.$inject = [
    '$scope',
    'horizon.dashboard.overview.workflow.rally-test.basePath',
    'RallyTestModel'
  ];

  function RallyTestScenariosController($scope,basePath,RallyTestModel) {
    var ctrl = this
    ctrl.Schema = $scope.model.orginalSchema.rallytask;
    
    
    // toggle selection for a given fruit by name
    $scope.toggleSelection = function toggleSelection(task) {
      var idx = $scope.model.initializeScenario.selections.indexOf(task);
      
      // is currently selected
      if (idx > -1) {
        $scope.model.initializeScenario.selections.splice(idx, 1);
      }
      
      // is newly selected
      else {
        $scope.model.initializeScenario.selections.push(task);
      }
    };

  }
})();
