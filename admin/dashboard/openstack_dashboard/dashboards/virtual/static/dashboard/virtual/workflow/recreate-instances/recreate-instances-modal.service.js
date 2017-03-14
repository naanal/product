/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.virtual.workflow.recreate-instances')
    .factory(
      'horizon.dashboard.virtual.workflow.recreate-instances.modal.service', RecreateInstancesModalService
    );

  RecreateInstancesModalService.$inject = [
    '$modal',
    '$window',
    'horizon.dashboard.virtual.workflow.recreate-instances.modal-spec'
  ];

  function RecreateInstancesModalService($modal, $window, modalSpec) {
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

      var createUsersModal = $modal.open(localSpec);      
      var handleModalClose = function (redirectPropertyName) {
        return function () {
          if (launchContext && launchContext[redirectPropertyName]) {
            $window.location.href = launchContext[redirectPropertyName];
          }
        };
      };

      return createUsersModal.result.then(
        handleModalClose('successUrl'),
        handleModalClose('dismissUrl')
      );
    }
  }

})();
