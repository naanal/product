# Copyright 2016 Naanal Technologies Pvt Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""API over the rally service.
"""

from django.views import generic

from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils
import subprocess
import json


@urls.register
class TaskStart(generic.View):
    """API for rally volumes.
    """
    url_regex = r'rally/task/$'

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        rtask = json.dumps(request.DATA)
 #       command='rally task start {0}'.str(rtask)
 #       rallyTask= subprocess.check_call(["rally","task","start", rtask], shell=False,stdout=file_out)
        rallyTask= subprocess.check_output(["rally","task","start", rtask], shell=False)
        report=rallyTask.split(" ")
        chars=[]
        for line in report:
            chars.extend(line)
#            print (line)
            if "UUID" in line:
                i=line.split(' ')
                print(i)
                id = [x[:x.index('\n')] if '\n' in x else x for x in i]
                uuid=''.join(map(str, id))
                jsn= subprocess.check_output(["rally","task","results", uuid], shell=False)              
 #       result=[rallyTask,jsn]
#        print(result[0])
#        print("!!!!!!!!!!!!!!!!!!!!!!!!!1")
#        print(jsn)
        return {"log_result":rallyTask,"jsn_result":jsn, "id" :uuid}


@urls.register
class viewHtml(generic.View):
    """API for rally volumes.
    """
    url_regex = r'rally/html/$'

    @rest_utils.ajax()
    def get(self, request):
        htm_result=subprocess.check_output(["rally","task","report","--out=report.html","--open"], shell = False)
        print(htm_result)
        return {"html_result":htm_result}
