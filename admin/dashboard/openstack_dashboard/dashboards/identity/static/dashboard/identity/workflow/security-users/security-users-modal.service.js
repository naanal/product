/**
 * Securityd by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.security-users')
    .factory(
      'horizon.dashboard.identity.workflow.security-users.modal.service', SecurityUsersModalService
    );

  SecurityUsersModalService.$inject = [
    '$modal',
    '$window',
    'horizon.dashboard.identity.workflow.security-users.modal-spec'
  ];

  function SecurityUsersModalService($modal, $window, modalSpec) {
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

      var securityUsersModal = $modal.open(localSpec);      
      var handleModalClose = function (redirectPropertyName) {
        return function () {
          if (launchContext && launchContext[redirectPropertyName]) {
            $window.location.href = launchContext[redirectPropertyName];
          }
        };
      };

      return securityUsersModal.result.then(
        handleModalClose('successUrl'),
        handleModalClose('dismissUrl')
      );
    }
  }

})();
