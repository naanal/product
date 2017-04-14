#!/usr/bin/python
from keystoneauth1 import loading
from keystoneauth1 import session
from keystoneclient.v3 import client as keystone_client
from novaclient import client as nova_client
from cinderclient import client as cinder_client
from neutronclient.v2_0 import client as neutron_client
import socket
import os, platform
import json
import simplejson
import  time
controller_ip="192.168.30.200"  # kolla_internal_vip_address
password="admin" # keystone_admin_password on passwords.yaml
project_name="admin"
username="admin"
auth_url="http://%s:35357/v2.0"%controller_ip
dump_directory="/home/naanal/Documents/testing_dash/product/admin/dashboard/" 

def init():
    try:
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(auth_url=auth_url,
                                username=username,
                                password=password,
                                 project_name=project_name)
        sess = session.Session(auth=auth)
        nova = nova_client.Client(2, session=sess)
        cinder = cinder_client.Client(2, session=sess)
        neutron = neutron_client.Client(session=sess)
        return  neutron,cinder,nova
    except Exception as e:
        raise Exception('nova cinder object init error...!')

        
def info_collection(nova,cinder,instance_id):
    try:
        instance = nova.servers.get(instance_id)
        info = instance._info
        ip_list = floating_ip_check(info)
        bdm, extra = cinder_volume_check(info, cinder=cinder)
        return instance,info,ip_list,bdm, extra
    except Exception as e:
        raise Exception('info collection error...!')

def floating_ip_check(info):
    for net in info.get('addresses', ''):
        tmp_list = []
        tmp_ip = []
        fix_ip = ''
        for nic in info.get('addresses')[net]:
            if nic['OS-EXT-IPS:type'] == 'fixed':
                fix_ip = nic['addr']
            elif nic['OS-EXT-IPS:type'] == 'floating':
                tmp_ip.append(nic['addr'])
        tmp_list.extend([(flt_ip, fix_ip) for flt_ip in tmp_ip])
        return tmp_list

def get_fixed_ip(info,neutron):
    try:
        nics = []
        for net in info.get('addresses',''):
            tmp_dict = {}
            for nic in info.get('addresses')[net]:
                net_id = [ x['id'] for x in neutron.list_networks(name=net)['networks'] if len(x) ]
                tmp_dict['net-id'] = net_id[0]
                for port in info.get('addresses')[net][0]:
                    tmp_dict['v%s-%s-ip'%(nic['version'],nic['OS-EXT-IPS:type'])]= nic['addr']
                    nics.append(tmp_dict)
                    return nics
    except Exception as e:
        print(e)

def cinder_volume_check(info, cinder=None):
    """info - instance._info - Information from instance Object
    This Function should uncheck Volume_delete_on_terminate and return volume details
    Should Change Volume Status from in_use to available"""

    bdm = {}
    volumes = {}
    try:
        volumes = {cinder.volumes.get(x['id']).attachments[0]['device']: x['id'] for x in
                   info.get('os-extended-volumes:volumes_attached')}

        # tmp_volumes = [ for x in info.get('os-extended-volumes:volumes_attached') ]
        # volumes = {cinder.volumes.get(x['id']).attachments[0]['device']:x['id'] for x in tmp_volumes }

        if volumes.has_key('/dev/vda'):
            bdm = {'vda': volumes['/dev/vda']}
            del (volumes['/dev/vda'])

    except Exception as e:
        # log.warning(e)
        bdm = None
    else:
        # if block_device_mapping.has_key('vda'):
        #    image=''
        pass
    return bdm, volumes

def check_rdp(ip=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((ip, 3389))
    if result == 0:
        return True
    else:
        return False
    s.close()

def ping(host=None):
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
    status=os.system("ping " + ping_str + " " + host) == 0
    return status

def json_dump_write(filename="instance_rdpstatus.json",data=None):
    file_path = dump_directory + filename
    print(file_path)
    #filepath = filename
    with open(file_path, 'w') as outfile:
        outfile.write(data)        
        outfile.close()
        
def run_always():
    try:
        while True:
            vms = []
            neutron, cinder, nova = init()
            ins_list = nova.servers.list(search_opts={"status": "active"})

            for ins in ins_list:
                vm_obj = {}
                instance, info, ip_list, bdm, extra = info_collection(nova, cinder, ins.id)

                nics = get_fixed_ip(info, neutron)
                volumes = {}

                if bool(extra):
                    volumes.update(extra)
                    volume = volumes
                else:
                    volume = volumes

                if (bdm):
                    volume_id = bdm['vda']

                else:
                    volume_id = None

                if not nics:
                    internal_ip = None
                else:
                    internal_ip = nics[0]['v4-fixed-ip']

                if ip_list:
                    floating_ip = ip_list[0][0]
                    ip = ip_list[0][0]
                    status = check_rdp(ip=ip)
                    if (status):
                        rdp_status = status
                        vm_state = status

                    else:
                        rdp_status = status
                        ping_status = ping(host=ip)
                        if ping_status:
                            vm_state = ping_status
                        else:
                            vm_state = ping_status
                else:
                    rdp_status = None
                    vm_state = None
                    floating_ip = None
                data = {"flavor_id": info['flavor']['id'],
                        "floating_ip": floating_ip,
                        "image_name": dict(info['image']).get('id', ''),
                        "instance_id": instance.id,
                        "instance_name": instance.name,
                        "instance_status": instance.status,
                        "instance_volume_id": volume_id,
                        "internal_ip": internal_ip,
                        "net_id": nics[0]['net-id'],
                        "other_volumes": volume,
                        "rdp_status": rdp_status,
                        "task_status": "null",
                        "vm_state": vm_state}
                vms.append(data)
            vms1 = {"vms": vms}
            instances_rdpstatus = json.dumps(vms1, ensure_ascii=True)
            json_dump_write(data=instances_rdpstatus)
            time.sleep(300)
            print("After 30 seconds")

    except Exception as e:
        print (e)
        run_always()
        
run_always()
