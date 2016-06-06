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

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control



@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginpage(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        LDAP_SERVER = 'ldap://172.30.1.197'
        LDAP_USERNAME = '%s@naanal.local' % username
        LDAP_PASSWORD = password
        base_dn = 'DC=naanal,DC=local'
        ldap_filter = 'userPrincipalName=%s@naanal.local' % username
        attrs = ['memberOf']
        try:  
            ldap_client = ldap.initialize(LDAP_SERVER)   
            ldap_client.set_option(ldap.OPT_REFERRALS,0)
            ldap_client.simple_bind_s(LDAP_USERNAME, LDAP_PASSWORD)
            print 'successfull'
            db = MySQLdb.connect(host="172.30.1.242",port=3306,user="root",passwd="password",db="mysql")
            cursor = db.cursor()
            cursor.execute("select instances_id from mapping1 where username='%s'" % (username))
            results = cursor.fetchall()
            for row in results:
                instance_id = row[0]
                print instance_id
            db.commit()
            db.close()
            db = MySQLdb.connect(host="172.30.1.242",port=3306,user="root",passwd="password",db="nova")
            cursor = db.cursor()
            cursor.execute("select display_name,vm_state from instances where uuid='%s'" % (instance_id))
            results = cursor.fetchall()            
            for row in results:               
                instance_name = row[0]
                status =row[1]                
            db.commit()
            db.close()
            return render_to_response('index.html',{'password':password, 'username': username,'instancename':instance_name,'instanceid':instance_id,'status':status})
        except ldap.INVALID_CREDENTIALS:
            ldap_client.unbind()
            state= 'Wrong username or password'
        except ldap.SERVER_DOWN:
            state= 'AD server not available'        
    return render_to_response('login.html',{'state':state})

@csrf_exempt
def index_page(request):
    username = password = ''
    if request.GET:
        username = request.GET.get('username')        
        db = MySQLdb.connect(host="172.30.1.242",port=3306,user="root",passwd="password",db="mysql")
        cursor = db.cursor()
        cursor.execute("select instances_id from mapping1 where username='%s'" % (username))
        results = cursor.fetchall()
        for row in results:
            instance_id = row[0]
            print instance_id
        db.commit()
        db.close()
        db = MySQLdb.connect(host="172.30.1.242",port=3306,user="root",passwd="password",db="nova")
        cursor = db.cursor()
        cursor.execute("select display_name,vm_state from instances where uuid='%s'" % (instance_id))
        results = cursor.fetchall() 
        for row in results:               
            instance_name = row[0]
            status =row[1]                
        db.commit()
        db.close()
        return render_to_response('index.html',{'password':password, 'username': username,'instancename':instance_name,'instanceid':instance_id,'status':status})
    
    return render_to_response('index.html',{'password':password, 'username': username})


@csrf_exempt
def change_password(request):
    username = password = ''
    if request.GET:
        username = request.GET.get('username')
        password = request.GET.get('password')
        #password = request.POST.get('password')
        print "GET method"
        print username 
        return render_to_response('changepassword.html',{'password':password, 'username': username})       
    
    if request.POST:  
        username = request.POST.get('username')      
        password = request.POST.get('currentpassword')
        new_password = request.POST.get('newpassword')
        print username
        print password
        print new_password
        print "change post method"
        LDAP_SERVER = 'ldap://172.30.1.197'
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
             return render_to_response('changepassword.html',{'password':password, 'username': username})   
        except ldap.INVALID_CREDENTIALS:
             ldap_client.unbind()
             return render_to_response('changepassword.html',{'password':password, 'username': username}) 
             print 'Wrong username or password'
        except ldap.SERVER_DOWN:
             print 'windows active directory not available'

    return render_to_response('changepassword.html',{'password':password, 'username': username})


def help(request):
    username = password = ''
    if request.GET:
        username = request.GET.get('username')        
        print username     
        return render_to_response('help.html',{'username': username})


@csrf_exempt
def instance_stop(request):
    instance_id=''
    if request.POST:
        instance_id = request.POST.get('instance_id')
        instance_name=request.POST.get('instance_name')
        operation=request.POST.get('operation')
        print "********************server start/stop**************************"
        print instance_id
        print instance_name
        print operation
        auth_url = 'http://controller:35357/v3'
        username = 'admin'
        user_domain_name = 'Default'
        project_name = 'admin'
        project_domain_name = 'Default'
        password = 'ADMIN'
        auth =v3.Password(auth_url=auth_url,username=username,password=password,project_id='9ae46562307842439cab73340e7ed47b',
        user_domain_name=user_domain_name)
        sess = session.Session(auth=auth)
        keystone = ksclient.Client(session=sess)
        keystone.projects.list()
        from novaclient import client
        nova = client.Client(2, session=keystone.session)
        server = nova.servers.find(name=instance_name)
        if operation == 'stop':
            server.stop()
        elif operation == 'start':
            server.start()
        elif operation == 'reboot':
            server.reboot(reboot_type='SOFT')         
        #****************** MYSQL coding to check the instances status *************************************
        time.sleep(20)
        db = MySQLdb.connect(host="172.30.1.242",port=3306,user="root",passwd="password",db="nova")
        cursor = db.cursor()
        cursor.execute("select display_name,vm_state from instances where uuid='%s'" % (instance_id))
        results = cursor.fetchall()
        instance=status= instance_id
        for row in results:
             instance = row[0]
             status =row[1]
        db.commit()
        db.close()
        return render_to_response('index.html',{'password':password, 'username': username,'instancename':instance_name,'instanceid':instance_id,'status':status})
 





@csrf_exempt
def change_pswd(request):  
    username = password = ''
    print 'post method'
    if request.POST:        
        password = request.POST.get('inputPassword1')
        print password
        print "change post method"
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        l = ldap.initialize('ldaps://172.30.1.197')
        l.simple_bind_s('Administrator@naanal.local', 'p@ssw0rd1') 
        dn="cn=map1,dc=naanal,dc=local" 
        password='p@ssw0rd1'
        unicode_pass = unicode('\"' + password + '\"', 'iso-8859-1')
        password_value = unicode_pass.encode('utf-16-le')
        print (password_value)
        unicode_pass = unicode('\"' + password + '\"', 'iso-8859-1')
        password_value = unicode_pass.encode('utf-16-le')
        add_pass = [(ldap.MOD_REPLACE, 'unicodePwd', [password_value])]
        l.modify_s(dn, add_pass)
        l.unbind_s()      
        return render_to_response('changepassword.html',{'password':password, 'username': username})   
    
    return render_to_response('changepassword.html',{'password':password, 'username': username})
