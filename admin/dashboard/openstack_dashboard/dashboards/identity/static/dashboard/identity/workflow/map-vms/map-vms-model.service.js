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
    .module('horizon.dashboard.identity.workflow.map-vms')
    .factory('mapVmsModel', mapVmsModel);

  mapVmsModel.$inject = [
    '$q',
    '$log',
    '$rootScope',
    'horizon.app.core.openstack-service-api.ldap',
    'horizon.framework.widgets.toast.service',
    'horizon.framework.widgets.modal-wait-spinner.service'
  ];

  /**
   * @ngdoc service
   * @name mapVmsModel
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
  function mapVmsModel(
    $q,
    $log,
    $rootScope,
    ldapAPI,
    toast,
    Spinner
  ) {

    var initPromise;

    /**
     * @ngdoc model api object
     */

      var model = {

      initializing: false,
      initialized: false,

      newMappingSpec: {},

      /**
       * cloud service properties, they should be READ-ONLY to all UI controllers
       */

      availableUsers: [],
      availableComputers: [],

      /**
       * api methods for UI controllers
       */

      initialize: initialize,
      mapVms: mapVms
    };

    // Local function.
    function initializeNewMappingSpec() {

      model.newMappingSpec = {
        map: [],
        autoMap: ""
      };
    }

    /**
     * @ngdoc method
     * @name mapVmsModel.initialize
     * @returns {promise}
     *
     * @description
     * Send request to get all data to initialize the model.
     */

    function initialize(deep) {
      var deferred, promise;

      // Each time opening launch instance wizard, we need to do this, or
      // we can call the whole methods `reset` instead of `initialize`.
      initializeNewMappingSpec();

      if (model.initializing) {
        promise = initPromise;

      } else if (model.initialized && !deep) {
        deferred = $q.defer();
        promise = deferred.promise;
        deferred.resolve();

      } else {
        model.initializing = true;
        Spinner.showModalSpinner(gettext("Collecting Users and Vms...."));
        promise = $q.all([

          ldapAPI.getAvailableUsers().then(onGetAvailableUsers, noop),
          ldapAPI.getAvailableComputers().then(onGetAvailableComputers, noop)
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

    function mapVms() {
        Spinner.showModalSpinner(gettext("Mapping Vms to Users...."));
        return ldapAPI.mapUserToVm(model.newMappingSpec).then(successMessage,Failed);
    }
      function successMessage(response) {
          Spinner.hideModalSpinner();
          $rootScope.retieveLdapUsers();
          var res = response.data;
          var count = res.length;
          if(res.hasOwnProperty('message'))
               toast.add('danger',res.message)
          var isSuccess = false, isFailed = false, success = [], failed = [];
          var failuremsg = '', successmsg = '';
          for(var i=0;i<count;i++) {
              if(res[i].status == 'success') {
                  isSuccess = true;
                  success.push(res[i].assigned_computer);
              }
              else {
                  isFailed = true;
                  failed.push(res[i].assigned_computer)
              }
          }
          successmsg = success + " are mapped Successfully"
          failuremsg = failed + " have problem in Mapping with the user"
       if(isSuccess == true)
           toast.add('success', successmsg);
       if(isFailed == true)
           toast.add('danger',failuremsg)
    }
      function Failed(){
          Spinner.hideModalSpinner();
      }
    function onGetAvailableUsers(data) {
      model.availableUsers.length = 0; // flush previous data !important
      push.apply(model.availableUsers, data.data);
    }

    function onGetAvailableComputers(data) {
      model.availableComputers.length = 0;  // flush previous data !important
      push.apply(model.availableComputers, data.data);
    }

    return model;
  }

})();
