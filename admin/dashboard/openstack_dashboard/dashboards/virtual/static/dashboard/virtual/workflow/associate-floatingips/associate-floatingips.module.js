/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.virtual.workflow.associate-floatingips', [])
    .config(config)
    .constant('horizon.dashboard.virtual.workflow.associate-floatingips.modal-spec', {
      backdrop: 'static',
      size: 'lg',
      controller: 'ModalContainerController',
      template: '<wizard class="wizard" ng-controller="AssociateFloatingipsWizardController"></wizard>'
    })
    
  config.$inject = [
    '$provide',
    '$windowProvider'
  ];

  /**
   * @name config
   * @param {Object} $provide
   * @param {Object} $windowProvider
   * @description Base path for the associate-floatingips code
   * @returns {undefined} No return value
   */
  function config($provide, $windowProvider) {
    var path = $windowProvider.$get().STATIC_URL + 'dashboard/virtual/workflow/associate-floatingips/';
    $provide.constant('horizon.dashboard.virtual.workflow.associate-floatingips.basePath', path);
  }

})();
