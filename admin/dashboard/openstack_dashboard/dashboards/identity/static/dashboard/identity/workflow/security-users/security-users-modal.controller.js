/**
 * Securityd by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.security-users')
    .controller('SecurityUsersModalController', SecurityUsersModalController);

  SecurityUsersModalController.$inject = [
    'horizon.dashboard.identity.workflow.security-users.modal.service'
  ];

  function SecurityUsersModalController(modalService) {
    var ctrl = this;

    ctrl.openSecurityUsersWizard = openSecurityUsersWizard;

    function openSecurityUsersWizard(launchContext) {
      modalService.open(launchContext);      
    }
  }

})();