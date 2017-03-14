/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.virtual.workflow.recreate-instances')
    .controller('RecreateInstancesModalController', RecreateInstancesModalController);

  RecreateInstancesModalController.$inject = [
    'horizon.dashboard.virtual.workflow.recreate-instances.modal.service'
  ];

  function RecreateInstancesModalController(modalService) {
    var ctrl = this;

    ctrl.openRecreateInstancesWizard = openRecreateInstancesWizard;

    function openRecreateInstancesWizard(launchContext) {
      modalService.open(launchContext);      
    }
  }

})();
