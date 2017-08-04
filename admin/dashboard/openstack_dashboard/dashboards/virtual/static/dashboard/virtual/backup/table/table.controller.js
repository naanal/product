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
     * @ngdoc backupController
     * @ngController
     *
     * @description
     * Controller for the virtual vms table.
     * Serve as the focal point for table actions.
     */
    angular
        .module('horizon.dashboard.virtual.backup')
        .controller('backupController', backupController);

    backupController.$inject = [
        'horizon.framework.widgets.toast.service',
        'horizon.framework.util.i18n.gettext',
        'horizon.app.core.openstack-service-api.nova',
        'horizon.app.core.openstack-service-api.backup',
        'horizon.framework.widgets.modal-wait-spinner.service',
        '$scope',
        '$rootScope'
    ];
    var app = angular.module('weekday', ['ng-weekday-selector']);

    function backupController(toast, gettext, novaAPI, backupAPI, Spinner, $scope, $rootScope) {

        $scope.drives = ["E:"];
        $scope.hours = [];
        $scope.mins = [];

        function pad2(number) {
            return (number < 10 ? '0' : '') + number
        }


        var initHours = function() {
            var i;
            for (i = 0; i <= 23; i++) {
                var num = pad2(i);
                $scope.hours.push(num);
            }
        }


        var initMins = function() {
            var i;
            for (i = 0; i <= 59; i++) {
                var num = pad2(i);
                $scope.mins.push(num);
            }
        }
        initHours();
        initMins();



        //$scope.mins = ["E:"];
        $scope.name = 'World';
        $scope.selectedDrive = $scope.drives[0];

        $scope.backups = ["Latest", "Previous"];

        $scope.selectedBackup = $scope.backups[0];

        $scope.tableBackup = {
            order: 'name',
            selected: []
        };

        $scope.tableRestore = {
            order: 'name',
            selected: []
        };


        $scope.example = {
            value: new Date(1970, 0, 1, 14, 57, 0)
        }



        $rootScope.reloadPage = function() {
            window.location.reload();
        }




        $rootScope.retieveCilentDetails = function() {
            Spinner.showModalSpinner(gettext("Retrieving Client machine details....."));
            backupAPI.getClientdetails()
                .then(function(res) {
                    Spinner.hideModalSpinner();
                    $scope.cilentdetails = res.data;
                    console.log("cilent details");
                    console.log($scope.cilentdetails);
                }, function(error) {
                    Spinner.hideModalSpinner();
                });
        }
        $rootScope.retieveCilentDetails();




        $scope.backupALL = function(ciletMachineName) {
            var backup_attributes = {};

            // console.log("Inside Backup All");
            // console.log(backup_attributes);
            // console.log(ciletMachineName);
            // console.log($scope.selectedDrive);
            backup_attributes.clients = ciletMachineName;
            backup_attributes.drive = $scope.selectedDrive;
            console.log(backup_attributes);
            backupAPI.backupClient(backup_attributes)
                .then(function(res) {
                    var res = res.data;
                    console.log(res);
                    $rootScope.reloadPage();
                    $rootScope.retieveCilentDetails();

                })
        }




        $scope.backupSingle = function(ciletMachineName) {
            var backup_attributes = {};


            // console.log(backup_attributes);
            // console.log(ciletMachineName);
            // console.log($scope.selectedDrive);
            backup_attributes.clients = [ciletMachineName];
            backup_attributes.drive = $scope.selectedDrive;
            console.log(backup_attributes);



            backupAPI.backupClient(backup_attributes)
                .then(function(res) {
                    var res = res.data;
                    console.log(res);
                    $rootScope.retieveCilentDetails();

                })
        }




        $scope.restoreALL = function(ciletMachineName) {
            var restore_attributes = {};


            // console.log(restore_attributes);
            // console.log(ciletMachineName);
            // console.log($scope.selectedDrive);
            restore_attributes.clients = ciletMachineName;
            restore_attributes.drive = $scope.selectedDrive;
            restore_attributes.backup_name = $scope.selectedBackup;
            console.log(restore_attributes);



            backupAPI.restoreClient(restore_attributes)
                .then(function(res) {
                    var res = res.data;
                    console.log(res);
                    $rootScope.reloadPage();
                    $rootScope.retieveCilentDetails();


                })
        }


        $scope.schduleALL = function(days, selectedHours, selectedMins) {
            var schduleAttributes = {};
            var dayString = "";
            for (var i = 0; i < days.length; i++) {
                if (days[i].isSelected == true) {
                    dayString += days[i].name + ","

                }
            }

            dayString = dayString.slice(0, -1);
            schduleAttributes.days = dayString;
            schduleAttributes.times = selectedHours.toString() + ':' + selectedMins.toString();
            console.log(schduleAttributes);
            backupAPI.schduleALL(schduleAttributes)
                .then(function(res) {
                    var res = res.data;
                    console.log(res);
                    $rootScope.reloadPage();
                    $rootScope.retieveCilentDetails();


                })


            schduleAttributes.drive = $scope.selectedDrive;




        }




    }

})();