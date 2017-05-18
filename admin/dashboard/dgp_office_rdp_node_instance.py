#!/usr/bin/python
from novaclient import client as nova_client
from cinderclient import client as cinder_client
from neutronclient.v2_0 import client as neutron_client
import socket
import os, platform
import json
import simplejson
import  time
controller_ip="192.168.30.231"
user ="admin"
passwd = "admin"
tenant = "admin"
dump_directory="/home/dashboard/product/admin/dashboard/"
import smtplib
import string

#-------------------------Notification mail-------------------------------
email = "naanal"
pwd = "************************"
to_email = ['naanalteam@gmail.com','naanaldgp@naanal.in']

#------------------------Slack--------------------------------------------

from slackclient import SlackClient
slack_client = SlackClient('xoxp-29804153346-29865765217-185394003318-71ab4e2067af11d66c5609d3b2c0f947')
channel="test_rdp_status"


def init():
    try:
        neutron = neutron_client.Client(username=user,password=passwd,tenant_name=tenant,auth_url="http://%s:5000/v2.0"%controller_ip)
        cinder = cinder_client.Client(1,user,passwd,tenant,"http://%s:5000/v2.0"%controller_ip)
        nova = nova_client.Client(2,user,passwd,tenant,"http://%s:5000/v2.0"%controller_ip,connection_pool=True)
        return  neutron,cinder,nova
    except Exception as e:
        raise Exception('nova cinder object init error...!')
def info_collection(nova,instance_id,cinder):
    try:
        print("Inside the info_collection...!")
        instance = nova.servers.get(instance_id)
        info = instance._info
        ip_list = floating_ip_check(info)
        return instance,info,ip_list
    except Exception as e:
        print("ERROR")


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

def check_rdp(ip=None):
    result=os.system("nc -z -v -w2 %s 3389" %(ip))
    if result == 0:
        return True
    else:
        return False
    s.close()

def ping(host=None):
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
    status=os.system("ping -w 2" + ping_str + " " + host) == 0
    return status

def json_dump_write(filename="instance_rdpstatus.json",data=None):
    print("inside json file write")
    file_path = dump_directory + filename
    print(file_path)
    #filepath = filename
    with open(file_path, 'w') as outfile:
        outfile.write(data)
        outfile.close()

    
def notification_mail(subj="",msg="",to_email=to_email,email=email,pwd=pwd):
    server = smtplib.SMTP('smtp.webfaction.com',25)
    server.starttls()
    server.login(email,pwd)

    subj = subj
    msg = msg
    email = email + "@naanal.in"
    print("mail in commonfunctions.........!!!")

    for i in to_email:
        BODY = string.join((
            "From: %s" % email,
            "To: %s" % to_email,
            "Subject: %s" % subj ,
            "",
            msg
            ), "\r\n")
        server.sendmail(email,to_email,BODY)
    server.quit()

def generate_msg(RDP_failed_instance=None):   
    f=''
    for i in range(0,len(RDP_failed_instance)):
        f=f+RDP_failed_instance[i]+','        
    notification_slack(channel,f)
    #notification_mail(subj="RDP failed instances",msg=f,to_email=to_email,email=email,pwd=pwd)
    
def notification_slack(channel,msg):
    slack_client.api_call( "chat.postMessage",channel=channel,text=msg)

def run_alway():        
    try:
        while True:    
            vms = []
            node_vm_status=[]
            RDP_failed_instance=[]
            neutron, cinder, nova = init()
            all_nodes=[host.host for host in nova.services.list(binary="nova-compute")]
            i=0
            #             print("alll nodes",all_nodes)
            for node in all_nodes:
                active_instance_count=0
                shutoff_instnce_count=0
                error_instance_count=0     
                unable_rdp_instance_count=0
                ins_list = nova.servers.list(search_opts={"host": node})
                print("Instance in "+node,ins_list)
                try:
            #                     print(ins_list)
                    for ins in ins_list:
            #                         print(ins)
                        if ins.status=="ACTIVE":
            #                             print('inside active')
                            i=i+1                   
                            vm_obj = {}
                            #instance, info, ip_list = info_collection(nova, cinder, ins.id)  
                            instance = nova.servers.get(ins.id)
                            info = instance._info
                            ip_list = floating_ip_check(info)
                            nics = get_fixed_ip(info, neutron)
                            if not nics:
                                internal_ip = None
                            else:
                                internal_ip = nics[0]['v4-fixed-ip']
                            if ip_list:
                                floating_ip = ip_list[0][0]
                                ip = ip_list[0][0]
                                status = check_rdp(ip=ip)
                                if (status):
                                    active_instance_count=active_instance_count+1                        
                                    rdp_status = status
                                    vm_state = status
                                else:
                                    rdp_status = status
                                    RDP_failed_instance.append(instance.name)                                    
                                    unable_rdp_instance_count=unable_rdp_instance_count+1
                                    ping_status = ping(host=ip)
                                    if ping_status:
                                        vm_state = ping_status
                                    else:
                                        vm_state = ping_status
                            else:
                                rdp_status = None
                                vm_state = None
                                floating_ip = None
                            data = {"floating_ip": floating_ip,
                                    "instance_status": instance.status,
                                    "internal_ip": internal_ip,
                                    "rdp_status": rdp_status,
                                    "instance_name": instance.name,
                                    "vm_state": vm_state,
                                    "instance_host":info['OS-EXT-SRV-ATTR:host'],
                                     "instance_id": instance.id}
                            vms.append(data)
                            #print(data)
                            print("----------------------",i,"---------------")
                        elif ins.status=="SHUTOFF":
                        #print("inside the shutoff")
                            shutoff_instnce_count=shutoff_instnce_count+1
                        else :
                            error_instance_count=error_instance_count+1
                    node_details={'node_name':node,'total':len(ins_list),'RDP:Inactive':unable_rdp_instance_count,'RDP:Active':active_instance_count,'Shutoff':shutoff_instnce_count,'Error':error_instance_count} 
                    node_vm_status.append(node_details)
                    #print(node_vm_status)
                except Exception as e:
                    print (e)
                    pass
            #print(node_vm_status)
            vms1 = {"vms": vms,"node_details":node_vm_status}
            #print(vms1)
            instances_rdpstatus = json.dumps(vms1, ensure_ascii=True)
            json_dump_write(data=instances_rdpstatus)
            generate_msg(RDP_failed_instance)
            print("------------------------------------------------------")
            print("finished")
            time.sleep(30)            
    except Exception as e:
            print (e)
            run_alway()
run_alway()
