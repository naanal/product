/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.create-groups')
    .controller('CreateGroupsModalController', CreateGroupsModalController);

  CreateGroupsModalController.$inject = [
    'horizon.dashboard.identity.workflow.create-groups.modal.service'
  ];

  function CreateGroupsModalController(modalService) {
    var ctrl = this;

    ctrl.openCreateGroupsWizard = openCreateGroupsWizard;

    function openCreateGroupsWizard(launchContext) {
      modalService.open(launchContext);      
    }
  }

})();