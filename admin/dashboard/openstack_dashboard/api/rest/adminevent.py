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
"""API over the admin log service.
"""
from django.views import generic
from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils
from django.conf import settings
import json


@urls.register
class Users(generic.View):
    """API for AD User Lists, Creation, Disable.
    """
    url_regex = r'log/$'
    @rest_utils.ajax()
    def get(self, request):
        """ Get a list of Admin User log
        """
        content = []
        with open("admin.log", "r") as ins:
        	for line in ins:
        		content.append(json.loads(line))
        	return(content)