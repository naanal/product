/*
 *    (c) Copyright 2016 Naanal Technologies.
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
    .module('horizon.dashboard.overview.workflow.rally-test')
    .factory('horizon.dashboard.overview.workflow.rally-test.workflow', RallyTestWorkflow);

  RallyTestWorkflow.$inject = [
    'horizon.dashboard.overview.workflow.rally-test.basePath',
    'horizon.app.core.workflow.factory'
  ];

  function RallyTestWorkflow(basePath, dashboardWorkflow) {
    return dashboardWorkflow({
      title: gettext('Test Virtual Components'),

      steps: [
        {
          id: 'scenario',
          title: gettext('Choose Scenarios'),
          templateUrl: basePath + 'scenario/choosescenario.html',
          formName: 'RallyTestScenarioForm'
        },
        {
          id: 'inputs',
          title: gettext('Choose Inputs'),
          templateUrl: basePath + 'input/chooseinput.html',
          formName: 'RallyTestInputForm'
        },
        {
          id: 'maketest',
          title: gettext('Run Test'),
          templateUrl: basePath + 'maketest/maketest.html',
          formName: 'RallyTestMaketestForm'
        }
      ],

      btnText: {
        finish: gettext('Run Test')
      },

      btnIcon: {
        finish: 'fa fa-cloud-upload'
      }
    });
  }

})();

