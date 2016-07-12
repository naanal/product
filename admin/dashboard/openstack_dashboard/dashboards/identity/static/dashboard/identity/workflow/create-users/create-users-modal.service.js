/**
 * Created by Raja on 6/29/2016.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.create-users')
    .factory(
      'horizon.dashboard.identity.workflow.create-users.modal.service', CreateUsersModalService
    );

  CreateUsersModalService.$inject = [
    '$modal',
    '$window',
    'horizon.dashboard.identity.workflow.create-users.modal-spec'
  ];

  function CreateUsersModalService($modal, $window, modalSpec) {
    var service = {
      open: open
    };

    return service;

    function open(launchContext) {
      console.log("create-users---create-users,modal.controller.js---->5")
      var localSpec = {
        resolve: {
          launchContext: function () {
            return launchContext;

          }
        }
      };

      angular.extend(localSpec, modalSpec);

      var createUsersModal = $modal.open(localSpec);
      console.log("create-users------2")
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
