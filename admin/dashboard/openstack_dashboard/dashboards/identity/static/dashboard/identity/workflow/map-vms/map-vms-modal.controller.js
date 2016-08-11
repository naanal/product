/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.map-vms')
    .controller('MapVmsModalController', MapVmsModalController);

  MapVmsModalController.$inject = [
    'horizon.dashboard.identity.workflow.map-vms.modal.service'
  ];

  function MapVmsModalController(modalService) {
    var ctrl = this;

    ctrl.openMapVmsWizard = openMapVmsWizard;

    function openMapVmsWizard(launchContext) {
      modalService.open(launchContext);
    }
  }

})();