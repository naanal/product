/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.virtual.workflow.recover-instances')
    .controller('RecoverInstancesModalController', RecoverInstancesModalController);

  RecoverInstancesModalController.$inject = [
    'horizon.dashboard.virtual.workflow.recover-instances.modal.service'
  ];

  function RecoverInstancesModalController(modalService) {
    var ctrl = this;

    ctrl.openRecoverInstancesWizard = openRecoverInstancesWizard;

    function openRecoverInstancesWizard(launchContext) {
      modalService.open(launchContext);      
    }
  }

})();