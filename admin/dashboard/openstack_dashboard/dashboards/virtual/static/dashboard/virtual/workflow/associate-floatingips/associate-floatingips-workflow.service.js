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
    .module('horizon.dashboard.virtual.workflow.associate-floatingips')
    .factory('horizon.dashboard.virtual.workflow.associate-floatingips.workflow', associateFloatingipsWorkflow);

  associateFloatingipsWorkflow.$inject = [
    'horizon.dashboard.virtual.workflow.associate-floatingips.basePath',
    'horizon.app.core.workflow.factory'
  ];

  function associateFloatingipsWorkflow(basePath, dashboardWorkflow) {    
    return dashboardWorkflow({
      title: gettext('Associate Floating Ips'),

      steps: [
        {
          id: 'select_instances',
          title: gettext('Select Instances'),
          templateUrl: basePath + 'select_instances/select_instances.html',
          helpUrl: basePath + 'select_instances/select_instances.help.html',
          formName: 'selectInstancesForm'
        },
        {
          id: 'select_method',
          title: gettext('Choose Method'),
          templateUrl: basePath + 'select_method/select_method.html',
          helpUrl: basePath + 'select_method/select_method.help.html',
          formName: 'selectMethodForm'
        }
      ],

      btnText: {
        finish: gettext('Associate Ips')
      },

      btnIcon: {
        finish: 'fa fa-map-signs'
      }
    });
  }

})();
