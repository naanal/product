(function () {

   angular.module('horizon.dashboard.overview.virtual_monitor')

    .factory('VMInfluxService', VMInfluxService);
        
    VMInfluxService.$inject = [
      'horizon.framework.widgets.toast.service',
      'horizon.framework.util.i18n.gettext',
      'horizon.framework.widgets.modal-wait-spinner.service',
      '$http'
    ];

    function VMInfluxService(toast, gettext, Spinner, $http) {
    
         function errFunction(response) {
            console.log(response.status,response.statusText,response.headers);
        }

        var obj = {};
        obj.getVMState = function(){
            return $http({
                method: "GET",
                url: '/static/vm_monitoring.json',
                headers : {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).then(function(response) { 
                return response.data;
            }, function errorCallback(response) {
                errFunction(response);
            });
        },
        obj.getVMData = function(query, vm_metric){
            db = 'telegraf';
            delete $http.defaults.headers.common["X-Requested-With"]
             var qurl = 'http://192.168.30.200:8086/query?q=' + query + '&db=' + db + '&u=' + 'root' + '&p=' + 'root';
            return $http({
                method: "GET",
                url: qurl
            }).then(function(response) { 
                if (response.data.results[0].hasOwnProperty('series')) {
                    response = response.data.results[0].series[0];
                    var out_metrics = { metrics:response.values.map(v => Object.assign(...response.columns.map((c,i) => ({[c] : v[i]})))) };
                    if ( out_metrics.metrics[0].CPU_Proc > 75 || out_metrics.metrics[0].CPU_User > 75 || 
                        out_metrics.metrics[0].RAM_Available < 2147483648 ||
                        out_metrics.metrics[0].Disk_Perc > 75 || out_metrics.metrics[0].Disk_Sec > 0.015 ||
                        out_metrics.metrics[0].NW_Received > 4194304 || out_metrics.metrics[0].NW_Sent > 4194304
                        ) {
                            vm_metric.health = 2;
                    }

                    if ( out_metrics.metrics[0].CPU_Proc > 85 || out_metrics.metrics[0].CPU_User > 85 || 
                        out_metrics.metrics[0].RAM_Available < 1147483648 ||
                        out_metrics.metrics[0].Disk_Perc > 85 || out_metrics.metrics[0].Disk_Sec > 0.029 ||
                        out_metrics.metrics[0].NW_Received > 10194304 || out_metrics.metrics[0].NW_Sent > 10194304
                        ) {
                            vm_metric.health = 3;
                    }

                    angular.extend(vm_metric,out_metrics.metrics[0]) ;

                }
                return ""
            }, function errorCallback(response) {
                errFunction(response);
            });
        }
    
        return obj;
    };

})();