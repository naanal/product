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
    .module('horizon.dashboard.virtual.workflow.recreate-instances')
    .factory('horizon.dashboard.virtual.workflow.recreate-instances.workflow', recreateInstancesWorkflow);

  recreateInstancesWorkflow.$inject = [
    'horizon.dashboard.virtual.workflow.recreate-instances.basePath',
    'horizon.app.core.workflow.factory'
  ];

  function recreateInstancesWorkflow(basePath, dashboardWorkflow) {    
    return dashboardWorkflow({
      title: gettext('Recreate Instances'),

      steps: [
        {
          id: 'select_error_instances',
          title: gettext('Select Instances'),
          templateUrl: basePath + 'select_error_instances/select_error_instances.html',
          helpUrl: basePath + 'select_error_instances/select_error_instances.help.html',
          formName: 'selectErrorInstancesForm'
        },
        {
          id: 'Download_json',
          title: gettext('Delete Instances'),
          templateUrl: basePath + 'download_json/download_json.html',
          helpUrl: basePath + 'download_json/download_json.help.html',
          formName: 'DeleteForm'
        },
        {
          id: 'start_recreate',
          title: gettext('Start Recreate'),
          templateUrl: basePath + 'start_recovery/start_recovery.html',
          helpUrl: basePath + 'start_recovery/start_recovery.help.html',
          formName: 'startRecreateForm'
        }
      ]
    });
  }

})();
