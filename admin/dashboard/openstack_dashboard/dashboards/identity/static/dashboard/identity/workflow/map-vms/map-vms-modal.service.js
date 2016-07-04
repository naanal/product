/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.map-vms')
    .factory(
      'horizon.dashboard.identity.workflow.map-vms.modal.service', MapVmsModalService
    );

  MapVmsModalService.$inject = [
    '$modal',
    '$window',
    'horizon.dashboard.identity.workflow.map-vms.modal-spec'
  ];

  function MapVmsModalService($modal, $window, modalSpec) {
    var service = {
      open: open
    };

    return service;

    function open(launchContext) {
      var localSpec = {
        resolve: {
          launchContext: function () {
            return launchContext;
          }
        }
      };

      angular.extend(localSpec, modalSpec);

      var mapVmsModal = $modal.open(localSpec);
      var handleModalClose = function (redirectPropertyName) {
        return function () {
          if (launchContext && launchContext[redirectPropertyName]) {
            $window.location.href = launchContext[redirectPropertyName];
          }
        };
      };

      return mapVmsModal.result.then(
        handleModalClose('successUrl'),
        handleModalClose('dismissUrl')
      );
    }
  }

})();
