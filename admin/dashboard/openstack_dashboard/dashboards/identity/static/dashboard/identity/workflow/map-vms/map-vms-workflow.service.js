/**
 * Created by Raja on 6/29/2016.
 */
/*
 *    (c) Copyright 2015 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the 'License');
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.map-vms')
    .factory('horizon.dashboard.identity.workflow.map-vms.workflow', mapVmsWorkflow);

  mapVmsWorkflow.$inject = [
    'horizon.dashboard.identity.workflow.map-vms.basePath',
    'horizon.app.core.workflow.factory'
  ];

  function mapVmsWorkflow(basePath, dashboardWorkflow) {
    return dashboardWorkflow({
      title: gettext('Map Virtual Machines'),

      steps: [
        {
          id: 'users',
          title: gettext('Users'),
          templateUrl: basePath + 'users/users.html',
          helpUrl: basePath + 'users/users.help.html',
          formName: 'mapVmsUsersForm'
        },
        {
          id: 'computers',
          title: gettext('Computers'),
          templateUrl: basePath + 'computers/computers.html',
          helpUrl: basePath + 'computers/computers.help.html',
          formName: 'mapVmsComputersForm'
        },
        {
          id: 'verify',
          title: gettext('Verify'),
          templateUrl: basePath + 'verify/verify.html',
          helpUrl: basePath + 'verify/verify.help.html',
          formName: 'mapVmsVerifyForm'
        }
      ],
      btnText: {
        finish: gettext('Map Vms')
      },

      btnIcon: {
        finish: 'fa  fa-exchange'
      }
    });
  }

})();
