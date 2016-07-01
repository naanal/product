from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import ldap
import ldap.modlist as modlist
import base64
import MySQLdb
from keystoneclient.auth.identity import v3
from keystoneclient import session
from keystoneclient.v3 import client as ksclient
from novaclient import client
import time
import unicodedata
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
import os
from django.contrib.sessions.models import Session
import ldap3
from ldap3 import Server, Connection, SUBTREE, ALL, ALL_ATTRIBUTES, \
    ALL_OPERATIONAL_ATTRIBUTES, MODIFY_REPLACE, MODIFY_ADD




@csrf_exempt
#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginpage(request):
    state = "Please log in below..."
    username = password = instance_id = instance_name = status = console = fixed =conn= ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        request.session['username'] = username
        user_name = '%s@naanal.local' % username
        password = password
        print "-----------------------------------------------------------inside loginpage method---------------------------------------"
        print "username::::"+user_name,"password::::"+password
        try:
            s = Server('windows-server', port=636, use_ssl=True, get_info=ALL)
            conn = Connection(s, user=user_name, password=password, auto_bind=True)
            print"------------------------------------------------------loginpage authentication--------------------------"
            print conn
            instance_name=get_assigned_computer(username)
            status = instance_status(instance_name)
            instance_id=get_instance_id(instance_name)
            fixed=get_instance_ipaddress(instance_name)
            floating_ip=get_instance_floatingip(instance_name)

            print "instance_id:::::"+instance_id,"\n fixed::::"+fixed,"\n status:::"+status,"\n instance_name"+instance_name
            print status           
            if status =="ACTIVE":
               console=vnc_console(instance_name)
               button_color = "btn btn-danger btn-xs"
               print console
            else:
                button_color = "btn btn-success btn-xs "
            rdp_file=download_RDP(username,instance_id,instance_name)
            print "\n rdp_file:::"+rdp_file
            return render_to_response('index.html',{'password':password, 'username': username,'instancename':instance_name,'instanceid':instance_id,'status':status,'console':console,'fixedip':fixed,'floatingip':floating_ip,'RDP_file':rdp_file,'button_color':button_color})
        except ldap3.core.exceptions.LDAPBindError:           
            state= 'Wrong username or password'
        except ldap3.core.exceptions.LDAPSocketOpenError:
            state= 'AD server not available'
    return render_to_response('login.html',{'state':state})




@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if request.GET:
        username = request.GET.get('username')
        state = "Please log in below..."
        del request.session['username']
        return render_to_response('login.html',{'state':state})



@csrf_exempt
def index_page(request):
    username = password = instance_id =instance_name = status = console = ''
    if request.GET:
        username = request.GET.get('username')
        if request.session.has_key('username'):
           username1 = request.session['username']
           instance_name = get_assigned_computer(username)
           status = instance_status(instance_name)
           instance_id = get_instance_id(instance_name)
           fixed = get_instance_ipaddress(instance_name)
           floating_ip = get_instance_floatingip(instance_name)
           rdp_file = download_RDP(username, instance_id, instance_name)
           if status == "ACTIVE":
               console = vnc_console(instance_name)
               button_color = "btn btn-danger btn-xs"
               print console
           else:
               button_color = "btn btn-success btn-xs "
           return render_to_response('index.html',{'password':password, 'username': username,'instancename':instance_name,'instanceid':instance_id,'status':status,'console':console,'fixedip':fixed,'floatingip':floating_ip,'RDP_file':rdp_file,'button_color':button_color})
    
    return render_to_response('login.html')





@csrf_exempt
def change_password(request):
    username = password = console=''
    if request.GET:
        if request.session.has_key('username'):
           username1 = request.session['username']    
           username = request.GET.get('username')
           password = request.GET.get('password')
           return render_to_response('changepassword.html',{'password':password, 'username': username})       
    
    if request.POST:
        if request.session.has_key('username'):
           username1 = request.session['username']      
           username = request.POST.get('username')      
           password = request.POST.get('currentpassword')
           new_password = request.POST.get('newpassword')
           new_password1=str(new_password)
           print new_password
           print "--------------inside the changepassword method-----------------"
           print "username:::"+username,"password:::"+password,"new_password:::"+new_password1
           user_name = '%s@naanal.local' % username
           password = password          
           try :
                s = Server('windows-server', port=636, use_ssl=True, get_info=ALL)
                conn = Connection(s, user=user_name, password=password, auto_bind=True)
                print "------------ current username and password authentication-----------"
                print 'user current password authentication successfull' 
                conn.unbind()
                conn=bind()
                print "--------------change password with new_password----------"
                dn="cn=%s,ou=Police,dc=naanal,dc=local" % username
                print "dn:::"+dn
                unicode_pass = unicode('"' + new_password1 + '"', 'iso-8859-1')
                encoded_pass = unicode_pass.encode('utf-16-le')
                conn.modify(dn, {'unicodePwd': [(MODIFY_REPLACE, [encoded_pass])]})
                conn.modify(dn, {'unicodePwd': [(MODIFY_REPLACE, [encoded_pass])]})
                status=conn.result['description']
                print "change_password status::::"+status
                #status='success'
                return render_to_response('changepassword.html',{'password':password, 'username': username, 'status': status})   
           except ldap3.core.exceptions.LDAPBindError:                
                status='worng current password'
                return render_to_response('changepassword.html',{'password':password, 'username': username, 'status': status}) 
                print 'Wrong username or password'
           except ldap3.core.exceptions.LDAPSocketOpenError:
                print 'windows active directory not available'

    return render_to_response('login.html')


def help(request):
    username = password = ''
    if request.GET:
        if request.session.has_key('username'):
           username1 = request.session['username']    
           username = request.GET.get('username')
           return render_to_response('help.html',{'username': username})
    return render_to_response('login.html')

@csrf_exempt
def instance_stop(request):
    instance_id=console=username= password= ''
    if request.POST:
        if request.session.has_key('username'):
           username1 = request.session['username']
           print"-----------------inside instance_stop/start/restart method--------------"
           instance_id = request.POST.get('instance_id')
           username = request.POST.get('user_name')
           instance_name=request.POST.get('instance_name')
           operation=request.POST.get('operation')
           username=str(username)
           rdp_file = download_RDP(username, instance_id, instance_name)
           nova=get_nova_keystone_auth()
           server = nova.servers.find(name=instance_name)
           status=str(server.status)
           print "\n instance_name:::"+instance_name,"\n instance_id::::"+instance_id
           if status == 'ACTIVE':
               print "------------instance stop-------------------"
               server.stop()
               status = instance_status(instance_name)
               timeout = time.time() + 4*5   # 5 minutes from now
               while status !='SHUTOFF':
                     status = instance_status(instance_name)
                     test = 0
                     if test == 5 or time.time() > timeout:
                        break
                     test = test - 1
               button_color="btn btn-success btn-xs "
               
           elif status == 'SHUTOFF':
               print "------------instance start-------------------"
               server.start()
               status = instance_status(instance_name)
               timeout = time.time() + 4*5   # 5 minutes from now
               while status !='ACTIVE':
                     status = instance_status(instance_name)
                     test = 0
                     if test == 5 or time.time() > timeout:
                        break
                     test = test - 1
               button_color="btn btn-danger btn-xs"
               console=vnc_console(instance_name)
           elif operation == 'reboot':
               print "------------instance reboot-------------------"
               server.reboot(reboot_type='SOFT')
               status = instance_status(instance_name)
               timeout = time.time() + 4*5   # 5 minutes from now
               while status !='ACTIVE':
                     status=instance_status(instance_id)
                     test = 0
                     if test == 5 or time.time() > timeout:
                        break
                     test = test - 1
               console=server.get_vnc_console('novnc')
               console1=console['console']
               console=console1['url']
               console=str(console)
               button_color = "btn btn-danger btn-xs"
           elif operation == 'rdp':               
               print rdp_file
           fixed = get_instance_ipaddress(instance_name)
           floating_ip = get_instance_floatingip(instance_name)
           time.sleep(5)
           status = instance_status(instance_name)
           print "fixed_ip:::"+fixed,"\n floating_ip::::"+floating_ip,"\n status of instance:::"+status,"\n console_url:::"+console

           return render_to_response('index.html',{'password':password, 'username': username,'instancename':instance_name,'instanceid':instance_id,'status':status,'console':console,'RDP_file':rdp_file,'fixedip':fixed,'floatingip':floating_ip,'button_color':button_color})
    return render_to_response('login.html')





def get_assigned_computer(username):
    assigned_computer=''   
    conn=bind()   
    conn.search(search_base='dc=naanal,dc=local',
                search_filter='(&(sAMAccountName='+username+'))',
                search_scope=SUBTREE, attributes=[ALL_ATTRIBUTES,
                                                  ALL_OPERATIONAL_ATTRIBUTES])
    for entry in conn.response:
        if 'attributes' in entry:            
            if 'userWorkstations' in entry['attributes']:
                assigned_computer = entry['attributes']['userWorkstations']
                mylist = assigned_computer.split(',')
                assigned_computer = mylist[0]
                assigned_computer=assigned_computer.lower()
            else:
                assigned_computer = ''
    return assigned_computer


def bind():
    s = Server('windows-server', port=636, use_ssl=True, get_info=ALL)
    admin_username = 'Administrator@naanal.local'
    admin_password = 'p@ssw0rd1'
    conn = Connection(s, user=admin_username, password=admin_password, auto_bind=True)    
    return conn

def get_instance_id(instance_name):
    instance_id=''
    nova=get_nova_keystone_auth()
    server = nova.servers.find(name=instance_name)
    instance_id=str(server.id)
    return(instance_id)


def get_instance_ipaddress(instance_name):
    fixed=''
    nova = get_nova_keystone_auth()
    server = nova.servers.find(name=instance_name)
    address = server.addresses
    address = address['net04']
    fixed = address[0]
    fixed = fixed['addr']
    fixed=str(fixed)
    return(fixed)


def get_instance_floatingip(instance_name):
    floating_ip=''
    nova = get_nova_keystone_auth()
    server = nova.servers.find(name=instance_name)
    address = server.addresses
    address = address['net04']
    if len(address)==2:
        floating_ip = address[1]
        floating_ip = floating_ip['addr']
        floating_ip = str(floating_ip)
    else:
        floating_ip=''
    print floating_ip

    return(floating_ip)


def instance_status(instance_name):
    status=''
    nova = get_nova_keystone_auth()
    server = nova.servers.find(name=instance_name)
    status = str(server.status)
    return(status)




def get_nova_keystone_auth():
    auth_url = 'http://controller:35357/v3'
    username1 = 'admin'
    user_domain_name = 'Default'
    project_name = 'admin'
    project_domain_name = 'Default'
    password = 'admin'
    project_id="359d91ddd8744d27be37e79401d7d9fd"
    auth =v3.Password(auth_url=auth_url,username=username1,password=password,project_id=project_id,
    user_domain_name=user_domain_name)
    sess = session.Session(auth=auth)
    keystone = ksclient.Client(session=sess)
    keystone.projects.list()
    from novaclient import client
    nova = client.Client(2, session=keystone.session)
    return(nova)

def vnc_console(instance_name):   
    nova=get_nova_keystone_auth()
    server = nova.servers.find(name=instance_name)
    console=server.get_vnc_console('novnc')
    console1=console['console']
    console=console1['url']
    return(console)
 
def download_RDP(username,instance_id,instance_name):
    fixed =''
    floating_ip=get_instance_floatingip(instance_name)
    file_name="login/static/RDP/"+username+".rdp"
    Rdpname=username+".rdp"
    content="auto connect:i:1\nfull address:s:%s\nusername:s:%s\n" % (floating_ip, username)     
    fo = open(file_name, "wb")
    fo.write(content);    
    return(Rdpname) 







        
