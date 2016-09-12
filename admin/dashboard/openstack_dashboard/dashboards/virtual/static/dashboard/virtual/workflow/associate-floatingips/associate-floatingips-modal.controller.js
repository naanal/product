/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.virtual.workflow.associate-floatingips')
    .controller('AssociateFloatingipsModalController', AssociateFloatingipsModalController);

  AssociateFloatingipsModalController.$inject = [
    'horizon.dashboard.virtual.workflow.associate-floatingips.modal.service'
  ];

  function AssociateFloatingipsModalController(modalService) {
    var ctrl = this;

    ctrl.openAssociateFloatingipsWizard = openAssociateFloatingipsWizard;

    function openAssociateFloatingipsWizard(launchContext) {
      modalService.open(launchContext);      
    }
  }

})();