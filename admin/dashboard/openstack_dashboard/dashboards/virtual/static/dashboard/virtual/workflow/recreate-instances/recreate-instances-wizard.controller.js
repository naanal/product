/**
 * Created by Raja on 6/29/2016.
 */
/*
 *    (c) Copyright 2016 Naanal Technologies Pvt Limited.
 *
 * Licensed under the Apache License, Version 2.0 (the 'License');
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.virtual.workflow.recreate-instances')
    .controller('RecreateInstancesWizardController', RecreateInstancesWizardController);

  RecreateInstancesWizardController.$inject = [
    '$scope',
    'recreateInstancesModel',
    'horizon.dashboard.virtual.workflow.recreate-instances.workflow'
  ];

  function RecreateInstancesWizardController($scope, recreateInstancesModel, recreateInstancesWorkflow) {    
    // Note: we set these attributes on the $scope so that the scope inheritance used all
    // through the launch instance wizard continues to work.
    $scope.workflow = recreateInstancesWorkflow;     // eslint-disable-line angular/controller-as
    $scope.model = recreateInstancesModel;           // eslint-disable-line angular/controller-as
    $scope.model.initialize(true);
    $scope.submit = $scope.model.finishProcess;  // eslint-disable-line angular/controller-as
  }

})();
