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

var push = Array.prototype.push;

  angular
    .module('horizon.dashboard.virtual.workflow.recreate-instances')
    .controller('downJsonController', downJsonController);

  downJsonController.$inject = [
    'recreateInstancesModel', '$scope',
    'horizon.framework.widgets.toast.service',
    'horizon.framework.widgets.modal-wait-spinner.service',
    'horizon.app.core.openstack-service-api.nova',
    'horizon.app.core.openstack-service-api.cinder',
    '$interval'
  ];

  function downJsonController(recreateInstancesModel,$scope,toast,Spinner,novaAPI,cinderAPI,$interval) {
    
      var ctrl = this;
    $scope.isStarted = false;
    $scope.isBackuped = false;
    $scope.isForceActive = false;
    $scope.isDeleted = false;
    $scope.isRecreated = false;
    $scope.isReattach = false;

    $scope.isBackupInProgress = false;
    $scope.isDeletedInProgress = false;
    $scope.isReattachInProgress = false;
    
    ctrl.deleteServers = deleteServers;

    ctrl.startRecreate = startRecreate;

    function startRecreate(){
      $scope.isStarted = true;
        backupServers();
        deleteServers();
    }

    function backupServers(){
      $scope.isBackupInProgress = true;
      novaAPI.backupServers({"selectedInstances":recreateInstancesModel.recreateInstancesSpec.selectedInstances})
      .then(function(res){
        if(res.status == 204)
        {
          $scope.isBackuped = true;
          $scope.isBackupInProgress =  false;
        }
      },function error(res){

      })
    }

   
    
    function deleteServers(){
      console.log("Deleting....");
      var instances_id = recreateInstancesModel.recreateInstancesSpec.selectedInstances.map(function(obj){return obj.instance_id;});
      novaAPI.deleteServers({"instances_ids":instances_id}).then(function(res){
        if(res.status == 204)
          $scope.isDeletedInProgress = true;
      },function error(){});
    }

    function deletingStatus(){
      $scope.deletedStatus = {"inProgress":[], "inError":[]}
      for(var i=0;i<$scope.selected_instances_status.length;i++){
          if($scope.selected_instances_status[i].instance_status == 'ACTIVE')
            $scope.deletedStatus.inProgress.push($scope.selected_instances_status[i].instance_id)
          else if($scope.selected_instances_status[i].instance_status == 'ERROR')
            $scope.deletedStatus.inError.push($scope.selected_instances_status[i].instance_id)
      }
    }

    function reBuild(){
      
      novaAPI.reCreate({"selectedInstances":recreateInstancesModel.recreateInstancesSpec.selectedInstances}).then(function(res){
        if(res.status == 204)
          $scope.isRecreatedInProgress = true;
      },function error(){});

    }

    function recreatingStatus(){
      $scope.recreatingStatus = {"inProgress":[], "inError":[]}
      for(var i=0;i<$scope.selected_instances_status.length;i++){
          if($scope.selected_instances_status[i].instance_status == 'BUILD')
            $scope.recreatingStatus.inProgress.push($scope.selected_instances_status[i].instance_id)
          else if($scope.selected_instances_status[i].instance_status == 'ERROR')
            $scope.recreatingStatus.inError.push($scope.selected_instances_status[i].instance_id)
      }
    }

    function attachExtraVolumes(){
       novaAPI.attachExtraVolumes({"selectedInstances":recreateInstancesModel.recreateInstancesSpec.selectedInstances}).then(function(res){
        if(res.status == 204)
          $scope.isReattachInProgress = true;
      },function error(){});
    }

    function attachVolumesStatus(){
      cinderAPI.attachVolumesStatus().then(function(res){
        $scope.attachingVolumes = res.data.attaching_volumes;

      },function error(){});
    }

    function OnSuccess(){

    }
    function OnError(){

    }


    function pullServers(){
      var instances_names = recreateInstancesModel.recreateInstancesSpec.selectedInstances.map(function(obj){return obj.instance_name;});
      novaAPI.getServersListBySearch({"searchterms":instances_names,"searchindex":"name"})
      .then(function(response){
          $scope.selected_instances_status = response.data.vms;
          if($scope.isDeletedInProgress == true){
            deletingStatus();
            if($scope.deletedStatus.inProgress.length == 0)
            {
              $scope.isDeletedInProgress = false;
              $scope.isDeleted = true;
              reBuild();
            }
          }
          
          if($scope.isRecreatedInProgress == true){
            recreatingStatus();
            if($scope.recreatingStatus.inProgress.length == 0)
            {
              $scope.isRecreatedInProgress = false;
              $scope.isRecreated = true;
              attachExtraVolumes();
            }
          }

          if($scope.isReattachInProgress == true){
            attachVolumesStatus();
            if($scope.attachingVolumes.length == 0)
            {
              $scope.isReattachInProgress == false;
              $scope.isReattach = true;
            }
          }

      }, function err(response){

      });
    }

    var theInterval = $interval(function(){
      if($scope.isStarted == true)
        pullServers();
     }.bind(this), 1500);    

    $scope.$on('$destroy', function () {
          $interval.cancel(theInterval)
    });
  }
})();
