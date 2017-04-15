
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
    .module('horizon.dashboard.identity.workflow.security-users')
    .controller('addUsersController', addUsersController);

  addUsersController.$inject = [
    'securityUsersModel',
    'horizon.app.core.openstack-service-api.ldap',
    'horizon.framework.widgets.modal-wait-spinner.service',
    '$scope'
  ];

  function addUsersController(securityUsersModel,ldapAPI, Spinner,$scope) {
    var ctrl = this;
    ctrl.getUsers=getUsers;
    ctrl.selectedGroup = $scope.launchContext;
    $scope.model.group=ctrl.selectedGroup;
    // console.log(ctrl.selectedGroup);
    console.log($scope.model.group);
   

    function getUsers(){
        console.log(ctrl.selectedGroup);
            Spinner.showModalSpinner(gettext("Retrieving Users...."));
        ldapAPI.getUsers()
          .then(function(res){
              Spinner.hideModalSpinner();
              $scope.ldapusers = res.data;              
              $scope.ldapuserscount = $scope.ldapusers.length;        
              console.log($scope.ldapusers);
              console.log($scope.ldapuserscount);
              if ($scope.model.newUserSpec.add_to_group=="true")
              {
                console.log("Inside the add user..!");
                $scope.model.usernames=[]
                for (var i = 0; i < $scope.ldapuserscount; i++) 
                    {
                        console.log($scope.ldapusers[i].username);
                        $scope.model.usernames.push($scope.ldapusers[i].username);
                    }
                for(var j=0; j<$scope.model.group.group.usernames.length; j++)
                {
                     var index = $scope.model.usernames.indexOf($scope.model.group.group.usernames[j]);
                     $scope.model.usernames.splice(index, 1);
                }
                console.log($scope.model.usernames);
              }
              else
              {
                $scope.model.usernames=[]
                console.log("inside the delete user");
                $scope.model.usernames=$scope.model.group.group.usernames;
                console.log($scope.model.usernames);

              }
              console.log("output");
              console.log($scope.model.usernames);
          },function(error){
              Spinner.hideModalSpinner();
          });

      
      
    }
  }
})();
