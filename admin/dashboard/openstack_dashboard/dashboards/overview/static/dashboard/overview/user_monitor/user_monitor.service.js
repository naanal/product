(function () {

   angular.module('horizon.dashboard.overview.user_monitor')

    .factory('InfluxService', InfluxService);
        
    InfluxService.$inject = [
      'horizon.framework.widgets.toast.service',
      'horizon.framework.util.i18n.gettext',
      'horizon.framework.widgets.modal-wait-spinner.service',
      '$http'
    ];

    function InfluxService(toast, gettext, Spinner, $http) {
    
         function errFunction(response) {
            console.log(response.status,response.statusText,response.headers);
        }

        var obj = {};
        obj.getData = function(query){
            db = 'telegraf';
            delete $http.defaults.headers.common["X-Requested-With"]
             var qurl = 'http://192.168.30.200:8086/query?q=' + query + '&db=' + db + '&u=' + 'root' + '&p=' + 'root';
            return $http({
                method: "GET",
                url: qurl
            }).then(function(response) { 
                return response.data.results[0].series;
            }, function errorCallback(response) {
                errFunction(response);
            });
        },
        obj.getUserData = function(query, user_session_status){
            db = 'telegraf';
            delete $http.defaults.headers.common["X-Requested-With"]
             var qurl = 'http://192.168.30.200:8086/query?q=' + query + '&db=' + db + '&u=' + 'root' + '&p=' + 'root';
            return $http({
                method: "GET",
                url: qurl
            }).then(function(response) { 
                response = response.data.results[0].series;
                isHigh= 0; msg = [];
                if(response[0].values[0][1] > 150 || response[0].values[0][2] > 150) {
                  isHigh = 1;
                  msg.push("CPU Usage is High");
                }
                if(response[0].values[0][3] > 2000) {
                  isHigh = 1
                  msg.push("RAM Usage is High");
                }
                if(response[0].values[0][4] > 5000 | response[0].values[0][5] > 5000) {
                  isHigh = 1
                  msg.push("Disk Usage is High");
                }
                user_session_status.isHigh = isHigh;
                user_session_status.msg = msg;
                return user_session_status
            }, function errorCallback(response) {
                errFunction(response);
            });
        },
        obj.getSessionData = function(query){
            db = 'telegraf';
            delete $http.defaults.headers.common["X-Requested-With"]
             var qurl = 'http://192.168.30.200:8086/query?q=' + query + '&db=' + db + '&u=' + 'root' + '&p=' + 'root';
            return $http({
                method: "GET",
                url: qurl
            }).then(function(response) { 
                return response.data.results[0].series;
            }, function errorCallback(response) {
                errFunction(response);
            });
        },
        obj.getTopData = function(query){
            db = 'telegraf';
            delete $http.defaults.headers.common["X-Requested-With"]
             var qurl = 'http://192.168.30.200:8086/query?q=' + query + '&db=' + db + '&u=' + 'root' + '&p=' + 'root';
            return $http({
                method: "GET",
                url: qurl
            }).then(function(response) { 
                return response.data.results;
            }, function errorCallback(response) {
                errFunction(response);
            });
        }
    
        return obj;
    };

})();