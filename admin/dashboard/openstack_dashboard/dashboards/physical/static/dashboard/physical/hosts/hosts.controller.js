/**
 * Copyright 2015 IBM Corp.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function() {
  'use strict';

  /**
   * @ngdoc identityUsersTableController
   * @ngController
   *
   * @description
   * Controller for the identity users table.
   * Serve as the focal point for table actions.
   */
  angular
    .module('horizon.dashboard.physical.hosts')
    .controller('forceMigrateController', forceMigrateController);

  forceMigrateController.$inject = [
    'horizon.framework.widgets.toast.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.app.core.openstack-service-api.ha',
    'horizon.framework.widgets.modal-wait-spinner.service',
    '$scope',
    '$rootScope'
  ];

  function forceMigrateController(toast, gettext, haAPI,Spinner, $scope, $rootScope) {

      $scope.downinstance = [];
        $scope.get_nodeDetails=function(){          
          console.log("inside the get get get_nodeDetails method")
          haAPI.createStartMigrate()
          .then(function(res){                    
            $scope.allNodes=res.data;
            console.log(res.data)
            if (res.data=="successfully started migration...!")
              toast.add('success', res.data);
            else
              toast.add('danger', res.data);                        
          })
        }
        
   
  }

})();
