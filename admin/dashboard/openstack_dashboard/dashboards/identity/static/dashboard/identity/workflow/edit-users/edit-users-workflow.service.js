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
    .module('horizon.dashboard.identity.workflow.edit-users')
    .factory('horizon.dashboard.identity.workflow.edit-users.workflow', editUsersWorkflow);

  editUsersWorkflow.$inject = [
    'horizon.dashboard.identity.workflow.edit-users.basePath',
    'horizon.app.core.workflow.factory'
  ];

  function editUsersWorkflow(basePath, dashboardWorkflow) {
    return dashboardWorkflow({
      title: gettext('Edit Users'),

      steps: [
        {
          id: 'actionlists',
          title: gettext('Select Actions'),
          templateUrl: basePath + 'actionlists/actionlists.html',
          helpUrl: basePath + 'actionlists/actionlists.help.html',
          formName: 'actionlistsForm'
        },
        {
          id: 'edit',
          title: gettext('Edit'),
          templateUrl: basePath + 'edit/edit.html',
          helpUrl: basePath + 'edit/edit.help.html',
          formName: 'editForm'
        },
        {
          id: 'verify',
          title: gettext('Verify'),
          templateUrl: basePath + 'verify/verify.html',
          helpUrl: basePath + 'verify/verify.help.html',
          formName: 'verifyDetailsForm'
        }
      ]
        ,

      btnText: {
        finish: gettext('Edit Users')
      },

      btnIcon: {
        finish: 'fa fa-user-plus'
      }
    });
  }

})();
