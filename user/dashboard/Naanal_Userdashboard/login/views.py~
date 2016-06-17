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

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginpage(request):
    state = "Please log in below..."
    username = password = instance_id = instance_name = status = console = fixed = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        request.session['username'] = username 
        LDAP_SERVER = 'ldap://windows-server'
        LDAP_USERNAME = '%s@naanal.local' % username
        LDAP_PASSWORD = password
        base_dn = 'DC=naanal,DC=local'
        ldap_filter = 'userPrincipalName=%s@naanal.local' % username
        attrs = ['memberOf']
        try:  
            ldap_client = ldap.initialize(LDAP_SERVER)   
            ldap_client.set_option(ldap.OPT_REFERRALS,0)
            ldap_client.simple_bind_s(LDAP_USERNAME, LDAP_PASSWORD)            
            instance_id=get_instance_id(username)     
            fixed=get_instance_ipaddress(instance_id)            
            status=instance_status(instance_id)              
            db = MySQLdb.connect(host="controller",port=3306,user="root",passwd="password",db="nova")
            cursor = db.cursor()
            cursor.execute("select display_name,vm_state from instances where uuid='%s'" % (instance_id))
            results = cursor.fetchall()            
            for row in results:               
                instance_name = row[0]                                           
            db.commit()
            db.close()            
            print status           
            if status =="active":
               console=vnc_console(instance_name)
               print console    
            rdp_file=download_RDP(username,instance_id) 
            return render_to_response('index.html',{'password':password, 'username': username,'instancename':instance_name,'instanceid':instance_id,'status':status,'console':console,'fixedip':fixed,'RDP_file':rdp_file})
        except ldap.INVALID_CREDENTIALS:
            ldap_client.unbind()
            state= 'Wrong username or password'
        except ldap.SERVER_DOWN:
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
           instance_id=get_instance_id(username)
           status=instance_status(instance_id) 
           fixed=get_instance_ipaddress(instance_id)            
           db = MySQLdb.connect(host="controller",port=3306,user="root",passwd="password",db="nova")
           cursor = db.cursor()
           cursor.execute("select display_name,vm_state from instances where uuid='%s'" % (instance_id))
           results = cursor.fetchall() 
           for row in results:               
               instance_name = row[0]                   
           db.commit()
           db.close()
           if status =="active":
              console=vnc_console(instance_name)
           print console          
           return render_to_response('index.html',{'password':password, 'username': username,'instancename':instance_name,'instanceid':instance_id,'status':status,'console':console,'fixedip':fixed})
    
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
           pswd=type(new_password1)
           print pswd        
           print "change post method"
           LDAP_SERVER = 'ldap://windows-server'
           LDAP_USERNAME = '%s@naanal.local' % username
           LDAP_PASSWORD = password
           base_dn = 'DC=naanal,DC=local'
           ldap_filter = 'userPrincipalName=%s@naanal.local' % username
           attrs = ['memberOf']
           try :
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)  
                ldap_client = ldap.initialize(LDAP_SERVER)   
                ldap_client.set_option(ldap.OPT_REFERRALS,0)
                ldap_client.simple_bind_s(LDAP_USERNAME, LDAP_PASSWORD)
                print 'user current password authentication successfull' 
                ldap_client.unbind()
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
                l = ldap.initialize('ldaps://windows-server')
                l.simple_bind_s('Administrator@naanal.local', 'p@ssw0rd1') 
                dn="cn=%s,ou=Police,dc=naanal,dc=local" % username
                password='p@ssword5'             
                unicode_pass = unicode('\"' + new_password1 + '\"', 'iso-8859-1')             
                password_value = unicode_pass.encode('utf-16-le')
                print (password_value)
                add_pass = [(ldap.MOD_REPLACE, 'unicodePwd', [password_value])]
                l.modify_s(dn, add_pass)
                l.modify_s(dn, add_pass)
                l.unbind_s()
                status='success'
                return render_to_response('changepassword.html',{'password':password, 'username': username, 'status': status})   
           except ldap.INVALID_CREDENTIALS:
                ldap_client.unbind()
                status='worng current password'
                return render_to_response('changepassword.html',{'password':password, 'username': username, 'status': status}) 
                print 'Wrong username or password'
           except ldap.SERVER_DOWN:
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
           instance_id = request.POST.get('instance_id')
           username = request.POST.get('user_name')
           instance_name=request.POST.get('instance_name')
           operation=request.POST.get('operation')
           username=str(username)
           rdp_file=download_RDP(username,instance_id)          
           nova=get_nova_keystone_auth()
           server = nova.servers.find(name=instance_name)           
           print instance_name,instance_id
           if operation == 'stop':
               server.stop()
               time.sleep(20)
           elif operation == 'start':
               server.start()
               time.sleep(20)
               console=vnc_console(instance_name)
           elif operation == 'reboot':
               server.reboot(reboot_type='SOFT')
               time.sleep(20)
               console=server.get_vnc_console('novnc')
               console1=console['console']
               console=console1['url']
               console=str(console)
           elif operation == 'rdp':               
               print rdp_file       
           fixed=get_instance_ipaddress(instance_id)
           status=instance_status(instance_id)            
           db = MySQLdb.connect(host="controller",port=3306,user="root",passwd="password",db="nova")
           cursor = db.cursor()
           cursor.execute("select display_name,vm_state from instances where uuid='%s'" % (instance_id))
           results = cursor.fetchall()
           instance=status= instance_id
           for row in results:
               instance = row[0]
               status=row[1]
           db.commit()
           db.close()
           return render_to_response('index.html',{'password':password, 'username': username,'instancename':instance_name,'instanceid':instance_id,'status':status,'console':console,'RDP_file':rdp_file,'fixedip':fixed})
    return render_to_response('login.html')

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
    fixed=get_instance_ipaddress(instance_id)     
    file_name="login/static/RDP/"+username+".rdp"
    Rdpname=username+".rdp"
    content="auto connect:i:1\nfull address:s:%s\nusername:s:%s\n" % (fixed, username)     
    fo = open(file_name, "wb")
    fo.write(content);    
    return(Rdpname) 

@csrf_exempt
def snapshot(request):
    username = password = ''
    if request.POST:
        if request.session.has_key('username'):
           username1 = request.session['username']    
           username = request.POST.get('username')  
           instance_id = request.POST.get('instance_id')
           instance_name=request.POST.get('instance_name')
           snapshot_name=request.POST.get('snapshot_name')     
           print "********snapshot*****************"
           print snapshot_name          
           nova=get_nova_keystone_auth()
           server = nova.servers.find(name=instance_name)
           network=server.networks
           i=0
           for k in network['lan-net']:
              i=i+1
              if i==1:
		      network_name= 'lan-net'
	      else :
		      network_name= 'wan-net'
           db = MySQLdb.connect(host="controller",port=3306,user="root",passwd="password",db="nova")
           cursor = db.cursor()                  
           cursor.execute("select instance_type_id from instances where uuid='%s'" % (instance_id))  
           results = cursor.fetchall()
           for row in results:     
              instance_type_id=row[0]    
           db.close()
           db = MySQLdb.connect(host="controller",port=3306,user="root",passwd="password",db="nova")
           cursor = db.cursor()                  
           cursor.execute(" select name from instance_types where id ='%s'" % (instance_type_id))  
           results = cursor.fetchall()           
           for row in results:     
              flavor_name=row[0]    
              print flavor_name
           image_name=username
           print instance_name,image_name,flavor_name,network_name  
           nova.servers.create_image(server, image_name, metadata=None) # here testing is name of the snapshot
           time.sleep(60)           
           console=fixed=''                       
           nova=get_nova_keystone_auth()
           image = nova.images.find(name=image_name)
           flavor = nova.flavors.find(name=flavor_name)
           network =nova.networks.find(label=network_name) 
           server = nova.servers.create(name = image_name,image = image.id,flavor = flavor.id,nics=[{'net-id': network.id}])
           new_instance_id=str(server.id)
           print new_instance_id            
           db = MySQLdb.connect(host="controller",port=3306,user="root",passwd="password",db="mysql")
           cursor = db.cursor()
           cursor.execute("UPDATE mapping1 SET instances_id='%s' ,instances_name='%s'  where username='%s';" % (new_instance_id,image_name,username))    
           db.commit()
           db.close()
           instance_id=get_instance_id(username)     
           fixed=get_instance_ipaddress(instance_id)            
           status=instance_status(instance_id)                   
           db = MySQLdb.connect(host="controller",port=3306,user="root",passwd="password",db="nova")
           cursor = db.cursor()
           cursor.execute("select display_name,vm_state from instances where uuid='%s'" % (instance_id))
           results = cursor.fetchall() 
           for row in results:               
               instance_name = row[0]                           
           db.commit()
           db.close()
           if status =="active":
              console=vnc_console(instance_name)
              print console              
           return render_to_response('index.html',{'password':password, 'username': username,'instancename':instance_name,'instanceid':instance_id,'status':status,'console':console,'fixedip':fixed})

def get_instance_id(username):
    db = MySQLdb.connect(host="controller",port=3306,user="root",passwd="password",db="mysql")
    cursor = db.cursor()
    cursor.execute("select instances_id from mapping1 where username='%s'" % (username))
    results = cursor.fetchall()
    for row in results:
        instance_id = row[0]
    db.commit()
    db.close()
    return(instance_id)

def get_instance_ipaddress(instance_id):
    fixed=''   
    db = MySQLdb.connect(host="controller",port=3306,user="root",passwd="password",db="nova")
    cursor = db.cursor()
    sql ="select ip_address from neutron.ipallocations where port_id = (select id  from neutron.ports where device_id ='%s' );" % (instance_id)           
    cursor.execute(sql)  
    results = cursor.fetchall()
    for row in results:     
        fixed=row[0]
    db.commit()
    db.close()
    return(fixed)


def instance_status(instance_id):
    status=''        
    db = MySQLdb.connect(host="controller",port=3306,user="root",passwd="password",db="nova")
    cursor = db.cursor()
    cursor.execute("select vm_state from instances where uuid='%s'" % (instance_id))
    results = cursor.fetchall()            
    for row in results:                       
        status =row[0]                             
    db.commit()
    db.close()
    return(status)


def instance_name(instance_id):    
    print"inside the instance_name method"
    print instance_id        
    db = MySQLdb.connect(host="controller",port=3306,user="root",passwd="password",db="nova")
    cursor = db.cursor()
    cursor.execute("select display_name from instances where uuid='%s'" % (instance_id))
    results = cursor.fetchall()            
    for row in results:                       
        instance_name = row[0]                             
    db.commit()
    db.close()    
    return(instance_name)


def get_nova_keystone_auth():
    auth_url = 'http://controller:35357/v3'
    username1 = 'admin'
    user_domain_name = 'Default'
    project_name = 'admin'
    project_domain_name = 'Default'
    password = 'ADMIN'
    auth =v3.Password(auth_url=auth_url,username=username1,password=password,project_id='c9b0922ac3c8400da4aabde2b2bb9daf',
    user_domain_name=user_domain_name)
    sess = session.Session(auth=auth)
    keystone = ksclient.Client(session=sess)
    keystone.projects.list()
    from novaclient import client
    nova = client.Client(2, session=keystone.session)
    return(nova)



