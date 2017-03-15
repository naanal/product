# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
Context processors used by Horizon.
"""

import re

from django.conf import settings
from local.local_settings import *
from settings import *

from horizon import conf


def openstack(request):
    """Context processor necessary for OpenStack Dashboard functionality.

    The following variables are added to the request context:

    ``authorized_tenants``
        A list of tenant objects which the current user has access to.

    ``regions``

        A dictionary containing information about region support, the current
        region, and available regions.
    """
    context = {}

    # Auth/Keystone context
    context.setdefault('authorized_tenants', [])
    if request.user.is_authenticated():
        context['authorized_tenants'] = [
            tenant for tenant in
            request.user.authorized_tenants if tenant.enabled]

    # Region context/support
    available_regions = getattr(settings, 'AVAILABLE_REGIONS', [])
    regions = {'support': len(available_regions) > 1,
               'current': {'endpoint': request.session.get('region_endpoint'),
                           'name': request.session.get('region_name')},
               'available': [{'endpoint': region[0], 'name':region[1]} for
                             region in available_regions]}
    context['regions'] = regions

    # Adding webroot access
    context['WEBROOT'] = getattr(settings, "WEBROOT", "/")

    # Search for external plugins and append to javascript message catalog
    # internal plugins are under the openstack_dashboard domain
    # so we exclude them from the js_catalog
    js_catalog = ['horizon', 'openstack_dashboard']
    regex = re.compile(r'^openstack_dashboard')
    all_plugins = conf.HORIZON_CONFIG['plugins']
    js_catalog.extend(p for p in all_plugins if not regex.search(p))
    context['JS_CATALOG'] = '+'.join(js_catalog)

    context['KEYSTONE_URL'] = OPENSTACK_KEYSTONE_URL
    context['SAN_STORAGE_URL'] = SAN_STORAGE_URL
    context['T_CPU_TEXT'] = T_CPU_TEXT
    context['T_RAM_TEXT'] = T_RAM_TEXT
    context['T_DISK_TEXT'] = T_DISK_TEXT
    context['C_CPU_TEXT'] = C_CPU_TEXT
    context['C_RAM_TEXT'] = C_RAM_TEXT
    context['C_DISK_TEXT'] = C_DISK_TEXT
    context['CPU_USAGE'] = CPU_USAGE
    context['RAM_USAGE'] = RAM_USAGE
    context['DISK_READ'] = DISK_READ
    context['DISK_WRITE'] = DISK_WRITE
    context['BYTES_SENT'] = BYTES_SENT
    context['BYTES_RECEVIED'] = BYTES_RECEVIED
    context['NETWORK_HOST'] = NETWORK_HOST
    context['DOCKER_TOTAL_TEXT'] = DOCKER_TOTAL_TEXT
    context['DOCKER_RUNNING_TEXT'] = DOCKER_RUNNING_TEXT
    context['DOCKER_STOPPED_TEXT'] = DOCKER_STOPPED_TEXT
    context['ALERTS'] = ALERTS
    context['DISK_USAGE'] = DISK_USAGE
    context['C2_CPU_TEXT'] = C2_CPU_TEXT
    context['C2_RAM_TEXT'] = C2_RAM_TEXT
    context['C2_DISK_TEXT'] = C2_DISK_TEXT
    context['C3_CPU_TEXT'] = C3_CPU_TEXT
    context['C3_RAM_TEXT'] = C3_RAM_TEXT
    context['C3_DISK_TEXT'] = C3_DISK_TEXT
    return context
