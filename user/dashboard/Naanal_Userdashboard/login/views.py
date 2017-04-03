from django.shortcuts import render_to_response
# from keystoneauth1.identity import v2
# from keystoneauth1 import session
# from keystoneclient import client as ksclient
import time
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
import os
import ldap3
from ldap3 import Server, Connection, SUBTREE, ALL, ALL_ATTRIBUTES, \
    ALL_OPERATIONAL_ATTRIBUTES, MODIFY_REPLACE, MODIFY_ADD
from django.conf import settings
import logging
userlog = logging.getLogger('userlog')
from django.shortcuts import redirect

from keystoneauth1 import loading
from keystoneauth1 import session
from keystoneclient.v3 import client as keystone_client
from novaclient import client as nova_client
from cinderclient import client as cinder_client
from neutronclient.v2_0 import client as neutron_client
auth_url="http://192.168.30.200:35357/v2.0"

@csrf_exempt
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginpage(request):
    state = "Please log in below..."
    username = password = instance_id = instance_name = status = console = fixed = conn = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            request.session['username'] = username
            user_name=username+'@'+settings.DOMAIN_NAME
            password = password
            # print(user_name)
            # print(password)
            try:
                s = Server(settings.LDAP_SERVER[0], port=settings.LDAP_SERVER_PORT, use_ssl=settings.LDAP_SSL, get_info=ALL)
                conn = Connection(s, user=user_name, password=password, auto_bind=True)
                #conn = Connection(s, user=user_name, password=password)
                userlog.info("%s user login ", username)
                instance_name = get_assigned_computer(username)
                if instance_name == '':
                    state = "No allocated instances..! Please contact your Administrator..!"
                    userlog.info(state)
                    return render_to_response('login.html', {'state': state})
                status = instance_status(instance_name)
                if status =="vm not found....!":
                    state = "Instance not found..! or Problem occuerd to find the instace from the server..!"
                    userlog.info(state)
                    return render_to_response('login.html', {'state': state})
                elif(status=="Server not Found"):
                    return render_to_response('Error.html')
                instance_id = get_instance_id(instance_name)
                #fixed = get_instance_ipaddress(instance_name)
                floating_ip = get_instance_floatingip(instance_name)
                console = vnc_console(instance_name)
                if status == "ACTIVE":

                    button_color = "btn btn-danger btn-xs"
                else:
                    button_color = "btn btn-success btn-xs "
                rdp_file = download_RDP(username, instance_id, instance_name)
                return render_to_response('index.html',
                                          {'password': password, 'username': username, 'instancename': instance_name,
                                           'instanceid': instance_id, 'status': status, 'console': console,
                                           'fixedip': fixed, 'floatingip': floating_ip, 'RDP_file': rdp_file,
                                           'button_color': button_color})
            except ldap3.core.exceptions.LDAPBindError:
                state = 'Wrong username or password'
                print(state)
            except ldap3.core.exceptions.LDAPSocketOpenError:
                try:
                    s = Server(settings.LDAP_SERVER[1], port=settings.LDAP_SERVER_PORT, use_ssl=settings.LDAP_SSL, get_info=ALL)
                    conn = Connection(s, user=user_name, password=password, auto_bind=True)
                    userlog.info("%s user login ", username)
                    instance_name = get_assigned_computer(username)
                    if instance_name == '':
                        state = "No allocated instances..! Please contact your Administrator..!"
                        userlog.info(state)
                        return render_to_response('login.html', {'state': state})
                    status = instance_status(instance_name)
                    if status =="vm not found....!":
                        state = "Instance not found..! or Problem occuerd to find the instace from the server..!"
                        userlog.info(state)
                        return render_to_response('login.html', {'state': state})
                    elif(status=="Server not Found"):
                        return render_to_response('Error.html')
                    instance_id = get_instance_id(instance_name)
                    #fixed = get_instance_ipaddress(instance_name)
                    floating_ip = get_instance_floatingip(instance_name)
                    console = vnc_console(instance_name)
                    if status == "ACTIVE":
                        button_color = "btn btn-danger btn-xs"
                    else:
                        button_color = "btn btn-success btn-xs "
                    rdp_file = download_RDP(username, instance_id, instance_name)
                    return render_to_response('index.html',
                                              {'password': password, 'username': username, 'instancename': instance_name,
                                               'instanceid': instance_id, 'status': status, 'console': console,
                                               'fixedip': fixed, 'floatingip': floating_ip, 'RDP_file': rdp_file,
                                               'button_color': button_color})
                except ldap3.core.exceptions.LDAPBindError:
                    state = 'Wrong username or password'
                except ldap3.core.exceptions.LDAPSocketOpenError:
                    state = 'AD server not available'
        else:
            state = "username and password must be NOt Empty...!!!!"
            return render_to_response('login.html', {'state': state})
    return render_to_response('login.html', {'state': state})


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if request.GET:
        username = request.GET.get('username')
        state = "Please log in below..."
        try:
            del request.session['username']
        except:
            return render_to_response('login.html', {'state': state})
        userlog.info("%s user logout", username)
    return redirect('login.views.loginpage')


@csrf_exempt
def index_page(request):
    username = password = instance_id = instance_name = status = console =fixed= ''
    if request.GET:
        username = request.GET.get('username')       

        if request.session.has_key('username'):
            username1 = request.session['username']
            instance_name = get_assigned_computer(username)
            status = instance_status(instance_name)
            if(status=="Server not Found"):
                    return render_to_response('Error.html')
            instance_id = get_instance_id(instance_name)
            #fixed = get_instance_ipaddress(instance_name)
            floating_ip = get_instance_floatingip(instance_name)
            rdp_file = username + ".rdp"
            if status == "ACTIVE":
                console = vnc_console(instance_name)
                button_color = "btn btn-danger btn-xs"
            else:
                button_color = "btn btn-success btn-xs "
            return render_to_response('index.html',
                                      {'password': password, 'username': username, 'instancename': instance_name,
                                       'instanceid': instance_id, 'status': status, 'console': console,
                                       'fixedip': fixed, 'floatingip': floating_ip, 'RDP_file': rdp_file,
                                       'button_color': button_color})
    return redirect('login.views.loginpage')



@csrf_exempt
def change_password(request):
    username = password = console = ''
    if request.GET:
        if request.session.has_key('username'):
            username1 = request.session['username']
            username = request.GET.get('username')
            password = request.GET.get('password')
            return render_to_response('changepassword.html', {'password': password, 'username': username})
        else:
            return redirect('login.views.loginpage')

    if request.POST:
        if request.session.has_key('username'):
            username1 = request.session['username']
            username = request.POST.get('username')
            password = request.POST.get('currentpassword')
            new_password = request.POST.get('newpassword')
            new_password1 = str(new_password)

            user_name=username+'@'+settings.DOMAIN_NAME
            password = password
            try:
                s = Server(settings.LDAP_SERVER[0], port=settings.LDAP_SERVER_PORT, use_ssl=settings.LDAP_SSL, get_info=ALL)
                #conn = Connection(s, user=user_name, password=password, auto_bind=True)
                conn = Connection(s, user=user_name, password=password)
                conn.unbind()
                conn = bind()
                dn = ("cn=%s," + settings.WINDOWS_SERVER_USERPATH + "," + settings.WINDOWS_SERVER_DOMAINPATH) % username
                unicode_pass = unicode('"' + new_password1 + '"', 'iso-8859-1')
                encoded_pass = unicode_pass.encode('utf-16-le')
                conn.modify(dn, {'unicodePwd': [(MODIFY_REPLACE, [encoded_pass])]})
                conn.modify(dn, {'unicodePwd': [(MODIFY_REPLACE, [encoded_pass])]})
                status = conn.result['description']
                userlog.info("%s change password ", username)
                # status='success'
                if status == 'success':
                    return redirect('login.views.loginpage')
                else:
                    return render_to_response('changepassword.html',
                                              {'password': password, 'username': username, 'status': status})

            except ldap3.core.exceptions.LDAPBindError:
                status = 'worng current password'
                userlog.error("%s change password %s", username, status)
                return render_to_response('changepassword.html',
                                          {'password': password, 'username': username, 'status': status})
            except ldap3.core.exceptions.LDAPSocketOpenError:
                try:
                    s = Server(settings.LDAP_SERVER[1], port=settings.LDAP_SERVER_PORT, use_ssl=settings.LDAP_SSL, get_info=ALL)
                    #conn = Connection(s, user=user_name, password=password, auto_bind=True)
                    conn = Connection(s, user=user_name, password=password)
                    conn.unbind()
                    conn = bind()
                    dn = ("cn=%s,"+settings.WINDOWS_SERVER_USERPATH+","+settings.WINDOWS_SERVER_DOMAINPATH) % username
                    unicode_pass = unicode('"' + new_password1 + '"', 'iso-8859-1')
                    encoded_pass = unicode_pass.encode('utf-16-le')
                    conn.modify(dn, {'unicodePwd': [(MODIFY_REPLACE, [encoded_pass])]})
                    conn.modify(dn, {'unicodePwd': [(MODIFY_REPLACE, [encoded_pass])]})
                    status = conn.result['description']
                    userlog.info("%s change password ", username)
                    # status='success'
                    if status=='success':
                        return redirect('login.views.loginpage')
                    else:
                        return render_to_response('changepassword.html',
                                              {'password': password, 'username': username, 'status': status})
                except ldap3.core.exceptions.LDAPBindError:
                    status = 'worng current password'
                    userlog.error("%s change password %s", username, status)
                    return render_to_response('changepassword.html',
                                              {'password': password, 'username': username, 'status': status})
                except ldap3.core.exceptions.LDAPSocketOpenError:
                    status = 'windows active directory not available'
                    userlog.error("%s change password %s", username, status)
    return redirect('login.views.loginpage')



def help(request):
    username = password = ''
    if request.GET:
        if request.session.has_key('username'):
            username1 = request.session['username']
            username = request.GET.get('username')
            return render_to_response('help.html', {'username': username})
    return redirect('login.views.loginpage')

def login_help(request):
    username = password = ''
    if request.GET:
        if request.session.has_key('username'):
            username1 = request.session['username']
            username = request.GET.get('username')
            return render_to_response('login_help.html', {'username': username})
    return redirect('login.views.loginpage')


def browservm_help(request):
    username = password = ''
    if request.GET:
        if request.session.has_key('username'):
            username1 = request.session['username']
            username = request.GET.get('username')
            return render_to_response('vmbrowser.html', {'username': username})
    return redirect('login.views.loginpage')

def RDP_help(request):
    username = password = ''
    if request.GET:
        if request.session.has_key('username'):
            username1 = request.session['username']
            username = request.GET.get('username')
            return render_to_response('RDP_help.html', {'username': username})
    return redirect('login.views.loginpage')
    return render_to_response('login.html')

def changepswd_help(request):
    username = password = ''
    if request.GET:
        if request.session.has_key('username'):
            username1 = request.session['username']
            username = request.GET.get('username')
            return render_to_response('changepassword_help.html', {'username': username})
    return redirect('login.views.loginpage')


@csrf_exempt
def instance_stop(request):
    instance_id = console = username = password = fixed=''
    if request.POST:
        if request.session.has_key('username'):
            username1 = request.session['username']
            instance_id = request.POST.get('instance_id')
            username = request.POST.get('user_name')
            instance_name = request.POST.get('instance_name')
            operation = request.POST.get('operation')
            username = str(username)
            rdp_file = username + ".rdp"
            nova = get_nova_keystone_auth()
            if(nova=="Server not Found"):
               return render_to_response('Error.html')
            server = nova.servers.find(name=instance_name)
            status = str(server.status)
            if status == 'ACTIVE' and operation == 'start':
                server.stop()
                userlog.info("%s stop instance", username)
                status = instance_status(instance_name)
                timeout = time.time() + 4 * 5  # 5 minutes from now
                while status != 'SHUTOFF':
                    status = instance_status(instance_name)
                    test = 0
                    if test == 5 or time.time() > timeout:
                        break
                    test = test - 1
                button_color = "btn btn-success btn-xs "
                console = vnc_console(instance_name)
            elif status == 'SHUTOFF' and operation == 'start':
                server.start()
                userlog.info("%s statrt instance %s", username, instance_name)
                status = instance_status(instance_name)
                timeout = time.time() + 4 * 5  # 5 minutes from now
                while status != 'ACTIVE':
                    status = instance_status(instance_name)
                    test = 0
                    if test == 5 or time.time() > timeout:
                        break
                    test = test - 1
                button_color = "btn btn-danger btn-xs"
                console = vnc_console(instance_name)
            elif operation == 'reboot' and status == 'ACTIVE':
                server.reboot()
                userlog.info("%s reboot instance %s", username, instance_name)
                status = instance_status(instance_name)
                timeout = time.time() + 4 * 5  # 5 minutes from now
                while status != 'ACTIVE':
                    status = instance_status(instance_name)
                    test = 0
                    if test == 5 or time.time() > timeout:
                        break
                    test = test - 1
                console = server.get_vnc_console('novnc')
                console1 = console['console']
                console = console1['url']
                console = str(console)
                button_color = "btn btn-danger btn-xs"
            else:
                Error = "Unable to perform your operation..! Try after sometime..!"
                userlog.error(Error)
                if status == "ACTIVE":
                    console = vnc_console(instance_name)
                    button_color = "btn btn-danger btn-xs"
                else:
                    button_color = "btn btn-success btn-xs "
                    console = vnc_console(instance_name)
            #fixed = get_instance_ipaddress(instance_name)
            floating_ip = get_instance_floatingip(instance_name)
            time.sleep(5)
            status = instance_status(instance_name)
            return render_to_response('index.html',
                                      {'password': password, 'username': username, 'instancename': instance_name,
                                       'instanceid': instance_id, 'status': status, 'console': console,
                                       'RDP_file': rdp_file, 'fixedip': fixed, 'floatingip': floating_ip,
                                       'button_color': button_color})
    return redirect('login.views.loginpage')


def get_assigned_computer(username):
    assigned_computer = ''
    conn = bind()
    conn.search(search_base=settings.WINDOWS_SERVER_DOMAINPATH,
                search_filter='(&(sAMAccountName=' + username + '))',
                search_scope=SUBTREE, attributes=[ALL_ATTRIBUTES,
                                                  ALL_OPERATIONAL_ATTRIBUTES])
    for entry in conn.response:
        if 'attributes' in entry:
            if 'userWorkstations' in entry['attributes']:
                assigned_computer = entry['attributes']['userWorkstations']
                mylist = assigned_computer.split(',')
                if len(mylist) == 2:
                    assigned_computer = mylist[0]
                    assigned_computer = assigned_computer.lower()
                else:
                    assigned_computer = ''
            else:
                assigned_computer = ''
    # print("-----------Assigned Computers-------------")
    # print(assigned_computer)
    return assigned_computer


def bind():
    try:
        s = Server(settings.LDAP_SERVER[0], port=settings.LDAP_SERVER_PORT, use_ssl=settings.LDAP_SSL, get_info=ALL)
        conn = Connection(s, user=settings.LDAP_ADMIN_USERNAME, password=settings.LDAP_ADMIN_PASSWORD, auto_bind=True)
        return conn
    except:
        s = Server(settings.LDAP_SERVER[1], port=settings.LDAP_SERVER_PORT, use_ssl=settings.LDAP_SSL, get_info=ALL)
        conn = Connection(s, user=settings.LDAP_ADMIN_USERNAME, password=settings.LDAP_ADMIN_PASSWORD, auto_bind=True)
        return conn


def get_instance_id(instance_name):
    instance_id = ''
    nova = get_nova_keystone_auth()
    if(nova=="Server not Found"):
        return (nova)
    server = nova.servers.find(name=instance_name)
    instance_id = str(server.id)
    return (instance_id)


def get_instance_ipaddress(instance_name):
    fixed = ''
    nova = get_nova_keystone_auth()
    if(nova=="Server not Found"):
        return (nova)
    server = nova.servers.find(name=instance_name)
    network = server.networks
    for network_name in network:
        network_name = network_name
    ip = network[network_name]
    fixed = ip[0]
    fixed = str(fixed)
    return (fixed)


def get_instance_floatingip(instance_name):
    floating_ip = ''
    nova = get_nova_keystone_auth()
    if(nova=="Server not Found"):
        return (nova)
    server = nova.servers.find(name=instance_name)
    network = server.networks
    for network_name in network:
        network_name = network_name
    ip = network[network_name]
    if len(ip) == 2:
        floating_ip = ip[1]
        floating_ip = str(floating_ip)
    else:
        floating_ip = ''

    return (floating_ip)


def instance_status(instance_name):
    status = ''
    nova = get_nova_keystone_auth()
    print(nova)
    if(nova=="Server not Found"):
        return (nova)
    try:
        ins_list=nova.servers.list()
        print(ins_list)
        server = nova.servers.find(name=instance_name)
        status =str(server.status)
    except nova_client.exceptions.NotFound:
        status = "vm not found....!"
        print(status)
        userlog.exception(status)
    except Exception:
        userlog.exception("Error:To find the server from the controller...!")
    return (status)


def get_nova_keystone_auth():
    try:
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(auth_url=auth_url,
                                username=settings.OPENSTACK_USERNAME,
                                password=settings.OPENSTACK_PASSWORD,
                                 project_name=settings.OPENSTACK_PROJECT_NAME)
        sess = session.Session(auth=auth)
        nova = nova_client.Client(2, session=sess)
        # cinder = cinder_client.Client(2, session=sess)
        # neutron = neutron_client.Client(session=sess)
        # return  neutron,cinder,nova
        # auth_url = settings.OPENSTACK_HOST
        # auth = v2.Password(auth_url=auth_url, username=settings.OPENSTACK_USERNAME, password=settings.OPENSTACK_PASSWORD, tenant_name=settings.OPENSTACK_PROJECT_NAME)
        # sess = session.Session(auth=auth)
        # keystone = ksclient.Client(session=sess)
        # from novaclient import client
        # nova = client.Client("2.1", session=sess)
        return (nova)
    except Exception as e:
        print(e)
        state="Server not Found"
        return (state)


def vnc_console(instance_name):
    nova = get_nova_keystone_auth()
    if(nova=="Server not Found"):
        return (nova)
    server = nova.servers.find(name=instance_name)
    console = server.get_vnc_console('novnc')
    console1 = console['console']
    console = console1['url']
    return (console)


def download_RDP(username, instance_id, instance_name):
    fixed = ''
    floating_ip = get_instance_floatingip(instance_name)
    Domain_name=settings.DOMAIN
    AD_username=Domain_name+username
    file_name = os.path.join(settings.BASE_DIR, 'login/static/RDP/' + username + ".rdp")
    Rdpname = username + ".rdp"
    content = "auto connect:i:1\nfull address:s:%s\nusername:s:%s\nenablecredsspsupport:i:0\n" % (floating_ip, AD_username)
    fo = open(file_name, "wb")
    fo.write(content);
    return (Rdpname)
