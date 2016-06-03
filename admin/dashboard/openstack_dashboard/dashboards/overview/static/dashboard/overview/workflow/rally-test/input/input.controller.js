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
   * @name RallyTestInputController
   * @description
   * The `RallyTestInputController` controller provides functions for
   * configuring the Scenarios step of the Launch Instance Wizard.
   *
   */
  angular
    .module('horizon.dashboard.overview.workflow.rally-test')
    .controller('RallyTestInputController', RallyTestInputController);

  RallyTestInputController.$inject = [
    '$scope',
    'RallyTestModel'
  ];

  function RallyTestInputController($scope,RallyTestModel) {
    var ctrl = this;
    ctrl.insertImage = insertImage;
    ctrl.insertFlavor = insertFlavor;


  function insertImage (image,task){
    
    angular.forEach($scope.model.initializeScenario.selections, function(value1, key1){
      
      angular.forEach($scope.model.initializeScenario.selections[key1], function(value2,key2){
        
        if( Object.keys(value2)[0] == Object.keys(task)[0] ) {
     
          $scope.model.initializeScenario.selections[key1].task[Object.keys(task)[0]][0].args.image.name = image;
    
         }
      });
    });
    
  };


  function insertFlavor (flavor,task){
    
    angular.forEach($scope.model.initializeScenario.selections, function(value1, key1){
      
      angular.forEach($scope.model.initializeScenario.selections[key1], function(value2,key2){
        
        if( Object.keys(value2)[0] == Object.keys(task)[0] ) {
           
          $scope.model.initializeScenario.selections[key1].task[Object.keys(task)[0]][0].args.flavor.name = flavor;
    
         }
      });
    });
    
  };

  }
})();
