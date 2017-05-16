# Copyright 2014, Rackspace, US, Inc.
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
"""API over the nova service.
"""
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.utils import http as utils_http
from django.views import generic

from novaclient import exceptions

from openstack_dashboard import api
from openstack_dashboard.api.rest import json_encoder
from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils
import simplejson
import os,platform
import time
from netaddr import *
import json
import socket


@urls.register
class Keypairs(generic.View):
    """API for nova keypairs.
    """
    url_regex = r'nova/keypairs/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of keypairs associated with the current logged-in
        account.

        The listing result is an object with property "items".
        """
        result = api.nova.keypair_list(request)
        return {'items': [u.to_dict() for u in result]}

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Create a keypair.

        Create a keypair using the parameters supplied in the POST
        application/json object. The parameters are:

        :param name: the name to give the keypair
        :param public_key: (optional) a key to import

        This returns the new keypair object on success.
        """
        if 'public_key' in request.DATA:
            new = api.nova.keypair_import(request, request.DATA['name'],
                                          request.DATA['public_key'])
        else:
            new = api.nova.keypair_create(request, request.DATA['name'])
        return rest_utils.CreatedResponse(
            '/api/nova/keypairs/%s' % utils_http.urlquote(new.name),
            new.to_dict()
        )


@urls.register
class Keypair(generic.View):
    url_regex = r'nova/keypairs/(?P<keypair_name>.+)/$'

    def get(self, request, keypair_name):
        """Creates a new keypair and associates it to the current project.

        * Since the response for this endpoint creates a new keypair and
          is not idempotent, it normally would be represented by a POST HTTP
          request. However, this solution was adopted as it
          would support automatic file download across browsers.

        :param keypair_name: the name to associate the keypair to
        :param regenerate: (optional) if set to the string 'true',
            replaces the existing keypair with a new keypair

        This returns the new keypair object on success.
        """
        try:
            regenerate = request.GET.get('regenerate') == 'true'
            if regenerate:
                api.nova.keypair_delete(request, keypair_name)

            keypair = api.nova.keypair_create(request, keypair_name)

        except exceptions.Conflict:
            return HttpResponse(status=409)

        except Exception:
            return HttpResponse(status=500)

        else:
            response = HttpResponse(content_type='application/binary')
            response['Content-Disposition'] = ('attachment; filename=%s.pem'
                                               % slugify(keypair_name))
            response.write(keypair.private_key)
            response['Content-Length'] = str(len(response.content))

            return response


@urls.register
class Services(generic.View):
    """API for nova services.
    """
    url_regex = r'nova/services/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of nova services.
        Will return HTTP 501 status code if the service_list extension is
        not supported.
        """
        if api.base.is_service_enabled(request, 'compute') \
           and api.nova.extension_supported('Services', request):
            result = api.nova.service_list(request)
            return {'items': [u.to_dict() for u in result]}
        else:
            raise rest_utils.AjaxError(501, '')


@urls.register
class AvailabilityZones(generic.View):
    """API for nova availability zones.
    """
    url_regex = r'nova/availzones/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of availability zones.

        The following get parameters may be passed in the GET
        request:

        :param detailed: If this equals "true" then the result will
            include more detail.

        The listing result is an object with property "items".
        """
        detailed = request.GET.get('detailed') == 'true'
        result = api.nova.availability_zone_list(request, detailed)
        return {'items': [u.to_dict() for u in result]}


@urls.register
class Limits(generic.View):
    """API for nova limits.
    """
    url_regex = r'nova/limits/$'

    @rest_utils.ajax(json_encoder=json_encoder.NaNJSONEncoder)
    def get(self, request):
        """Get an object describing the current project limits.

        Note: the Horizon API doesn't support any other project (tenant) but
        the underlying client does...

        The following get parameters may be passed in the GET
        request:

        :param reserved: This may be set to "true" but it's not
            clear what the result of that is.

        The result is an object with limits as properties.
        """
        reserved = request.GET.get('reserved') == 'true'
        result = api.nova.tenant_absolute_limits(request, reserved)
        return result


@urls.register
class Servers(generic.View):
    """API over all servers.
    """
    url_regex = r'nova/servers/$'

    _optional_create = [
        'block_device_mapping', 'block_device_mapping_v2', 'nics', 'meta',
        'availability_zone', 'instance_count', 'admin_pass', 'disk_config',
        'config_drive', 'scheduler_hints'
    ]

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of servers.

        The listing result is an object with property "items". Each item is
        a server.

        Example GET:
        http://localhost/api/nova/servers
        """
        servers = api.nova.server_list(request)[0]
        return {'items': [s.to_dict() for s in servers]}

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Create a server.

        Create a server using the parameters supplied in the POST
        application/json object. The required parameters as specified by
        the underlying novaclient are:

        :param name: The new server name.
        :param source_id: The ID of the image to use.
        :param flavor_id: The ID of the flavor to use.
        :param key_name: (optional extension) name of previously created
                      keypair to inject into the instance.
        :param user_data: user data to pass to be exposed by the metadata
                      server this can be a file type object as well or a
                      string.
        :param security_groups: An array of one or more objects with a "name"
            attribute.

        Other parameters are accepted as per the underlying novaclient:
        "block_device_mapping", "block_device_mapping_v2", "nics", "meta",
        "availability_zone", "instance_count", "admin_pass", "disk_config",
        "config_drive"

        This returns the new server object on success.
        """
        try:
            args = (
                request,
                request.DATA['name'],
                request.DATA['source_id'],
                request.DATA['flavor_id'],
                request.DATA['key_name'],
                request.DATA['user_data'],
                request.DATA['security_groups'],
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter '
                                            "'%s'" % e.args[0])
        kw = {}
        # print(request.DATA)
        print("***************************")
        print(request.DATA['node'])
        if request.DATA['node'] :
            request.DATA['availability_zone']=request.DATA['availability_zone']+":"+request.DATA['node']
            print(request.DATA['availability_zone'])
        for name in self._optional_create:
            if name in request.DATA:
                kw[name] = request.DATA[name]
        # print(kw)
        new = api.nova.server_create(*args, **kw)
        return rest_utils.CreatedResponse(
            '/api/nova/servers/%s' % utils_http.urlquote(new.id),
            new.to_dict()
        )

    @rest_utils.ajax()
    def delete(self, request):
        """Delete a list of servers.


        Example GET:
        http://localhost/api/nova/servers
        """
        try:
            args = (
                request,
                request.DATA['instances_ids'],
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter '
                                            "'%s'" % e.args[0])
        for id in request.DATA['instances_ids']:
            api.nova.reset_state(request, id, 'active')
            api.nova.server_delete(request, id)


@urls.register
class Server(generic.View):
    """API for retrieving a single server
    """
    url_regex = r'nova/servers/(?P<server_id>[^/]+|default)$'

    @rest_utils.ajax()
    def get(self, request, server_id):
        """Get a specific server

        http://localhost/api/nova/servers/1
        """
        return api.nova.server_get(request, server_id).to_dict()


@urls.register
class ServerMetadata(generic.View):
    """API for server metadata.
    """
    url_regex = r'nova/servers/(?P<server_id>[^/]+|default)/metadata$'

    @rest_utils.ajax()
    def get(self, request, server_id):
        """Get a specific server's metadata

        http://localhost/api/nova/servers/1/metadata
        """
        return api.nova.server_get(request,
                                   server_id).to_dict().get('metadata')

    @rest_utils.ajax()
    def patch(self, request, server_id):
        """Update metadata items for a server

        http://localhost/api/nova/servers/1/metadata
        """
        updated = request.DATA['updated']
        removed = request.DATA['removed']
        if updated:
            api.nova.server_metadata_update(request, server_id, updated)
        if removed:
            api.nova.server_metadata_delete(request, server_id, removed)


@urls.register
class Extensions(generic.View):
    """API for nova extensions.
    """
    url_regex = r'nova/extensions/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of extensions.

        The listing result is an object with property "items". Each item is
        an image.

        Example GET:
        http://localhost/api/nova/extensions
        """
        result = api.nova.list_extensions(request)
        return {'items': [e.to_dict() for e in result]}


@urls.register
class Flavors(generic.View):
    """API for nova flavors.
    """
    url_regex = r'nova/flavors/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of flavors.

        The listing result is an object with property "items". Each item is
        a flavor. By default this will return the flavors for the user's
        current project. If the user is admin, public flavors will also be
        returned.

        :param is_public: For a regular user, set to True to see all public
            flavors. For an admin user, set to False to not see public flavors.
        :param get_extras: Also retrieve the extra specs.

        Example GET:
        http://localhost/api/nova/flavors?is_public=true
        """
        is_public = request.GET.get('is_public')
        is_public = (is_public and is_public.lower() == 'true')
        get_extras = request.GET.get('get_extras')
        get_extras = bool(get_extras and get_extras.lower() == 'true')
        flavors = api.nova.flavor_list(request, is_public=is_public,
                                       get_extras=get_extras)
        result = {'items': []}
        for flavor in flavors:
            d = flavor.to_dict()
            if get_extras:
                d['extras'] = flavor.extras
            result['items'].append(d)
        return result

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        flavor_access = request.DATA.get('flavor_access', [])
        flavor_id = request.DATA['id']
        is_public = not flavor_access

        flavor = api.nova.flavor_create(request,
                                        name=request.DATA['name'],
                                        memory=request.DATA['ram'],
                                        vcpu=request.DATA['vcpus'],
                                        disk=request.DATA['disk'],
                                        ephemeral=request
                                        .DATA['OS-FLV-EXT-DATA:ephemeral'],
                                        swap=request.DATA['swap'],
                                        flavorid=flavor_id,
                                        is_public=is_public
                                        )

        for project in flavor_access:
            api.nova.add_tenant_to_flavor(
                request, flavor.id, project.get('id'))

        return rest_utils.CreatedResponse(
            '/api/nova/flavors/%s' % flavor.id,
            flavor.to_dict()
        )


@urls.register
class Flavor(generic.View):
    """API for retrieving a single flavor
    """
    url_regex = r'nova/flavors/(?P<flavor_id>[^/]+)/$'

    @rest_utils.ajax()
    def get(self, request, flavor_id):
        """Get a specific flavor

        :param get_extras: Also retrieve the extra specs.

        Example GET:
        http://localhost/api/nova/flavors/1
        """
        get_extras = self.extract_boolean(request, 'get_extras')
        get_access_list = self.extract_boolean(request, 'get_access_list')
        flavor = api.nova.flavor_get(request, flavor_id, get_extras=get_extras)

        result = flavor.to_dict()
        # Bug: nova API stores and returns empty string when swap equals 0
        # https://bugs.launchpad.net/nova/+bug/1408954
        if 'swap' in result and result['swap'] == '':
            result['swap'] = 0
        if get_extras:
            result['extras'] = flavor.extras

        if get_access_list and not flavor.is_public:
            access_list = [item.tenant_id for item in
                           api.nova.flavor_access_list(request, flavor_id)]
            result['access-list'] = access_list
        return result

    @rest_utils.ajax()
    def delete(self, request, flavor_id):
        api.nova.flavor_delete(request, flavor_id)

    @rest_utils.ajax(data_required=True)
    def patch(self, request, flavor_id):
        flavor_access = request.DATA.get('flavor_access', [])
        is_public = not flavor_access

        # Grab any existing extra specs, because flavor edit is currently
        # implemented as a delete followed by a create.
        extras_dict = api.nova.flavor_get_extras(request, flavor_id, raw=True)
        # Mark the existing flavor as deleted.
        api.nova.flavor_delete(request, flavor_id)
        # Then create a new flavor with the same name but a new ID.
        # This is in the same try/except block as the delete call
        # because if the delete fails the API will error out because
        # active flavors can't have the same name.
        flavor = api.nova.flavor_create(request,
                                        name=request.DATA['name'],
                                        memory=request.DATA['ram'],
                                        vcpu=request.DATA['vcpus'],
                                        disk=request.DATA['disk'],
                                        ephemeral=request
                                        .DATA['OS-FLV-EXT-DATA:ephemeral'],
                                        swap=request.DATA['swap'],
                                        flavorid=flavor_id,
                                        is_public=is_public
                                        )
        for project in flavor_access:
            api.nova.add_tenant_to_flavor(
                request, flavor.id, project.get('id'))

        if extras_dict:
            api.nova.flavor_extra_set(request, flavor.id, extras_dict)

    def extract_boolean(self, request, name):
        bool_string = request.GET.get(name)
        return bool(bool_string and bool_string.lower() == 'true')


@urls.register
class FlavorExtraSpecs(generic.View):
    """API for managing flavor extra specs
    """
    url_regex = r'nova/flavors/(?P<flavor_id>[^/]+)/extra-specs/$'

    @rest_utils.ajax()
    def get(self, request, flavor_id):
        """Get a specific flavor's extra specs

        Example GET:
        http://localhost/api/nova/flavors/1/extra-specs
        """
        return api.nova.flavor_get_extras(request, flavor_id, raw=True)

    @rest_utils.ajax(data_required=True)
    def patch(self, request, flavor_id):
        """Update a specific flavor's extra specs.

        This method returns HTTP 204 (no content) on success.
        """
        if request.DATA.get('removed'):
            api.nova.flavor_extra_delete(
                request, flavor_id, request.DATA.get('removed')
            )
        api.nova.flavor_extra_set(
            request, flavor_id, request.DATA['updated']
        )


@urls.register
class AggregateExtraSpecs(generic.View):
    """API for managing aggregate extra specs
    """
    url_regex = r'nova/aggregates/(?P<aggregate_id>[^/]+)/extra-specs/$'

    @rest_utils.ajax()
    def get(self, request, aggregate_id):
        """Get a specific aggregate's extra specs

        Example GET:
        http://localhost/api/nova/flavors/1/extra-specs
        """
        return api.nova.aggregate_get(request, aggregate_id).metadata

    @rest_utils.ajax(data_required=True)
    def patch(self, request, aggregate_id):
        """Update a specific aggregate's extra specs.

        This method returns HTTP 204 (no content) on success.
        """
        updated = request.DATA['updated']
        if request.DATA.get('removed'):
            for name in request.DATA.get('removed'):
                updated[name] = None
        api.nova.aggregate_set_metadata(request, aggregate_id, updated)


# Added By Raja S @ 26.08.16


@urls.register
class Servers_Status(generic.View):
    """API over all servers.
    """
    url_regex = r'nova/servers_status/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of servers.

        The listing result is an object with server status.

        Example GET:
        http://localhost/api/nova/servers
        """
        servers_status = api.nova.server_status(request)
        return servers_status


@urls.register
class ServersListBySearch(generic.View):
    """API over all servers.
    """
    url_regex = r'nova/servers_list_by_search/$'

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Get a list of servers.

        The listing result is an object with property "items". Each item is
        a server.

        Example GET:
        http://localhost/api/nova/recover_servers/
        """
        try:
            args = (
                request,
                request.DATA['searchterms'],
                request.DATA['searchindex'],
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])
        # status=["error","active"]
        vms = []

        for stat in request.DATA['searchterms']:
            vms_raw = api.nova.server_list(request,
                                           {request.DATA['searchindex']: stat})[0]
            vms_raw_json = [s.to_dict() for s in vms_raw]
            for vm in vms_raw_json:

                vm_obj = {}
                vm_obj['internal_ip'] = vm_obj['floating_ip'] = None
                vm_obj['instance_id'] = vm['id']
                vm_obj['instance_status'] = vm['status']
                vm_obj['task_status'] = vm['OS-EXT-STS:task_state']
                vm_obj['instance_name'] = vm['name']
                vm_obj['flavor_id'] = vm['flavor']['id']
                vm_obj['instance_volume_id'] = None
                vm_obj['other_volumes'] = []
                vm_obj['image_name']=vm['image_name']

                # rerieve IPs
                for net in vm.get('addresses', ''):
                    for nic in vm.get('addresses')[net]:
                        net_id = [x['id']
                                  for x in api.neutron.network_list(request, name=net)]
                        vm_obj['net_id'] = net_id[0]
                        if nic['OS-EXT-IPS:type'] == 'fixed':
                            vm_obj['internal_ip'] = nic['addr']
                        elif nic['OS-EXT-IPS:type'] == 'floating':
                            vm_obj['floating_ip'] = nic['addr']

                if vm_obj['internal_ip'] is not None:
                    # retrieve Volume
                    vol_raw = api.nova.instance_volumes_list(request, vm['id'])
                    vol = [v.to_dict() for v in vol_raw]
                    if len(vol) > 0:
                        for dev in vol:
                            if dev['device'] == '/dev/vda':
                                vm_obj['instance_volume_id'] = dev['id']
                            else:
                                vm_obj['other_volumes'].append(dev['id'])

                    if vm_obj['instance_volume_id'] is not None:
                        vms.append(vm_obj)

        return {'vms': vms}


@urls.register
class BackupServers(generic.View):
    """API over all servers.
    """
    url_regex = r'nova/backup_servers/$'

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Get a list of servers.

        The listing result is an object with property "items". Each item is
        a server.

        Example GET:
        http://localhost/api/nova/recover_servers/
        """
        try:
            args = (
                request,
                request.DATA['selectedInstances']
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])

        isEmpty = os.stat('backupedinstances.json').st_size
        with open('backupedinstances.json', 'r+') as bk_file:
            if isEmpty == 0:
                bk_ins = {}
                bk_ins['instances'] = request.DATA['selectedInstances']
                simplejson.dump(bk_ins, bk_file)
            else:
                existing_data = simplejson.load(bk_file)
                existing_data['instances'].extend(
                    request.DATA['selectedInstances'])
                bk_file.seek(0)
                bk_file.truncate()
                simplejson.dump(existing_data, bk_file)


@urls.register
class ReCreate(generic.View):
    """API over all servers.
    """
    url_regex = r'nova/recreate/$'

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Get a list of servers.

        The listing result is an object with property "items". Each item is
        a server.

        Example GET:
        http://localhost/api/nova/recover_servers/
        """
        try:
            args = (
                request,
                request.DATA['selectedInstances']
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])

        for ins in request.DATA['selectedInstances']:
            bdm = {'vda': ins['instance_volume_id'] + ':vol::false'}
            nic = [{'net-id': ins['net_id'],
                    'v4-fixed-ip': ins['internal_ip']}]
            time.sleep(3)
            api.nova.server_create(request,
                                   name=ins['instance_name'],
                                   image='',
                                   flavor=ins['flavor_id'],
                                   key_name=None,
                                   user_data='',
                                   security_groups=[],
                                   block_device_mapping=bdm,
                                   nics=nic,
                                   disk_config="AUTO",
                                   config_drive=False)
            time.sleep(2)
            if ins['floating_ip'] is not None:
                api.nova.addExisitingFloatingIp(
                    request, ins['instance_name'], ins['floating_ip'])


@urls.register
class AttachExtraVolumes(generic.View):
    """API over all servers.
    """
    url_regex = r'nova/attach_extra_volumes/$'

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Get a list of servers.

        The listing result is an object with property "items". Each item is
        a server.

        Example GET:
        http://localhost/api/nova/recover_servers/
        """
        try:
            args = (
                request,
                request.DATA['selectedInstances']
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])

        for ins in request.DATA['selectedInstances']:

            ins_id = [vm.id for vm in api.nova.server_list(
                request, search_opts={"name": ins['instance_name'], "status": "active"})[0]]
            for vol in ins['other_volumes']:
                api.nova.instance_volume_attach(
                    request, vol, ins_id[0], None)


@urls.register
class Servers_Without_Floating_Ip(generic.View):
    """API over all servers.
    """
    url_regex = r'nova/servers_no_floating_ip/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of servers.

        The listing result is an object with server status.

        Example GET:
        http://localhost/api/nova/servers_no_floating_ip
        """
        instances_no_floating_ip = []
        for vm in api.nova.server_list(request)[0]:
            temp = {}
            networks = []
            for net in vm.addresses:
                networks = vm.addresses[net]
            if len(networks) == 1:
                temp['instance_id'] = vm.id
                temp['instance_name'] = vm.name
                fi_target = api.network.floating_ip_target_get_by_instance(
                    request, vm.id)
                # target id is in the format : 6ead8a8f-a2c3-40aa-8313-27de4c4ba2a9_41.20.0.62
                # so In order to get id, target id is split by underscore(-)
                temp['port_id'] = fi_target
                if temp['port_id'] is not None:
                    instances_no_floating_ip.append(temp)
        return {"instances_no_fips": instances_no_floating_ip}

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        try:
            args = (
                request,
                request.DATA['selectedInstances'],
                request.DATA['poolId'],
                request.DATA['method']
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])

        instances = request.DATA['selectedInstances']

        method = request.DATA['method']

        unassigned_ips_obj = [addr for addr in
                              api.network.tenant_floating_ip_list(request)
                              if addr.instance_id is None]

        allocated_ips = [addr.ip for addr in
                         api.network.tenant_floating_ip_list(request)]

        if method == 'auto':
            for vm in instances:
                if(len(unassigned_ips_obj) >= 1):
                    IpAssociate(
                        request, unassigned_ips_obj.pop().id, vm['port_id'])
                else:
                    newIP = IPCreate(request, request.DATA['poolId'], None)
                    IpAssociate(request, newIP.id, vm['port_id'])

        if method == 'semiauto':

            selected_range = request.DATA['selectedPoolRange']

            gathered_ips = []

            ips_in_selected_range = IPRange(
                selected_range['start'], selected_range['end'])

            print("Gathering Ips in Selected Range...%d found" %
                  len(ips_in_selected_range))

            no_f_assigned_ips = 0

            for ip in allocated_ips:
                if IPAddress(ip) in ips_in_selected_range:
                    no_f_assigned_ips = no_f_assigned_ips + 1

            print("In Selected Range, Calculating IPs"
                  " already in allocated... %d found" %
                  no_f_assigned_ips)

            for aip in unassigned_ips_obj:
                if(IPAddress(aip.ip) in IPRange(selected_range['start'],
                                                selected_range['end'])):
                    gathered_ips.append(aip)

            print("In Selected Range, Calculating IPs"
                  "already in allocated but not used... %d found" %
                  len(gathered_ips))

            available_ips = len(ips_in_selected_range) + len(gathered_ips) - \
                no_f_assigned_ips

            print("In Selected Range, Calculating available"
                  "number of ips... %d found" %
                  available_ips)

            print("Check Instance Count match with available number of ips...")

            print("Instances : %d Available Ips: %d" %
                  (len(instances), available_ips))

            if len(instances) <= available_ips:
                print("Eligible for IP allocation")
                ip_generator = iter_iprange(
                    selected_range['start'], selected_range['end'], step=1)

                while (len(instances) > len(gathered_ips)):
                    new_ip = str(ip_generator.next())
                    if new_ip not in allocated_ips:
                        gathered_ips.append(new_ip)

                for vm in instances:
                    if len(gathered_ips) > 0:
                        current_ip_to_assign = gathered_ips.pop()
                        if current_ip_to_assign in unassigned_ips_obj:
                            print("Only Associated")
                            IpAssociate(
                                request,
                                current_ip_to_assign.id, vm['port_id'])
                        else:
                            print("Created and Associated")
                            newIP = IPCreate(request, request.DATA[
                                             'poolId'], current_ip_to_assign)
                            IpAssociate(request, newIP.id, vm['port_id'])

                result = {"status": "success",
                          "msg": "Floating Ips Associated"}
            else:
                result = {"status": "danger",
                          "msg": "Available Ips lesss than selected instances"}
            return result

        if method == 'manual':
            for vm in instances:
                if(len(unassigned_ips_obj) >= 1 and
                        vm['prefered_ip'] in allocated_ips):
                    IpAssociate(request,
                                getFloatingIpId(request, vm['prefered_ip']),
                                vm['port_id'])
                else:
                    newIP = IPCreate(request,
                                     request.DATA['poolId'], vm['prefered_ip'])
                    IpAssociate(request, newIP.id, vm['port_id'])

@urls.register
class HypervisorStats(generic.View):
    """API for Hypervisor Stats.
    """
    url_regex = r'nova/hypervisor_stats/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a details about hypervisor.

        The listing result is an object with property "items".
        """
        result = api.nova.hypervisor_stats(request)
        #return {'items': [u.to_dict() for u in result]}
	
        return result.to_dict()


def IpAssociate(request, ip_id, port_id):
    return api.network.floating_ip_associate(request, ip_id, port_id)


def IPCreate(request, pool_id, floating_ip):
    return api.network.tenant_floating_ip_allocate(
        request, pool_id, floating_ip)


def getFloatingIpId(request, floating_ip):
    all_ips = api.network.tenant_floating_ip_list(request)
    for f_obj in all_ips:
        if f_obj.ip == floating_ip:
            return f_obj.id

@urls.register
class downloadJson(generic.View):
    """API for Hypervisor Stats.
    """
    url_regex = r'nova/download-json/$'

    @rest_utils.ajax()
    def post(self, request):
        """Get a details about recreate blue screnn instances
        

        The listing result is an object with property "items".
        """
        print("Download JSON")
        instances=(request.DATA['selectedInstances'])
        input=request.DATA
        json_string = json.dumps(input)
        with open("static/instances.json", 'w') as outfile:
                outfile.write(json_string)
                outfile.close()
        return ("static/instances.json")

@urls.register
class recreates_instances(generic.View):
    """API for recreate blue screen error instances.
    """
    url_regex = r'nova/recreates_instances/$'
    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Get a list of servers.

        The listing result is an object with property "items". Each item is
        a server.

        Example GET:
        http://localhost/api/nova/recover_servers/
        """
        try:
            args = (
                request,
                request.DATA['selectedInstances']
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])

        for ins in request.DATA['selectedInstances']:
            bdm = {'vda': ins['instance_volume_id'] + ':snap::false'}
            nic = [{'net-id': ins['net_id'],
                    'v4-fixed-ip': ins['internal_ip']}]
            time.sleep(3)

            api.nova.server_create(request,
                                   name=ins['instance_name'],
                                   image='',
                                   flavor=ins['flavor_id'],
                                   key_name=None,
                                   user_data='',
                                   security_groups=[],
                                   block_device_mapping=bdm,
                                   nics=nic,
                                   disk_config="AUTO",
                                   config_drive=False)
            time.sleep(15)
            if ins['floating_ip'] is not None:
                api.nova.addExisitingFloatingIp(
                    request, ins['instance_name'], ins['floating_ip'])


def check_rdp(ip=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((ip, 3389))
    if result == 0:
        return True
    else:
        return False
    s.close()

# def ping_check(hostname=None):
#     response=os.system("/bin/ping -c 1" + hostname)
#     if response == 0:
#        return True
#     else:
#        return False

def ping_check(hostname=None):
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
    status=os.system("ping " + ping_str + " " + hostname) == 0
    return status

@urls.register
class instances_check(generic.View):
    """API over all servers.
    """
    url_regex = r'nova/instances_rdpcheck/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of servers in active state .
        """  
        with open('instance_rdpstatus.json') as data_file:
            data = json.loads(data_file.read())
            return(data)      
        # vms = []
        # vms_raw = api.nova.server_list(request,search_opts={"status": "active"})[0]    
        # vms_raw_json = [s.to_dict() for s in vms_raw]
        # for vm in vms_raw_json:

        #     vm_obj = {}
        #     vm_obj['internal_ip'] = vm_obj['floating_ip'] = None
        #     vm_obj['instance_id'] = vm['id']
        #     vm_obj['instance_status'] = vm['status']
        #     vm_obj['task_status'] = vm['OS-EXT-STS:task_state']
        #     vm_obj['instance_name'] = vm['name']
        #     vm_obj['flavor_id'] = vm['flavor']['id']
        #     vm_obj['instance_volume_id'] = None
        #     vm_obj['other_volumes'] = []
        #     vm_obj['image_name']=vm['image_name']

        #     # rerieve IPs
        #     for net in vm.get('addresses', ''):
        #         for nic in vm.get('addresses')[net]:
        #             net_id = [x['id']
        #                       for x in api.neutron.network_list(request, name=net)]
        #             vm_obj['net_id'] = net_id[0]
        #             if nic['OS-EXT-IPS:type'] == 'fixed':
        #                 vm_obj['internal_ip'] = nic['addr']
        #             elif nic['OS-EXT-IPS:type'] == 'floating':
        #                 vm_obj['floating_ip'] = nic['addr']

        #     if vm_obj['internal_ip'] is not None:
        #         # retrieve Volume
        #         vol_raw = api.nova.instance_volumes_list(request, vm['id'])
        #         vol = [v.to_dict() for v in vol_raw]
        #         if len(vol) > 0:
        #             for dev in vol:
        #                 if dev['device'] == '/dev/vda':
        #                     vm_obj['instance_volume_id'] = dev['id']
        #                 else:
        #                     vm_obj['other_volumes'].append(dev['id'])

        #         if vm_obj['instance_volume_id'] is not None:
        #             vms.append(vm_obj)

        #     if vm_obj['floating_ip']:               
        #         rdp_status=check_rdp(ip=vm_obj['floating_ip'])
        #         vm_obj['rdp_status']=rdp_status
        #         if not rdp_status :                    
        #             vm_state=ping_check(hostname=vm_obj['floating_ip'])
        #             print(vm_state)
        #             vm_obj['vm_state']=vm_state
        #         else:
        #             vm_obj['vm_state']=True

        #     else:
        #         vm_obj['rdp_status']=None
        #         vm_obj['vm_state']=None

        # return {'vms': vms}

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Get a list of servers.

        The listing result is an object with property "items". Each item is
        a server.

        Example GET:
        http://localhost/api/nova/recover_servers/
        """
        try:
            args = (
                request,
                request.DATA['instance_id']
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])
        
        instance_id=request.DATA['instance_id']

        restart_status=api.nova.server_reboot(request,instance_id)
        return restart_status        
        


@urls.register
class VmMonitoring(generic.View):
    """API over all servers.
    """
    url_regex = r'nova/vm_monitoring/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of servers in active state .
        """  
        with open('vm_monitoring.json') as data_file:
            data = json.loads(data_file.read())
            return(data)      

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Get a list of servers.

        The listing result is an object with property "items". Each item is
        a server.

        Example GET:
        http://localhost/api/nova/recover_servers/
        """
        try:
            args = (
                request,
                request.DATA['instance_id']
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])
        
        instance_id=request.DATA['instance_id']

        restart_status=api.nova.server_reboot(request,instance_id)
        return restart_status


@urls.register
class Hostlist(generic.View):
    """API for nova host name lists.
    """
    url_regex = r'nova/hostlist/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of nova node names.
        Will return HTTP 501 status code if the service_list extension is
        not supported.
        """
        if api.base.is_service_enabled(request, 'compute') \
                and api.nova.extension_supported('Services', request):
            result = api.nova.service_list(request, binary="nova-compute")
            return {'all_hosts': [host.host for host in result]}
        else:
            raise rest_utils.AjaxError(501, '')