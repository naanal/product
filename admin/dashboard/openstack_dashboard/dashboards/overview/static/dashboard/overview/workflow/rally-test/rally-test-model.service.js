(function () {
  'use strict';

  var push = Array.prototype.push;
  var noop = angular.noop;

  /**
   * @ngdoc overview
   * @name horizon.dashboard.overview.workflow.rally-test
   *
   * @description
   * Manage workflow of Benchmarking and Test.
   */

  angular
    .module('horizon.dashboard.overview.workflow.rally-test')
    .factory('RallyTestModel', RallyTestModel);

  RallyTestModel.$inject = [
    '$q',
    '$log',
    'horizon.app.core.openstack-service-api.rally',
    'horizon.app.core.openstack-service-api.nova',
    'horizon.app.core.openstack-service-api.neutron',
    'horizon.app.core.openstack-service-api.glance'
  ];

  /**
   * @ngdoc service
   * @name RallyTestModel
   *
   * @param {Object} $q
   * @param {Object} $log
   * @param {Object} cinderAPI
   * @param {Object} glanceAPI
   * @param {Object} neutronAPI
   * @param {Object} novaAPI
   * @param {Object} novaExtensions
   * @param {Object} securityGroup
   * @param {Object} serviceCatalog
   * @param {Object} settings
   * @param {Object} toast
   * @description
   * This is the M part in MVC design pattern for launch instance
   * wizard workflow. It is responsible for providing data to the
   * view of each step in launch instance workflow and collecting
   * user's input from view for  creation of new instance.  It is
   * also the center point of communication between launch instance
   * UI and services API.
   * @returns {Object} The model
   */
  function RallyTestModel($q, $log, rallyAPI, novaAPI, neutronAPI, glanceAPI) {

    var initPromise;
    var model = {

      initializing: false,
      initialized: false,

      initializeScenario : {},

      orginalSchema : {},
      flavors: [],
      images: [],
            /**
       * api methods for UI controllers
       */

      initialize: initialize,
      runRally : runRally,
      log : []
    };

    function runRally() {

      var finalselections = angular.copy(model.initializeScenario.selections); 

      for (var i=0; i<finalselections.length; i++){
        angular.extend(model.initializeScenario.processedScenarios, finalselections[i].task)
      }

      var processedselections = angular.copy(model.initializeScenario.processedScenarios);
      return rallyAPI.rallyStartTest(processedselections).then(function(response){
        model.log = response.data;
      });

    }

    function initializeSelectedScenarios(){
      model.initializeScenario = {
        selections : [],
        processedScenarios : {}
      }
    }

    function initialize(deep) {
      var deferred, promise;

      initializeSelectedScenarios();

      if (model.initializing) {
        promise = initPromise;

      } else if (model.initialized && !deep) {
        deferred = $q.defer();
        promise = deferred.promise;
        deferred.resolve();

      } else {
        model.initializing = true;

        promise = $q.all([
          getImages(),
          getFlavors(),
          getSamples()

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

    function getSamples() {
      return rallyAPI.rallyTasksScenarios().then(onGetSamples);
    }

    function getImages() {
      return glanceAPI.getImages({status:'active'}).then(onGetImages);
    }

     function getFlavors() {
      return  novaAPI.getFlavors(true, true).then(onGetFlavors);
    }

    function onGetSamples(data) {
      angular.extend(model.orginalSchema, data.data);
    }

    function onGetImages(data) {
   
      push.apply(model.images, data.data.items);
    }

     function onGetFlavors(data) {
   
      push.apply(model.flavors, data.data.items);
    }

    return model;
  }

})();


    