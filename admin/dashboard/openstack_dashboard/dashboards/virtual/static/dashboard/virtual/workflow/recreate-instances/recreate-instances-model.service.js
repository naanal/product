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
    .module('horizon.dashboard.virtual.workflow.recreate-instances')
    .factory('recreateInstancesModel', recreateInstancesModel);

  recreateInstancesModel.$inject = [
    '$q',
    '$log',
    'horizon.framework.widgets.toast.service',
    'horizon.framework.widgets.modal-wait-spinner.service',
    'horizon.app.core.openstack-service-api.nova',
    'horizon.app.core.openstack-service-api.cinder',
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
  function recreateInstancesModel(
    $q,
    $log,
    toast,
    Spinner,
    novaAPI,
    cinderAPI
  ) {

    var initPromise;

    /**
     * @ngdoc model api object
     */

      var model = {

      initializing: false,
      initialized: false,

      allErrorInstances: [],
      volumeSnapshots: [],
      
      recreateInstancesSpec : {},

      initialize: initialize,
      finishProcess: finishProcess,
      createJson:createJson
    };

    // Local function.
    function initializeNewRecreateSpec() {

    
      model.recreateInstancesSpec = {
        selectedInstances: []
      };
      model.volumesnapshot_list={
        volume_list:[]
        
      };

    }
    
    function createJson(){
       console.log("download json");
       var instances = model.recreateInstancesSpec.selectedInstances;
       console.log(instances);
       novaAPI.createJsoninNova({"selectedInstances":instances})
       
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
      initializeNewRecreateSpec();
      var vol_list = $q.all([          
          cinderAPI.getVolumeSnapshots({ status: 'available' }).then(onGetVolumeSnapshots)
                          
        ]);               
        
        
   

      if (model.initializing) {
        promise = initPromise;

      } else if (model.initialized && !deep) {
        deferred = $q.defer();
        promise = deferred.promise;
        deferred.resolve();

      } else {
        model.initializing = true;
        Spinner.showModalSpinner(gettext("Collecting  Vms...."));
        promise = $q.all([
          novaAPI.getServersListBySearch({"searchterms":["active"],"searchindex":"status"}).then(onGetRecreateServers, noop)
        ]);        
        

        promise.then(onInitSuccess, onInitFail);
      }

      return promise;
    
    }
    function onGetVolumeSnapshots(data) {
      model.volumeSnapshots.length = 0;
      push.apply(model.volumeSnapshots, data.data.items);
      push.apply(model.volumesnapshot_list.volume_list,data.data.items);
      console.log(model.volumeSnapshots);
      console.log(model.volumesnapshot_list.volume_list);
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

    function onGetRecreateServers(res) {
      model.allErrorInstances.length = 0
      push.apply(model.allErrorInstances, res.data.vms);
    }

    return model;
  }

})();
