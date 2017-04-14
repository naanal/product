
//  *    (c) Copyright 2015 Hewlett-Packard Development Company, L.P.
//  *
//  * Licensed under the Apache License, Version 2.0 (the "License");
//  * you may not use this file except in compliance with the License.
//  * You may obtain a copy of the License at
//  *
//  *    http://www.apache.org/licenses/LICENSE-2.0
//  *
//  * Unless required by applicable law or agreed to in writing, software
//  * distributed under the License is distributed on an "AS IS" BASIS,
//  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  * See the License for the specific language governing permissions and
//  * limitations under the License.
 
// (function() {
//     'use strict';

//     angular
//         .module('horizon.dashboard.identity.workflow.security-users')
//         .controller('addUsersController', addUsersController);

//     addUsersController.$inject = [
//         'securityUsersModel',
        
//         '$scope'
//     ];

//     function addUsersController(securityUsersModel,  $scope) {
//         var ctrl = this;
        

//         function getUsers(user) {
            
//     }
// })();



/*
 *    (c) Copyright 2015 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function () {
  'use strict';

  angular
    .module('horizon.dashboard.identity.workflow.security-policy')
    .controller('addPolicyController', addPolicyController);

  addPolicyController.$inject = [
    'securityPolicyModel',
    'horizon.app.core.openstack-service-api.ldap',
    'horizon.framework.widgets.modal-wait-spinner.service',
    '$scope',
    '$rootScope'
  ];

  function addPolicyController(securityPolicyModel,ldapAPI, Spinner,$scope, $rootScope) {
    var ctrl = this;
    ctrl.applyPolicy=applyPolicy;
    ctrl.selectedGroup = $scope.launchContext;
    $scope.model.group=ctrl.selectedGroup;
    $scope.model.policys=[];
    // console.log(ctrl.selectedGroup);
    console.log($scope.model.group);
    console.log("inside securityPolicyModel");

    $rootScope.retriveSecurityPolicy = function(){           
        ldapAPI.getsecurityPolicy()
          .then(function(res){
              Spinner.hideModalSpinner();
              $scope.securitypolicy = res.data['users_groups']; 
              $scope.securitypolicycount = $scope.securitypolicy.length;             
              console.log("securitypolicy");
              // console.log($scope.securitypolicy);
              // console.log($scope.securitypolicycount);
              // console.log($scope.model.group.group.cn);
              $scope.model.policys=[];
              for (var i = 0; i < $scope.securitypolicycount; i++) 
                    {
                        // console.log($scope.securitypolicy[i].cn);
                        // console.log($scope.securitypolicy[i].dn);
                        // console.log($scope.securitypolicy[i].cn);
                        // console.log($scope.model.group.group.dn);
                        // console.log($scope.securitypolicy[i].usernames.indexOf($scope.model.group.group.cn));
                        if($scope.securitypolicy[i].usernames.indexOf($scope.model.group.group.cn) > -1)
                        {
                          // console.log("INside if condition");
                          var add_to_group=false;
                          // console.log("set add to group === false");
                        }
                        else
                        {
                          var add_to_group=true;
                          // console.log("set add_to_group == true");
                        }
                        var policy={"name":$scope.securitypolicy[i].cn,"policy_dn":$scope.securitypolicy[i].dn,"user_dn":$scope.model.group.group.dn,"add_to_group":add_to_group}
                        console.log(policy);
                        $scope.model.policys.push(policy);                        
                        // $scope.model.usernames.push($scope.ldapusers[i].username);
                    }
                    console.log("final input");
                    console.log($scope.model.policys);
          },function(error){              
          });
      }
    $rootScope.retriveSecurityPolicy();

    function applyPolicy(policy){
      console.log("Inside the applyPolicy");
      console.log(policy.policy.add_to_group);


      if(policy.policy.add_to_group)
      {
        console.log("change true to false");
        policy.policy.add_to_group=false;
      }
      else
      {
        console.log("change false to true");
        policy.policy.add_to_group=true
      }
        console.log("After chagne");
        console.log(policy.policy);

       ldapAPI.applysecurityPolicy(policy.policy)
          .then(function(res){
            $rootScope.retriveSecurityPolicy();         
            var res = res.data;
            for(var i=0;i<res.length;i++) {
              if (res[i].status.includes("success"))   
                
                toast.add('success', res[i].group_name+" "+res[i].action+" "+res[i].status);
              else                
                toast.add('danger',res[i].group_name+" "+res[i].action+" "+res[i].status);
            }           
          })  
          $rootScope.retriveSecurityPolicy();



      
      
    }
  }
})();
