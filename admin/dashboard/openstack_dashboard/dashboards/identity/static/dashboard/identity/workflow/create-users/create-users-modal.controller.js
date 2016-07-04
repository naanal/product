/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.create-users')
    .controller('CreateUsersModalController', CreateUsersModalController);

  CreateUsersModalController.$inject = [
    'horizon.dashboard.identity.workflow.create-users.modal.service'
  ];

  function CreateUsersModalController(modalService) {
    var ctrl = this;

    ctrl.openCreateUsersWizard = openCreateUsersWizard;

    function openCreateUsersWizard(launchContext) {
      modalService.open(launchContext);
    }
  }

})();