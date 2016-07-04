/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.edit-users')
    .factory(
      'horizon.dashboard.identity.workflow.edit-users.modal.service', EditUsersModalService
    );

  EditUsersModalService.$inject = [
    '$modal',
    '$window',
    'horizon.dashboard.identity.workflow.edit-users.modal-spec'
  ];

  function EditUsersModalService($modal, $window, modalSpec) {
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

      var editUsersModal = $modal.open(localSpec);
      console.log(localSpec);
      var handleModalClose = function (redirectPropertyName) {
        return function () {
          if (launchContext && launchContext[redirectPropertyName]) {
            $window.location.href = launchContext[redirectPropertyName];
          }
        };
      };

      return editUsersModal.result.then(
        handleModalClose('successUrl'),
        handleModalClose('dismissUrl')
      );
    }
  }

})();
