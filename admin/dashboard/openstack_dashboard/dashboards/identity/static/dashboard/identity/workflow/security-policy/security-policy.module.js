/**
 * Securityd by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.security-policy', [])
    .config(config)
    .constant('horizon.dashboard.identity.workflow.security-policy.modal-spec', {
      backdrop: 'static',
      size: 'lg',
      controller: 'ModalContainerController',
      template: '<wizard class="wizard" ng-controller="SecurityPolicyWizardController"></wizard>'
    })
    
  config.$inject = [
    '$provide',
    '$windowProvider'
  ];

  /**
   * @name config
   * @param {Object} $provide
   * @param {Object} $windowProvider
   * @description Base path for the security-policy code
   * @returns {undefined} No return value
   */
  function config($provide, $windowProvider) {
    var path = $windowProvider.$get().STATIC_URL + 'dashboard/identity/workflow/security-policy/';
    $provide.constant('horizon.dashboard.identity.workflow.security-policy.basePath', path);
  }

})();
