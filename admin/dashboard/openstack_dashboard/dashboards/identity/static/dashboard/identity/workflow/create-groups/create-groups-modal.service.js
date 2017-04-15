/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.create-groups')
    .factory(
      'horizon.dashboard.identity.workflow.create-groups.modal.service', CreateGroupsModalService
    );

  CreateGroupsModalService.$inject = [
    '$modal',
    '$window',
    'horizon.dashboard.identity.workflow.create-groups.modal-spec'
  ];

  function CreateGroupsModalService($modal, $window, modalSpec) {
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

      var createGroupsModal = $modal.open(localSpec);      
      var handleModalClose = function (redirectPropertyName) {
        return function () {
          if (launchContext && launchContext[redirectPropertyName]) {
            $window.location.href = launchContext[redirectPropertyName];
          }
        };
      };

      return createGroupsModal.result.then(
        handleModalClose('successUrl'),
        handleModalClose('dismissUrl')
      );
    }
  }

})();
