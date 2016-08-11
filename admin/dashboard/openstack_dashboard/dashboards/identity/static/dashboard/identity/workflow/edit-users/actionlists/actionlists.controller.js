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
    .module('horizon.dashboard.identity.workflow.edit-users')
    .controller('selectActionsController', selectActionsController);

  selectActionsController.$inject = [
    'editUsersModel',
    '$scope'
  ];

  function selectActionsController(editUsersModel,$scope) {
      var ctrl = this;      
      ctrl.selectedUsers = $scope.launchContext.users;
      console.log($scope.launchContext.users.length)       
      for(var i=0;i>$scope.launchContext.users.length;i++){
        console.log(i)
        var temp = { 
          'name':$scope.launchContext.users[i].username,
          'dn': $scope.launchContext.users[i].user_dn,
          'computer': $scope.launchContext.users[i].computer,
         }          
          editUsersModel.newEditSpec.users.push(temp);            
      }      
  }
})();
