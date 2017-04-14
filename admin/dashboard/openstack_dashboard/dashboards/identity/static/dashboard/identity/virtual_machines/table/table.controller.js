/**
 * Copyright 2015 IBM Corp.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function() {
  'use strict';

  /**
   * @ngdoc identityevirtualmachineTableController
   * @ngController
   *
   * @description
   * Controller for the identity vms table.
   * Serve as the focal point for table actions.
   */
  angular
    .module('horizon.dashboard.identity.virtual_machines')
    .controller('identityevirtualmachineTableController', identityevirtualmachineTableController);

  identityevirtualmachineTableController.$inject = [
    'horizon.framework.widgets.toast.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.app.core.openstack-service-api.nova',
    'horizon.framework.widgets.modal-wait-spinner.service',
    '$scope',
    '$rootScope'
  ];

  function identityevirtualmachineTableController(toast, gettext,novaAPI,Spinner, $scope, $rootScope) {
      
      $rootScope.retieveAdminEvents = function(){
           Spinner.showModalSpinner(gettext("Retrieving instances status...."));
        novaAPI.instances_rdpcheck()
          .then(function(res){
              Spinner.hideModalSpinner();
              $scope.vms = res.data['vms'];
              $scope.vmcount = $scope.vms.length;
              console.log($scope.vms)
              console.log($scope.vmcount)
              console.log(typeof($scope.vms['vms']))
          },function(error){
              Spinner.hideModalSpinner();
          });
      }
      $rootScope.retieveAdminEvents();

       $scope.restart = function (instance_id) {
      console.log("download json");
      console.log(instance_id);
      var obj = new Object();
      obj.instance_id = instance_id;       
      var jsonString= JSON.stringify(obj);
      console.log(jsonString);
      // var instances_restart = [];
      // instances_restart.push({
      //             key:   "instance_id",
      //             value: instance_id
      //         });
      // console.log(instances_restart);

       novaAPI.instance_hardreboot(obj).then(function(res){       
      },function error(){});
    }

      
  }

})();
