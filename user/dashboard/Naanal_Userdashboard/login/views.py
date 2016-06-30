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
            instance_id=get_instance_id(instance_name)
            fixed=get_instance_ipaddress(instance_id)
            status=instance_status(instance_id)
            floating_ip=get_instance_floatingip(instance_id)           
            print "instance_id:::::"+instance_id,"\n fixed::::"+fixed,"\n status"+status,"\n instance_name"+instance_name
            print status           
            if status =="active":
               console=vnc_console(instance_name)
               print console    
            rdp_file=download_RDP(username,instance_id)
            print "\n rdp_file:::"+rdp_file
            return render_to_response('index.html',{'password':password, 'username': username,'instancename':instance_name,'instanceid':instance_id,'status':status,'console':console,'fixedip':fixed,'floatingip':floating_ip,'RDP_file':rdp_file})
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
           instance_name=get_assigned_computer(username)
           instance_id=get_instance_id(instance_name)
           fixed=get_instance_ipaddress(instance_id)
           floating_ip = get_instance_floatingip(instance_id)
           status=instance_status(instance_id)
           rdp_file = download_RDP(username, instance_id)
           if status =="active":
              console=vnc_console(instance_name)
           print console          
           return render_to_response('index.html',{'password':password, 'username': username,'instancename':instance_name,'instanceid':instance_id,'status':status,'console':console,'fixedip':fixed,'floatingip':floating_ip,'RDP_file':rdp_file})
    
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
           print username
           print password
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
           print username     
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
           rdp_file=download_RDP(username,instance_id)          
           nova=get_nova_keystone_auth()
           server = nova.servers.find(name=instance_name)
           print "\n instance_name:::"+instance_name,"\n instance_id::::"+instance_id
           if operation == 'stop':
               print "------------instance stop-------------------"
               server.stop()               
               status=instance_status(instance_id)
               timeout = time.time() + 4*5   # 5 minutes from now
               while status !='stopped':
                     status=instance_status(instance_id)
                     test = 0
                     if test == 5 or time.time() > timeout:
                        break
                     test = test - 1
               
           elif operation == 'start':
               print "------------instance start-------------------"
               server.start()
               status=instance_status(instance_id)
               timeout = time.time() + 4*5   # 5 minutes from now
               while status !='active':
                     status=instance_status(instance_id)
                     test = 0
                     if test == 5 or time.time() > timeout:
                        break
                     test = test - 1
               console=vnc_console(instance_name)
           elif operation == 'reboot':
               print "------------instance reboot-------------------"
               server.reboot(reboot_type='SOFT')
               status=instance_status(instance_id)
               timeout = time.time() + 4*5   # 5 minutes from now
               while status !='active':
                     status=instance_status(instance_id)
                     test = 0
                     if test == 5 or time.time() > timeout:
                        break
                     test = test - 1
               console=server.get_vnc_console('novnc')
               console1=console['console']
               console=console1['url']
               console=str(console)
           elif operation == 'rdp':               
               print rdp_file
           fixed=get_instance_ipaddress(instance_id)
           floating_ip = get_instance_floatingip(instance_id)
           time.sleep(5)
           status=instance_status(instance_id)
           print "fixed_ip:::"+fixed,"\n floating_ip::::"+floating_ip,"\n status of instance:::"+status,"\n console_url:::"+console

           return render_to_response('index.html',{'password':password, 'username': username,'instancename':instance_name,'instanceid':instance_id,'status':status,'console':console,'RDP_file':rdp_file,'fixedip':fixed,'floatingip':floating_ip})
    return render_to_response('login.html')



@csrf_exempt
def snapshot(request):
    username = password = ''
    if request.POST:
        if request.session.has_key('username'):
           username1 = request.session['username']    
           username = request.POST.get('username')  
           instance_id = request.POST.get('instance_id')
           instance_name=request.POST.get('instance_name')
           print "-----------inside the snapshot method-----------"
           console = fixed = ''
           instance_name = get_assigned_computer(username)
           instance_id = get_instance_id(instance_name)
           fixed = get_instance_ipaddress(instance_id)
           status = instance_status(instance_id)
           floating_ip = get_instance_floatingip(instance_id)
           rdp_file = download_RDP(username, instance_id)
           nova=get_nova_keystone_auth()
           server = nova.servers.find(name=instance_name)
           network=server.networks
           i=0
           for k in network['net04']:
              i=i+1
              if i==1:
		      network_name= 'net04'
	      else :
		      network_name= 'net04_ext'

           flavor_name=get_flavor_name(instance_id)
           image_name = username
           print "username:::" + username, "\n instance_id:::" + instance_id, "\n instance_name::::" + instance_name,'\n network_name:::'+network_name,'\n flavor_name::'+flavor_name,'\n image_name::'+image_name

           db = MySQLdb.connect(host="controller", port=3306, user="ha", passwd="ha_pass", db="glance")
           cursor = db.cursor()
           cursor.execute("select id from  images where status != 'deleted'and name ='%s' and created_at < NOW();" % (image_name))
           results = cursor.fetchall()
           for row in results:
               oldimage_id = row[0]
               print "----------inside snapshot old image_id-----------------------"
               print oldimage_id
           try:
                oldimage_id
           except NameError:
                oldimage_id= ''

           if oldimage_id !='':
              print "---------------if already having snapshot image--------------------"
              nova.servers.create_image(server, image_name, metadata=None)  # here testing is name of the snapshot
              time.sleep(10)
              print "snapshot was created"
              db = MySQLdb.connect(host="controller",port=3306,user="ha",passwd="ha_pass",db="glance")
              cursor = db.cursor()
              cursor.execute("select id from  images where status !='deleted' and id != '%s' and name='%s';" %(oldimage_id,image_name))
              results=cursor.fetchall()
              for row in results:
                  image_id=row[0]
                  print "/n new_image_id ::;"+image_id
              cursor.execute("select status from  images where id='%s';" % (image_id))
              results = cursor.fetchall()
              for row in results:
                  snapshot_status= row[0]
                  print "***********************snapshot image status*****************"
                  print snapshot_status
           else:
               print "--------------1st time having snapshot--------------------------------"
               nova.servers.create_image(server, image_name, metadata=None)  # here testing is name of the snapshot
               time.sleep(10)
               print "snapshot was created"
               db = MySQLdb.connect(host="controller", port=3306, user="ha", passwd="ha_pass", db="glance")
               cursor = db.cursor()
               cursor.execute("select id from  images where status !='deleted' and  name='%s';" % (image_name))
               results = cursor.fetchall()
               for row in results:
                   image_id = row[0]
                   print "/n new_image_id ::;" + image_id
               cursor.execute("select status from  images where id='%s';" % (image_id))
               results = cursor.fetchall()
               for row in results:
                   snapshot_status = row[0]
                   print "***********************snapshot image status*****************"
                   print snapshot_status
                   print snapshot_status == 'active'

           while snapshot_status !='active':
                 print "************************inside the while statement*******************************"
                 print snapshot_status
                 db = MySQLdb.connect(host="controller",port=3306,user="ha",passwd="ha_pass",db="glance")
                 cursor = db.cursor()
                 cursor.execute("select status from  images where id='%s';" % (image_id))
                 results = cursor.fetchall()
                 for row in results:
                     snapshot_status= row[0]
                     print snapshot_status
                 if snapshot_status=='killed':
                     break
                 db.commit()
                 db.close()

           if snapshot_status=='active':
              print "***********inside the if active statment*****************"
              error='snapshot created successfully.....!!!!!'
              if oldimage_id != '':
                  print "---------delete if old image is found-----------"
                  nova = get_nova_keystone_auth()
                  print nova.images.delete(oldimage_id)

              if status =="active":
                 console=vnc_console(instance_name)
                 print console

              return render_to_response('index.html',
                                        {'password': password, 'username': username, 'instancename': instance_name,
                                         'instanceid': instance_id, 'status': status, 'console': console,
                                         'fixedip': fixed, 'floatingip': floating_ip, 'RDP_file': rdp_file,'error':error})


           elif snapshot_status=='killed':
                error= "Error while creating snapshot......!!!"
                print error

           return render_to_response('index.html',
                                     {'password': password, 'username': username, 'instancename': instance_name,
                                      'instanceid': instance_id, 'status': status, 'console': console, 'fixedip': fixed,
                                      'floatingip': floating_ip, 'RDP_file': rdp_file,'error':error})


@csrf_exempt
def restore_from_snapshot(request):
    username = password = task_state = vm_state = console=''
    if request.POST:
        if request.session.has_key('username'):
            username1 = request.session['username']
            username = request.POST.get('username')
            instance_id = request.POST.get('instance_id')
            instance_name = request.POST.get('instance_name')
            nova = get_nova_keystone_auth()
            server = nova.servers.find(name=instance_name)
            network = server.networks
            print "-----------------------------inside the restore from snapshot method---------------------"
            i = 0
            for k in network['net04']:
                i = i + 1
                if i == 1:
                    network_name = 'net04'
                else:
                    network_name = 'net04_ext'

            flavor_name = get_flavor_name(instance_id)
            image_name = username
            print "\n username:::"+username,"\n old_instance_id::::"+instance_id,"\n flavor_name:::"+flavor_name,'\n  image_name:::'+image_name
            instance_name = get_assigned_computer(username)
            instance_id = get_instance_id(instance_name)
            fixed = get_instance_ipaddress(instance_id)
            status = instance_status(instance_id)
            floating_ip = get_instance_floatingip(instance_id)
            rdp_file = download_RDP(username, instance_id)
            db = MySQLdb.connect(host="controller", port=3306, user="ha", passwd="ha_pass", db="glance")
            cursor = db.cursor()
            cursor.execute(
                "select id from  images where status != 'deleted'and name ='%s' and created_at < NOW();" % (image_name))
            results = cursor.fetchall()
            for row in results:
                oldimage_id = row[0]
                print "----------inside snapshot old image_id-----------------------"
                print oldimage_id
            try:
                oldimage_id
            except NameError:
                oldimage_id = ''

            if oldimage_id!='':
                console = fixed = ''
                nova = get_nova_keystone_auth()
                image = nova.images.find(name=image_name)
                flavor = nova.flavors.find(name=flavor_name)
                network = nova.networks.find(label=network_name)
                server = nova.servers.create(name=instance_name, image=image.id, flavor=flavor.id,
                                         nics=[{'net-id': network.id}])
                print "-------------------------new instances created from the snapshot image successfully...!!!!!!!------------"
                new_instance_id = str(server.id)
                time.sleep(10)
                print "/n new_instance_name:::::" + image_name,'/n new_instance_id::::'+new_instance_id,'old_instance_id:::'+instance_id

                db = MySQLdb.connect(host="controller", port=3306, user="ha", passwd="ha_pass", db="nova")
                cursor = db.cursor()
                cursor.execute("select task_state,vm_state from instances where uuid='%s';" % (new_instance_id))
                results = cursor.fetchall()
                for row in results:
                    task_state = row[0]
                    vm_state = row[1]
                task_state = str(task_state)
                vm_state = str(vm_state)
                print "****************************************"
                print task_state, vm_state
                print "****************************************"
                print"***************************before while statement task_state and vm_state*********************************"

                while vm_state != 'active':
                    db = MySQLdb.connect(host="controller", port=3306, user="ha", passwd="ha_pass", db="nova")
                    cursor = db.cursor()
                    cursor.execute("select task_state,vm_state from instances where uuid='%s';" % (new_instance_id))
                    results = cursor.fetchall()
                    for row in results:
                        task_state = row[0]
                        vm_state = row[1]
                    if vm_state == "error":
                        break
                    print"***************************INSIDE while statement task_state and vm_state*********************************"
                    print vm_state

                if vm_state == 'active':
                    print "***************inside the update statement part****************************"
                    delete_old_instance = delete_instance(instance_id)  # DELETE THE OLD INSTANCE
                    print "-------old instance deleted-------------------"
                    print delete_old_instance
                    instance_name = get_assigned_computer(username)
                    instance_id = get_instance_id(instance_name)
                    fixed = get_instance_ipaddress(instance_id)
                    status = instance_status(instance_id)
                    floating_ip = get_instance_floatingip(instance_id)
                    rdp_file = download_RDP(username, instance_id)
                    print '------------updated new instance successfully--------------------------'
                    print '\n instance_name:::'+instance_name,'\n instance_id:::'+instance_id,'\n fixed:::'+fixed,'\n floating_ip:::'+floating_ip
                    error='restore from snapshot successfully....!!!!! '
                    if status == "active":
                        console = vnc_console(instance_name)
                        print console
                    return render_to_response('index.html',
                                              {'password': password, 'username': username, 'instancename': instance_name,
                                               'instanceid': instance_id, 'status': status, 'console': console,
                                               'fixedip': fixed, 'floatingip': floating_ip, 'RDP_file': rdp_file,
                                               'error': error})


                elif vm_state == 'error':
                    print"---------------------Restore from the snapshot having error------------------------"
                    error= "Restore for snapshot is error...........!!!!!!"
                    return render_to_response('index.html',
                                              {'password': password, 'username': username, 'instancename': instance_name,
                                               'instanceid': instance_id, 'status': status, 'console': console,
                                               'fixedip': fixed, 'floatingip': floating_ip, 'RDP_file': rdp_file,
                                               'error': error})
            else:
                error = "Do u have no previous snapshot images to restore....!!!!!!"
                status = instance_status(instance_id)
                if status == "active":
                    console = vnc_console(instance_name)
                    print console
                return render_to_response('index.html',
                                          {'password': password, 'username': username, 'instancename': instance_name,
                                           'instanceid': instance_id, 'status': status, 'console': console,
                                           'fixedip': fixed, 'floatingip': floating_ip, 'RDP_file': rdp_file,
                                           'error': error})


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
                print "-------Assigned computer-----"
                mylist = assigned_computer.split(',')
                assigned_computer = mylist[0]
                print assigned_computer
            else:
                assigned_computer = ''
    return assigned_computer

def bind():
    s = Server('172.30.1.197', port=636, use_ssl=True, get_info=ALL)
    admin_username = 'Administrator@naanal.local'
    admin_password = 'p@ssw0rd1'
    conn = Connection(s, user=admin_username, password=admin_password, auto_bind=True)    
    return conn

def get_instance_id(instance_name):
    instance_id=''
    db = MySQLdb.connect(host="controller",port=3306,user="ha",passwd="ha_pass",db="nova")
    cursor = db.cursor()
    cursor.execute("select uuid from instances where deleted=0 and display_name='%s'" % (instance_name))
    results = cursor.fetchall()
    for row in results:
        instance_id = row[0]
    db.commit()
    db.close()
    return(instance_id)


def get_instance_ipaddress(instance_id):
    fixed=''   
    db = MySQLdb.connect(host="controller",port=3306,user="ha",passwd="ha_pass",db="nova")
    cursor = db.cursor()
    sql ="select ip_address from neutron.ipallocations where port_id = (select id  from neutron.ports where device_id ='%s' );" % (instance_id)           
    cursor.execute(sql)  
    results = cursor.fetchall()
    for row in results:     
        fixed=row[0]
    db.commit()
    db.close()
    return(fixed)


def get_instance_floatingip(instance_id):
    floating_ip=''
    db = MySQLdb.connect(host="controller",port=3306,user="ha",passwd="ha_pass",db="nova")
    cursor = db.cursor()
    sql ="select floating_ip_address from neutron.floatingips where fixed_port_id = (select id  from neutron.ports where device_id ='%s' );" % (instance_id)           
    cursor.execute(sql)  
    results = cursor.fetchall()
    for row in results:     
        floating_ip=row[0]
    db.commit()
    db.close()
    return(floating_ip)


def instance_status(instance_id):
    status=''        
    db = MySQLdb.connect(host="controller",port=3306,user="ha",passwd="ha_pass",db="nova")
    cursor = db.cursor()
    cursor.execute("select vm_state from instances where deleted=0 and  uuid='%s'" % (instance_id))
    results = cursor.fetchall()            
    for row in results:                       
        status =row[0]                             
    db.commit()
    db.close()
    return(status)


def get_instance_name(instance_id):    
    print"inside the instance_name method"
    print instance_id
    instance_name=''        
    db = MySQLdb.connect(host="controller",port=3306,user="ha",passwd="ha_pass",db="nova")
    cursor = db.cursor()
    cursor.execute("select display_name from instances where deleted=0 and uuid='%s'" % (instance_id))
    results = cursor.fetchall()            
    for row in results:                       
        instance_name = row[0]                             
    db.commit()
    db.close()    
    return(instance_name)
def get_project_id(project_name):
    db = MySQLdb.connect(host="controller",port=3306,user="ha",passwd="ha_pass",db="keystone")
    cursor = db.cursor()
    cursor.execute("select id from project where name='%s'" % (project_name))
    results = cursor.fetchall()            
    for row in results:                       
        project_id = row[0]                             
    db.commit()
    db.close()
    print "inside the get_project_id:"    
    print project_id
    return(project_id)

def get_nova_keystone_auth():
    auth_url = 'http://controller:35357/v3'
    username1 = 'admin'
    user_domain_name = 'Default'
    project_name = 'admin'
    project_domain_name = 'Default'
    password = 'admin'
    project_id=get_project_id(project_name)
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
 
def download_RDP(username,instance_id):
    print "inside the Download RDP"
    fixed =''
    floating_ip=get_instance_floatingip(instance_id)    
    file_name="login/static/RDP/"+username+".rdp"
    Rdpname=username+".rdp"
    content="auto connect:i:1\nfull address:s:%s\nusername:s:%s\n" % (floating_ip, username)     
    fo = open(file_name, "wb")
    fo.write(content);    
    return(Rdpname) 



def get_flavor_name(instance_id):    
    print"inside the instance_name method"
    db = MySQLdb.connect(host="controller",port=3306,user="ha",passwd="ha_pass",db="nova")
    cursor = db.cursor()                  
    cursor.execute("select instance_type_id from instances where uuid='%s'" % (instance_id))  
    results = cursor.fetchall()
    for row in results:     
        instance_type_id=row[0]    
    db.close()
    db = MySQLdb.connect(host="controller",port=3306,user="ha",passwd="ha_pass",db="nova")
    cursor = db.cursor()                  
    cursor.execute(" select name from instance_types where id ='%s'" % (instance_type_id))  
    results = cursor.fetchall()           
    for row in results:     
        flavor_name=row[0]   
    return(flavor_name)




        
def delete_instance(instance_id):    
    print"inside the delete_instance method"
    print instance_id 
    nova=get_nova_keystone_auth()
    server = nova.servers.delete(instance_id)
    time.sleep(10)
    db = MySQLdb.connect(host="controller", port=3306, user="ha", passwd="ha_pass", db="nova")
    cursor = db.cursor()
    cursor.execute("select deleted from instances where uuid='%s'" % (instance_id))
    results = cursor.fetchall()
    for row in results:
        deleted = row[0]
    db.close()

    while deleted !=0:
        db = MySQLdb.connect(host="controller", port=3306, user="ha", passwd="ha_pass", db="nova")
        cursor = db.cursor()
        cursor.execute("select deleted from instances where uuid='%s'" % (instance_id))
        results = cursor.fetchall()
        for row in results:
            deleted = row[0]
    if deleted==0:
        status='delete the previous instance is success...'
    return(status)
