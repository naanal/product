/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.edit-users')
    .controller('EditUsersModalController', EditUsersModalController);

  EditUsersModalController.$inject = [
    'horizon.dashboard.identity.workflow.edit-users.modal.service'
  ];

  function EditUsersModalController(modalService) {
    var ctrl = this;

    ctrl.openEditUsersWizard = openEditUsersWizard;

    function openEditUsersWizard(launchContext) {
      modalService.open(launchContext);
    }
  }

})();