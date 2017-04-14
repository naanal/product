/**
 * Securityd by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.security-policy')
    .controller('SecurityPolicyModalController', SecurityPolicyModalController);

  SecurityPolicyModalController.$inject = [
    'horizon.dashboard.identity.workflow.security-policy.modal.service'
  ];

  function SecurityPolicyModalController(modalService) {
    var ctrl = this;

    ctrl.openSecurityPolicyWizard = openSecurityPolicyWizard;

    function openSecurityPolicyWizard(launchContext) {
      modalService.open(launchContext);      
    }
  }

})();