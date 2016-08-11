/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.create-users', [])
    .config(config)
    .constant('horizon.dashboard.identity.workflow.create-users.modal-spec', {
      backdrop: 'static',
      size: 'lg',
      controller: 'ModalContainerController',
      template: '<wizard class="wizard" ng-controller="CreateUsersWizardController"></wizard>'
    })
    
  config.$inject = [
    '$provide',
    '$windowProvider'
  ];

  /**
   * @name config
   * @param {Object} $provide
   * @param {Object} $windowProvider
   * @description Base path for the create-users code
   * @returns {undefined} No return value
   */
  function config($provide, $windowProvider) {
    var path = $windowProvider.$get().STATIC_URL + 'dashboard/identity/workflow/create-users/';
    $provide.constant('horizon.dashboard.identity.workflow.create-users.basePath', path);
  }

})();
