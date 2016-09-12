
# Copyright 2015, Hewlett-Packard Development Company, L.P.
# Copyright 2016 IBM Corp.
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
"""API for the network abstraction APIs.
"""

from django.views import generic

from openstack_dashboard import api
from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils
from netaddr import *

@urls.register
class SecurityGroups(generic.View):
    """API for Network Abstraction

    Handles differences between Nova and Neutron.
    """
    url_regex = r'network/securitygroups/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of security groups.

        The listing result is an object with property "items". Each item is
        a security group.

        Example GET:
        http://localhost/api/network/securitygroups
        """

        security_groups = api.network.security_group_list(request)

        return {'items': [sg.to_dict() for sg in security_groups]}


@urls.register
class FloatingIP(generic.View):
    """API for a single floating IP address.
    """
    url_regex = r'network/floatingip/$'

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Allocate a new floating IP address.

        :param pool_id: The ID of the floating IP address pool in which to
                        allocate the new address.

        :return: JSON representation of the new floating IP address
        """
        pool = request.DATA['pool_id']
        result = api.network.tenant_floating_ip_allocate(request, pool)
        return result.to_dict()

    @rest_utils.ajax(data_required=True)
    def patch(self, request):
        """Associate or disassociate a floating IP address.

        :param address_id: The ID of the floating IP address to associate
                           or disassociate.
        :param port_id: The ID of the port to associate.
        """
        address = request.DATA['address_id']
        port = request.DATA.get('port_id')
        if port is None:
            api.network.floating_ip_disassociate(request, address)
        else:
            api.network.floating_ip_associate(request, address, port)


@urls.register
class FloatingIPs(generic.View):
    """API for floating IP addresses.
    """
    url_regex = r'network/floatingips/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of floating IP addresses.

        The listing result is an object with property "items". Each item is
        an extension.

        Example:
        http://localhost/api/network/floatingips
        """
        result = api.network.tenant_floating_ip_list(request)
        return {'items': [ip.to_dict() for ip in result]}


@urls.register
class FloatingIPPools(generic.View):
    """API for floating IP pools.
    """
    url_regex = r'network/floatingippools/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of floating IP pools.

        The listing result is an object with property "items". Each item is
        an extension.

        Example:
        http://localhost/api/network/floatingippools
        """
        result = api.network.floating_ip_pools_list(request)
        return {'items': [p.to_dict() for p in result]}


@urls.register
class FloatingIPTargets(generic.View):
    """API for floating IP pools.
    """
    url_regex = r'network/floatingiptargets/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of floating IP pools.

        The listing result is an object with property "items". Each item is
        an extension.

        Example:
        http://localhost/api/network/floatingippools
        """
        result = api.network.floating_ip_target_list(request)
        return {'items': [p.to_dict() for p in result]}


# Created By Raja

@urls.register
class FloatingIPPoolsRanges(generic.View):
    """API for floating IP pools ranges.
    """
    url_regex = r'network/floatingippoolsranges/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of floating IP pools ranges.

        The listing result is an object with property "items". Each item is
        an extension.

        Example:
        http://localhost/api/network/floatingippools
        """
        pools_range = []
        temp = {}
        pools = api.network.floating_ip_pools_list(request)
        for pool in pools:
            temp['pool_id'] = pool.id
            temp['pool_name'] = pool.name
            temp['pools'] = []
            for subnet in pool.subnets:
                params = {'id': subnet}
                subnet_details = api.neutron.subnet_list(request, **params)[0]
                # subnet_temp['subnet_id'] = subnet_details.id
                # subnet_temp['subnet_name'] = subnet_details.name
                temp['pools'].extend(subnet_details.allocation_pools)
            pools_range.append(temp)
        return pools_range


@urls.register
class FloatingIPPoolsRanges(generic.View):
    """API for floating IP pools ranges.
    """
    url_regex = r'network/availablefloatingips_in_range/$'

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        try:
            args = (
                request,
                request.DATA['selected_range'],
                request.DATA['instance_count']
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])

        selected_range = request.DATA['selected_range']
        instance_count = request.DATA['instance_count']

        unassigned_ips = set([addr.ip for addr in
                              api.network.tenant_floating_ip_list(request)
                              if addr.instance_id is None])

        allocated_ips = set([addr.ip for addr in
                             api.network.tenant_floating_ip_list(request)])

        already_associated = list(allocated_ips - unassigned_ips)

        already_associated_set = IPSet(already_associated)

        already_associated_ranges = list(already_associated_set.iter_ipranges())

        ranges_set = IPSet(IPRange(
            selected_range['start'], selected_range['end']))

        for associated_range in already_associated_ranges:
            print(associated_range)
            ranges_set.remove(associated_range)


        available_ips = []

        for ip in ranges_set:
            if len(available_ips) < instance_count:
                available_ips.append(ip)
            else:
                break
        return { "available_ips": available_ips }
