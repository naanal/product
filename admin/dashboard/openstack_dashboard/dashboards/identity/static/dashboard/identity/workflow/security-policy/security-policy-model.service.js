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
    .module('horizon.dashboard.identity.workflow.security-policy')
    .factory('securityPolicyModel', securityPolicyModel);

  securityPolicyModel.$inject = [
    '$q',
    '$log',
    '$rootScope',
    'horizon.app.core.openstack-service-api.ldap',
    'horizon.framework.widgets.toast.service',
    'horizon.framework.widgets.modal-wait-spinner.service',
  ];

  /**
   * @ngdoc service
   * @name securityPolicyModel
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
  function securityPolicyModel(
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

      newUserSpec: {},
      singleUser: {},
      isCurrentModelPushed: false,
      /**
       * cloud service properties, they should be READ-ONLY to all UI controllers
       */
        availableComputers: [],
      /**
       * api methods for UI controllers
       */

      initialize: initialize,
      securityPolicy: securityPolicy
    };

    // Local function.
    function initializeNewMappingSpec() {
      model.group="",
      model.usernames=[],

      model.singleUser = {},
      model.newUserSpec = {
        user_dn: [],
        group_dn:"",
        create_group: false,
        delete_group: false,
        add_to_group: "False"
      };

    }

    /**
     * @ngdoc method
     * @name securityPolicyModel.initialize
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

        promise = $q.all([

        ]);

        promise.then(onInitSuccess, onInitFail);
      }

      return promise;
    }

    function onInitSuccess() {
      model.initializing = false;
      model.initialized = true;
    }

    function onInitFail() {
      model.initializing = false;
      model.initialized = false;
    }

    function securityPolicy() {    
      
      model.newUserSpec.group_dn=model.group.group.dn;
      console.log("input");
      console.log(model.newUserSpec);
      console.log(model.newUserSpec.user_dn);
      console.log(model.newUserSpec.add_to_group);
     
      return ldapAPI.addGroup(model.newUserSpec).then(successMessage,Failed);
    }
      function successMessage(response) {
          Spinner.hideModalSpinner();
           $rootScope.$emit("callretieveLdapUsers", {});
          var res = response.data;
          for(var i=0;i<res.length;i++) {
              if (res[i].status.includes("success"))
                  toast.add('success', res[i].status);
              else
                  toast.add('danger', res[i].status);
          }
    }
      function Failed(){
          Spinner.hideModalSpinner();
      }
    return model;
  }

})();
