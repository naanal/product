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
    .module('horizon.dashboard.identity.workflow.create-users')
    .controller('selectComputersController', selectComputersController);

  selectComputersController.$inject = [
    'createUsersModel',
      '$scope', 
      'horizon.app.core.openstack-service-api.ldap',
      'horizon.framework.widgets.modal-wait-spinner.service',
      '$log'
  ];

  function selectComputersController(createUsersModel,$scope,ldapAPI,Spinner,$log) {
      var ctrl = this;
     
      ctrl.getVMs = getVMs;
      function getVMs(){
        Spinner.showModalSpinner(gettext("Collecting available Vms...."));
                ldapAPI.getAvailableComputers()
                    .then(function(res){
                        Spinner.hideModalSpinner();
                        createUsersModel.availableComputers.length = 0;  // flush previous data !important
                        Array.prototype.push.apply(createUsersModel.availableComputers, res.data);
                        $scope.vmCount = createUsersModel.availableComputers.length;
                         var isExist = createUsersModel.newUserSpec.users.map(function(e){ return e.username;}).indexOf(createUsersModel.singleUser.username);
                        if(isExist == -1)
                          createUsersModel.newUserSpec.users.push(createUsersModel.singleUser);
                        createUsersModel.isCurrentModelPushed = true;
                        $scope.isShortage = createUsersModel.newUserSpec.users.length > $scope.vmCount;
                        if($scope.isShortage == true){
                            createUsersModel.newUserSpec.isAssignVm = "False";
                        }

                    },function(err){
                         Spinner.hideModalSpinner();
                    });
        
        
        ctrl.computerSearch= computerSearch;
        ctrl.computerTextChange=computerTextChange;
        ctrl.selectedComputerChange=selectedComputerChange;
        $scope.selectedVms = new Array(createUsersModel.availableComputers.length);
        function computerSearch (query) {
            var results = query ? createUsersModel.availableComputers.filter( createFilterForComputer(query) ) : createUsersModel.availableComputers, deferred;
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
  }
})();
