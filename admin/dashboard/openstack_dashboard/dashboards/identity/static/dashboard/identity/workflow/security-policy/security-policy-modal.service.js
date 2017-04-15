/**
 * Securityd by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.security-policy')
    .factory(
      'horizon.dashboard.identity.workflow.security-policy.modal.service', SecurityPolicyModalService
    );

  SecurityPolicyModalService.$inject = [
    '$modal',
    '$window',
    'horizon.dashboard.identity.workflow.security-policy.modal-spec'
  ];

  function SecurityPolicyModalService($modal, $window, modalSpec) {
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

      var securityPolicyModal = $modal.open(localSpec);      
      var handleModalClose = function (redirectPropertyName) {
        return function () {
          if (launchContext && launchContext[redirectPropertyName]) {
            $window.location.href = launchContext[redirectPropertyName];
          }
        };
      };

      return securityPolicyModal.result.then(
        handleModalClose('successUrl'),
        handleModalClose('dismissUrl')
      );
    }
  }

})();
