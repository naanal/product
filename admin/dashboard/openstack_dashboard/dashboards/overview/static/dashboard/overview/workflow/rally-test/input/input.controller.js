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
    ctrl.insertVolumesize = insertVolumesize;
    ctrl.insertFixednetwork = insertFixednetwork;
    ctrl.insertNo_Times = insertNo_Times;
    ctrl.gatherInputs = gatherInputs;
    ctrl.insertCommon = insertCommon;
    var common_inputs_dup = [];
    $scope.common_inputs = [];

    function gatherInputs(selections) {
      for(var i in selections){
          common_inputs_dup.push.apply(common_inputs_dup, selections[i].inputs);
      }
      $scope.common_inputs = unique(common_inputs_dup);
    }

    function insertCommon (type, value)
    {

        if(type == 'image')
        {
          for( var i=0; i < $scope.model.initializeScenario.selections.length; i++){
            if($scope.model.initializeScenario.selections[i].inputs.indexOf('image') > -1)
              insertImage (value, $scope.model.initializeScenario.selections[i].task);
          }
        }
         if(type == 'flavor')
        {
          for( var i=0; i < $scope.model.initializeScenario.selections.length; i++){
            if($scope.model.initializeScenario.selections[i].inputs.indexOf('flavor') > -1)
              insertFlavor (value, $scope.model.initializeScenario.selections[i].task);
          }
        }

         if(type == 'volume_args')
        {
          for( var i=0; i < $scope.model.initializeScenario.selections.length; i++){
            if($scope.model.initializeScenario.selections[i].inputs.indexOf('volume_args') > -1)
              insertVolumesize (value, $scope.model.initializeScenario.selections[i].task);
          }
        }

         if(type == 'times')
        {
          for( var i=0; i < $scope.model.initializeScenario.selections.length; i++){
            if($scope.model.initializeScenario.selections[i].inputs.indexOf('times') > -1)
              insertNo_Times (value, $scope.model.initializeScenario.selections[i].task);
          }
        }
         if(type == 'fixed_network')
        {
          for( var i=0; i < $scope.model.initializeScenario.selections.length; i++){
            if($scope.model.initializeScenario.selections[i].inputs.indexOf('fixed_network') > -1)
              insertFixednetwork (value, $scope.model.initializeScenario.selections[i].task);
          }
        }


    }

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

  function insertNo_Times (no_times,task){
    
    angular.forEach($scope.model.initializeScenario.selections, function(value1, key1){
      
      angular.forEach($scope.model.initializeScenario.selections[key1], function(value2,key2){
        
        if( Object.keys(value2)[0] == Object.keys(task)[0] ) {
           
          $scope.model.initializeScenario.selections[key1].task[Object.keys(task)[0]][0].runner.times = no_times;
    
         }
      });
    });
    
  };

  function insertVolumesize (volume_args,task){
    
    angular.forEach($scope.model.initializeScenario.selections, function(value1, key1){
      
      angular.forEach($scope.model.initializeScenario.selections[key1], function(value2,key2){
        
        if( Object.keys(value2)[0] == Object.keys(task)[0] ) {
           
          $scope.model.initializeScenario.selections[key1].task[Object.keys(task)[0]][0].args.volume_args.size = volume_args;
    
         }
      });
    });
    
  };

  function insertFixednetwork (fixed_network,task){
    
    angular.forEach($scope.model.initializeScenario.selections, function(value1, key1){
      
      angular.forEach($scope.model.initializeScenario.selections[key1], function(value2,key2){
        
        if( Object.keys(value2)[0] == Object.keys(task)[0] ) {
           
          $scope.model.initializeScenario.selections[key1].task[Object.keys(task)[0]][0].args.fixed_network = fixed_network;
    
         }
      });
    });
    
  };

  function unique(origArr) {
      var newArr = [],
          origLen = origArr.length,
          found, x, y;

      for (x = 0; x < origLen; x++) {
          found = undefined;
          for (y = 0; y < newArr.length; y++) {
              if (origArr[x] === newArr[y]) {
                  found = true;
                  break;
              }
          }
          if (!found) {
              newArr.push(origArr[x]);
          }
      }
      return newArr;
  }

  }
})();
