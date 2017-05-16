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

  describe('Identity virtual_machines status table controller', function() {

    var policy = { allowed: true };
    function fakePolicy() {
      return {
        then: function(successFn, errorFn) {
          if (policy.allowed) {
            successFn();
          } else {
            errorFn();
          }
        }
      };
    }
    function fakePromise() {
      return { success: angular.noop };
    }
    function fakeToast() {
      return { add: angular.noop };
    }

    var controller, toastService, policyAPI, keystoneAPI;

    ///////////////////////

    beforeEach(module('horizon.framework.util.http'));
    beforeEach(module('horizon.framework.util.i18n'));
    beforeEach(module('horizon.framework.conf'));
    beforeEach(module('horizon.framework.widgets.toast'));
    beforeEach(module('horizon.app.core.openstack-service-api'));

    beforeEach(module('horizon.dashboard.virtual'));
    beforeEach(module('horizon.dashboard.virtual.virtual_machines'));
    beforeEach(inject(function($injector) {

      toastService = $injector.get('horizon.framework.widgets.toast.service');
      policyAPI = $injector.get('horizon.app.core.openstack-service-api.policy');
      keystoneAPI = $injector.get('horizon.app.core.openstack-service-api.keystone');
      controller = $injector.get('$controller');

      spyOn(toastService, 'add').and.callFake(fakeToast);
      spyOn(policyAPI, 'ifAllowed').and.callFake(fakePolicy);
      spyOn(keystoneAPI, 'geteventlog').and.callFake(fakePromise);
      spyOn(keystoneAPI, 'getCurrenteventlogession').and.callFake(fakePromise);
    }));

    function createController() {
      return controller('virtualevirtualmachineTableController', {
        toast: toastService,
        policyAPI: policyAPI,
        keystoneAPI: keystoneAPI
      });
    }

    it('should invoke keystone apis if policy passes', function() {
      policy.allowed = true;
      createController();
      expect(policyAPI.ifAllowed).toHaveBeenCalled();
      expect(keystoneAPI.geteventlog).toHaveBeenCalled();
      expect(keystoneAPI.getCurrenteventlogession).toHaveBeenCalled();
    });

    it('should not invoke keystone apis if policy fails', function() {
      policy.allowed = false;
      createController();
      expect(policyAPI.ifAllowed).toHaveBeenCalled();
      expect(toastService.add).toHaveBeenCalled();
      expect(keystoneAPI.geteventlog).not.toHaveBeenCalled();
      expect(keystoneAPI.getCurrenteventlogession).not.toHaveBeenCalled();
    });

  });

})();
