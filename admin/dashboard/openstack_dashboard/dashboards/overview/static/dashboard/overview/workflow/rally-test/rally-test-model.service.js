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
    'horizon.app.core.openstack-service-api.glance',
    'horizon.framework.widgets.modal-wait-spinner.service',
    'horizon.framework.widgets.toast.service'
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
  function RallyTestModel($q, $log, rallyAPI, novaAPI, neutronAPI, glanceAPI, modalWaitSpinnerService, toast) {

    var initPromise;
    var model = {

      initializing: false,
      initialized: false,

      initializeScenario : {},

      orginalSchema : {},
      flavors: [],
      images: [],
      fixed_network:[],
            /**
       * api methods for UI controllers
       */

      initialize: initialize,
      runRally : runRally,
      log : [],
      jn : [],
      id : '',
      resultschema: {},
      finalresults : [],
    //  viewhtml: viewhtml,
    //  htm: [],
      isProcessing : false
    };


  function initializeSelectedScenarios(){
      model.initializeScenario = {
        selections : [],
        processedScenarios : {},
        flavor: null,
        log : [],
        jn : [],
        id : '',
        resultschema: {},
        finalresults : []
      }
    }


    /**function viewhtml() {
        return rallyAPI.rallyViewHtml().then(function(response){
          model.htm = response.data.html_result;
        });
    }**/

    function runRally() {

      var finalselections = angular.copy(model.initializeScenario.selections); 
      cleanNullProperties(finalselections);
 //     model.isProcessing=true;
      for (var i=0; i<finalselections.length; i++){
        angular.extend(model.initializeScenario.processedScenarios, finalselections[i].task)
      }

      var processedselections = angular.copy(model.initializeScenario.processedScenarios);
      modalWaitSpinnerService.showModalSpinner(gettext("Please Wait...     Test is Running"));
      return rallyAPI.rallyStartTest(processedselections)
      .then(function(response){
        model.log = response.data.log_result;
        model.jn = response.data.jsn_result;
        model.id = response.data.id;
        processResult(model.jn);
        modalWaitSpinnerService.hideModalSpinner();
        model.initializeScenario.selections=[];
        model.initializeScenario.processedScenarios={};
      },
      function(data) {
        // Handle error here
        model.initializeScenario.selections=[];
        model.initializeScenario.processedScenarios={};
        modalWaitSpinnerService.hideModalSpinner();
        toast.add('error', interpolate("Failed to select Tasks or Inputs", "1"));
      });
//      model.isProcessing=false;
    }

    function cleanNullProperties(finalselections) {
      // Initially clean fields that don't have any value.
      for (var key in finalselections) {
        if (finalselections.hasOwnProperty(key) && finalselections[key] === null) {
          delete finalselections[key];
        }
      }
    }

    function initresultschema(){
      model.resultschema = {
         "sno" : '',
         "name" : '',
         "count" : '',
         "duration" : '',
         "status" : '',
         "percentage" : ''
       }
    }
    function processResult(results){
   
         initresultschema();

         var results = JSON.parse(results);

         for (var i=0;i<results.length;i++) {
               model.resultschema.sno = i+1;
               model.resultschema.name= results[i].key.name;
               model.resultschema.count = results[i].result.length;
               var duration = 0; 
               var err = 0;
               var suc = 0;
           
               for(var j=0; j< results[i].result.length; j++)
                 {
                   duration  = duration + results[i].result[j].duration;
                   if(results[i].result[j].error.length > 0)
                     err  = err + 1;
                 }
              model.resultschema.duration = duration;
              if(err > 0)
              {
                model.resultschema.status = 'Failed';
                model.resultschema.percentage = ( err / results[i].result.length ) * 100;
               }
              else
              {
                model.resultschema.status = 'Success';
                model.resultschema.percentage = 100;
              }
              
           model.finalresults.push(model.resultschema);
           initresultschema();     
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
        model.finalresults.length = 0;

        promise = $q.all([
          getImages(),
          getFlavors(),
          getSamples(),
          getNetworks()

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
    function getNetworks() {
      return  neutronAPI.getNetworks().then(onGetNet_list, noop);
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
    function onGetNet_list(data) {
   
      push.apply(model.fixed_network, data.data.items);
    }
    return model;
  }

})();

