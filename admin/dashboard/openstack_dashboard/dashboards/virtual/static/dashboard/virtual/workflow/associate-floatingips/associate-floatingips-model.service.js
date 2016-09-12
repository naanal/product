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
    .module('horizon.dashboard.virtual.workflow.associate-floatingips')
    .factory('associateFloatingipsModel', associateFloatingipsModel);

  associateFloatingipsModel.$inject = [
    '$q',
    '$log',
    'horizon.framework.widgets.toast.service',
    'horizon.framework.widgets.modal-wait-spinner.service',
    'horizon.app.core.openstack-service-api.nova',
    'horizon.app.core.openstack-service-api.network',
  ];

  /**
   * @ngdoc service
   * @name associateFloatingipsModel
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
  function associateFloatingipsModel(
    $q,
    $log,
    toast,
    Spinner,
    novaAPI,
    networkAPI
  ) {

    var initPromise;

    /**
     * @ngdoc model api object
     */

      var model = {

      initializing: false,
      initialized: false,

      vmHadNoIps: [],
      
      availablePools: [],

      newspec : {},

      getAvailableIpsInRange: getAvailableIpsInRange,
      availableIpsInRange : [],

      initialize: initialize,
      allocateIps: allocateIps
    };

    // Local function.
    function initializeNewRecoverySpec() {

    
      model.newspec = {
        selectedInstances: [],
        selectedPoolRange: "",
        poolId: "",
        method: "auto",
      };

    }

    /**
     * @ngdoc method
     * @name associateFloatingipsModel.initialize
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
        Spinner.showModalSpinner(gettext("Collecting Vms had no Floating Ips...."));
        promise = $q.all([
          novaAPI.getInstancesHadNoFloatingIps().then(onGetVmsNoIps, noop),
          networkAPI.getFloatingIpPoolsRange().then(onGetPools, noop)
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

    function allocateIps() {
      Spinner.showModalSpinner(gettext("Associating Ips..."));
      return novaAPI.createManyFloatingIps(model.newspec).then(successMessage,Failed);
    }

    

    function successMessage(response) {
          Spinner.hideModalSpinner();
          toast.add(response.data.status, response.data.msg);
    }

    function Failed(){
        Spinner.hideModalSpinner();
        toast.add('danger',"There is some problem")
    }

    function onGetVmsNoIps(res) {
      model.vmHadNoIps.length = 0;
      push.apply(model.vmHadNoIps, res.data.instances_no_fips);
    }

    function onGetPools(res) {
      model.availablePools.length = 0;
      push.apply(model.availablePools, res.data);
    }

    function getAvailableIpsInRange(){
      var tmp = {}
      tmp['selected_range'] = model.newspec.selectedPoolRange;
      tmp['instance_count'] = model.newspec.selectedInstances.length;
      networkAPI.getAvailableIpsInSelectedRange(tmp).then(function(res){
        model.availableIpsInRange.length = 0;
        model.availableIpsInRange = res.data.available_ips;
      });
    }
    return model;
  }

})();
