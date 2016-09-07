/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  var push = Array.prototype.push;
  var noop = angular.noop;

  /**
   * @ngdoc overview
   * @name horizon.dashboard.virtual.workflow.launch-instance
   *
   * @description
   * Manage workflow of creating server.
   */

  angular
    .module('horizon.dashboard.virtual.workflow.recover-instances')
    .factory('recoverInstancesModel', recoverInstancesModel);

  recoverInstancesModel.$inject = [
    '$q',
    '$log',
    'horizon.framework.widgets.toast.service',
    'horizon.framework.widgets.modal-wait-spinner.service',
    'horizon.app.core.openstack-service-api.nova',
  ];

  /**
   * @ngdoc service
   * @name recoverInstancesModel
   *
   * @param {Object} $q
   * @param {Object} $log
   * @param {Object} ldapAPI
   * @param {Object} settings
   * @param {Object} toast
   * @description
   * This is the M part in MVC design pattern for Map VM
   * wizard workflow. It is responsible for providing data to the
   * view of each step in map vm workflow and collecting
   * user's input from view for  mapping of new vm.  It is
   * also the center point of communication between map vm
   * UI and services API.
   * @returns {Object} The model
   */
  function recoverInstancesModel(
    $q,
    $log,
    toast,
    Spinner,
    novaAPI
  ) {

    var initPromise;

    /**
     * @ngdoc model api object
     */

      var model = {

      initializing: false,
      initialized: false,

      allErrorInstances: [],
      
      recoverInstancesSpec : {},

      initialize: initialize,
      finishProcess: finishProcess
    };

    // Local function.
    function initializeNewRecoverySpec() {

    
      model.recoverInstancesSpec = {
        selectedInstances: []
      };

    }

    /**
     * @ngdoc method
     * @name recoverInstancesModel.initialize
     * @returns {promise}
     *
     * @description
     * Send request to get all data to initialize the model.
     */

    function initialize(deep) {
      var deferred, promise;

      // Each time opening launch instance wizard, we need to do this, or
      // we can call the whole methods `reset` instead of `initialize`.
      initializeNewRecoverySpec();

      if (model.initializing) {
        promise = initPromise;

      } else if (model.initialized && !deep) {
        deferred = $q.defer();
        promise = deferred.promise;
        deferred.resolve();

      } else {
        model.initializing = true;
        Spinner.showModalSpinner(gettext("Collecting Errored Vms...."));
        promise = $q.all([
          novaAPI.getServersListBySearch({"searchterms":["error"],"searchindex":"status"}).then(onGetRecoverServers, noop)
        ]);

        promise.then(onInitSuccess, onInitFail);
      }

      return promise;
    }

    function onInitSuccess() {
      Spinner.hideModalSpinner();
      model.initializing = false;
      model.initialized = true;
    }

    function onInitFail() {
      Spinner.hideModalSpinner();
      model.initializing = false;
      model.initialized = false;
    }

    function finishProcess() {
      
    }

    

    function successMessage(response) {
          Spinner.hideModalSpinner();
    }

    function Failed(){
        Spinner.hideModalSpinner();
    }

    function onGetRecoverServers(res) {
      model.allErrorInstances.length = 0
      push.apply(model.allErrorInstances, res.data.vms);
    }

    return model;
  }

})();
