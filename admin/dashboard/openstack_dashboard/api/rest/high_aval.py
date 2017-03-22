from django.views import generic
from openstack_dashboard import api

from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils
from django.conf import settings
import kazoo.exceptions as kexception
import kazoo
from kazoo.client import KazooClient
kazoo_host_ipaddress='192.168.30.52:2181,192.168.30.53:2181,192.168.30.54:2181'
path="/openstack_ha/hosts/start_migration/"
zk = KazooClient(hosts=kazoo_host_ipaddress)



def down_hosts(result):
	return [host.host for host in result if host.state.lower() == 'down']

@urls.register
class Users(generic.View):
    """API for AD User Lists, Creation, Disable.
    """
    url_regex = r'ha/high_availability/$'

    @rest_utils.ajax()
    def get(self, request):
        """ Get a list of AD Users
        """
        result = api.nova.service_list(request,binary="nova-compute")
        hosts=down_hosts(result)
        if len(hosts)==1:
        	try:
        		zk.start()
        		zk.create(path+hosts[0]) 
        		return("successfully started migration...!")      		
        	except Exception as e:
        		print(e)
        		return("unable to start Force migration...!")
        else:
        	return ("Unmanageable disaster...!")


    @rest_utils.ajax(data_required=True)
    def post(self, request):       
    	zk.start()
    	# result = api.nova.service_list(request,binary="nova-compute")
    	# name=host.host for host in api.nova.services.list(binary="nova-compute") if host.state.lower() == 'down'
    	# print(name)
    	# print(result)
        print("----------------------------------------")
        print(request.DATA['down_nodes']['name'])
        print("----------------------------------------")
        if request.DATA['down_nodes']['create']:
        	zk.create(path+request.DATA['down_nodes']['name'])
        elif request.DATA['down_nodes']['delete']:
          	 zk.delete(path + request.DATA['down_nodes']['name'], recursive=True)
   




    