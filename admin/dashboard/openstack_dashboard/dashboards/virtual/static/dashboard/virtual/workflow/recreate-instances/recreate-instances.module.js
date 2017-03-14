/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.virtual.workflow.recreate-instances', [])
    .config(config)
    .constant('horizon.dashboard.virtual.workflow.recreate-instances.modal-spec', {
      backdrop: 'static',
      size: 'lg',
      controller: 'ModalContainerController',
      template: '<wizard class="wizard" ng-controller="RecreateInstancesWizardController"></wizard>'
    })
    
  config.$inject = [
    '$provide',
    '$windowProvider'
  ];

  /**
   * @name config
   * @param {Object} $provide
   * @param {Object} $windowProvider
   * @description Base path for the recover-instances code
   * @returns {undefined} No return value
   */
  function config($provide, $windowProvider) {
    var path = $windowProvider.$get().STATIC_URL + 'dashboard/virtual/workflow/recreate-instances/';
    $provide.constant('horizon.dashboard.virtual.workflow.recreate-instances.basePath', path);
  }

})();
