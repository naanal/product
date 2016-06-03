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
        rallyTask = subprocess.Popen("rally task start '%s'"%(rtask), stdout=subprocess.PIPE, shell=True)
        (output, err) = rallyTask.communicate()
        return output
