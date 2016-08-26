# Copyright 2016 Naanal Technologies Pvt Limited.
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
"""API over the ldap service.
"""

from django.views import generic

from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils
from django.conf import settings
from ldap3 import Server, Connection, SUBTREE, ALL, ALL_ATTRIBUTES, \
    ALL_OPERATIONAL_ATTRIBUTES, MODIFY_REPLACE, MODIFY_ADD, MODIFY_INCREMENT
import ldap3
import logging
adminlog = logging.getLogger('adminlog')
ip=''
user=''
from openstack_dashboard.api import keystone
import os
b=os.path.getsize("admin.log")
b=b/1024
b=b/1024
if(b>=50):    
    fo=open('admin.log',"wb")
    fo.truncate()
@urls.register
class Users(generic.View):
    """API for AD User Lists, Creation, Disable.
    """
    url_regex = r'ldap/users/$'

    @rest_utils.ajax()
    def get(self, request):
        """ Get a list of AD Users
        """ 
        global user  
        ip=get_ip(request)
        user = request.user       
        d={'clientip':ip,'username':user} 
        conn = bind()
        if conn.bind():
            return retriveUsers(conn)
        else:
            return "Authendication Failed"

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Create a list Of users in Active Directory Directive Services.

        Create users using the parameters supplied in the POST
        application/json object. The parameters are:

        :param users : array of users

         Each Users array must have
        :username: the username to give to the user
        :password: the password given to the user
        :mail: mail id of the user

        This returns status of user creation.
        """
        try:
            args = (
                request,
                request.DATA['users'],
                request.DATA['isAssignVm'],
                request.DATA['isAutoMap']
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])
        result = []
        conn = bind()
        if conn.bind():
            users = request.DATA['users']
            isAssignVm = request.DATA['isAssignVm']
            isAutoMap = request.DATA['isAutoMap']
            return userCreationWorkflow(users, isAssignVm, isAutoMap, conn)

        else:
            return "Authentication Failed"

    @rest_utils.ajax()
    def delete(self, request):
        """Disable users in Active Directory Directive Services.

        Disable users using the parameters supplied in the POST
        application/json object. The parameters are:

        :param users : array of users

        Each Users array must have
        :username: the username to give to the user
        :ou: Organizaional Unit of User

        This returns status of Disabled User.
        """ 
        global user  
        ip=get_ip(request)
        user = request.user       
        d={'clientip':ip,'username':user} 
        try:
            args = (request, request.DATA['users'],)
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter '
                                            "'%s'" % e.args[0])
        enable=request.DATA['enable']
        # Enable user 
        if(enable==True):             
            result = []
            conn = bind()
            if conn.bind():
                for user in request.DATA['users']:
                    dn = user['user_dn']
                    username=user['username']                
                    adminlog.info("Enable user::%s",username,extra=d)
                    response = enableUser(dn, conn) 
                    adminlog.info(" Enable user ::%s %s ",username,response,extra=d)                                          
                    result.append(
                        {"user": user['username'], "action": "Enable",
                         "status": response})
                unbind(conn)                
                return result
            else:
                return "Authentication Failed"

        result = []
        conn = bind()
        if conn.bind():
            
            for user in request.DATA['users']:
                dn = user['user_dn']
                username=user['username']                 
                response = disableUser(dn, conn)                 
                adminlog.info(" Disable user :: %s %s",username,response,extra=d)                      
                result.append(
                    {"user": user['username'], "action": "Disable",
                     "status": response})
            unbind(conn)            
            return result
        else:
            return "Authentication Failed"





    @rest_utils.ajax()
    def patch(self, request):
        global user  
        ip=get_ip(request)
        user = request.user       
        d={'clientip':ip,'username':user}         
        try:
            args = (
                request,
                request.DATA['users'],
                request.DATA['change_password'],
                request.DATA['change_commonName'],
                request.DATA['change_computer'],
                request.DATA['password']
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])

        users = request.DATA['users']
        change_password = request.DATA['change_password']        
        change_computer = request.DATA['change_computer']
        change_commonName = request.DATA['change_commonName'] 
        password= request.DATA['password']         
       
        if(change_password==True and change_commonName==True and change_computer==True):                       
            result = [] 
            conn = bind()
            if conn.bind():
                for user in users:
                    username = user['name']
                    dn=user['dn']
                    computer=user['new_computer']
                    new_username=user['new_username']
                    #password=user['password']
                    password = str(password)                                    
                    changepasswordStatus= changePassword(dn, password, conn)
                    result.append({"user": username,"action": "change_password","status": changepasswordStatus}) 
                    change_computerstatus=mapUserToVm(dn,computer,conn)
                    result.append({"user": username,"action": "change_computer","status": change_computerstatus}) 
                    change_userPrincipalNameStatus = change_userPrincipalName(dn, new_username, conn)
                    change_sAMAccountNameStatus = change_sAMAccountName(dn, new_username, conn)                
                    change_dnstatus = change_userDN(dn, new_username, conn)               
                    result.append({"user": username,"action": "change_commonName","status": change_dnstatus})                     
                unbind(conn)                
                return result
            else:
                return "Authentication Failed"

           

        elif(change_commonName==True and change_computer==True):                        
            result = [] 
            conn = bind()
            if conn.bind():
                for user in users:
                    username = user['name']
                    dn=user['dn']
                    computer=user['new_computer']
                    new_username=user['new_username']
                    change_computerstatus=mapUserToVm(dn,computer,conn)
                    result.append({"user": dn,"action": "change_computer","status": change_computerstatus}) 
                    change_userPrincipalNameStatus = change_userPrincipalName(dn, new_username, conn)
                    change_sAMAccountNameStatus = change_sAMAccountName(dn, new_username, conn)                
                    change_dnstatus = change_userDN(dn, new_username, conn)               
                    result.append({"user": username,"action": "change_commonName","status": change_dnstatus})                     
                unbind(conn)                
                return result
            else:
                return "Authentication Failed"
            
        elif(change_commonName==True and change_password==True):            
            result = [] 
            conn = bind()
            if conn.bind():
                for user in users:
                    username = user['name']
                    dn=user['dn']                    
                    new_username=user['new_username']
                    #password=user['password']
                    password = str(password)                              
                    changepasswordStatus= changePassword(dn, password, conn)
                    result.append({"user": dn,"action": "change_password","status": changepasswordStatus})                    
                    change_userPrincipalNameStatus = change_userPrincipalName(dn, new_username, conn)
                    change_sAMAccountNameStatus = change_sAMAccountName(dn, new_username, conn)                
                    change_dnstatus = change_userDN(dn, new_username, conn)               
                    result.append({"user": username,"action": "change_commonName","status": change_dnstatus})                     
                unbind(conn)                
                return result
            else:
                return "Authentication Failed"
            
            
        elif(change_password==True and change_computer==True):            
            result = [] 
            conn = bind()
            if conn.bind():
                for user in users:
                    username = user['name']
                    dn=user['dn']
                    computer=user['new_computer']                    
                    #password=user['password']
                    password = str(password)                           
                    changepasswordStatus= changePassword(dn, password, conn)
                    result.append({"user": dn,"action": "change_password","status": changepasswordStatus}) 
                    change_computerstatus=mapUserToVm(dn,computer,conn)
                    result.append({"user": username,"action": "change_computer","status": change_computerstatus})                                 
                unbind(conn)                
                return result
            else:
                return "Authentication Failed"
               
        elif(change_password==True):            
            result = [] 
            conn = bind()
            if conn.bind():
                for user in users:
                    username = user['name']
                    dn=user['dn']                    
                    #password=user['password']
                    password = str(password)                    
                    changepasswordStatus= changePassword(dn, password, conn)
                    result.append({"user": username,"action": "change_password","status": changepasswordStatus})                                          
                unbind(conn)                
                return result
            else:
                return "Authentication Failed"
        elif(change_computer==True):            
            result = [] 
            conn = bind()
            if conn.bind():
                for user in users:
                    username = user['name']
                    dn=user['dn']
                    computer=user['new_computer']                            
                    change_computerstatus=mapUserToVm(dn,computer,conn)
                    result.append({"user": username,"action": "change_computer","status": change_computerstatus}) 
                unbind(conn)                
                return result
            else:
                return "Authentication Failed"

        elif(change_commonName==True):            
            result = [] 
            conn = bind()
            if conn.bind():
                for user in users:
                    username = user['name']
                    dn=user['dn']                    
                    new_username=user['new_username']                    
                    change_userPrincipalNameStatus = change_userPrincipalName(dn, new_username, conn)
                    change_sAMAccountNameStatus = change_sAMAccountName(dn, new_username, conn)                
                    change_dnstatus = change_userDN(dn, new_username, conn)               
                    result.append({"user": username,"action": "change_commonName","status": change_dnstatus})                     
                unbind(conn)                
                return result
            else:
                return "Authentication Failed"





@urls.register
class AvailableUsers(generic.View):
    """ API for Available(Enabled & Unattached to computer) Users Lists
    """
    url_regex = r'ldap/available_users/$'

    @rest_utils.ajax()
    def get(self, request):
        conn = bind()
        if conn.bind():
            return retriveAvailableUsers(conn)
        else:
            return "Authendication Failed"


@urls.register
class Computers(generic.View):
    """ API for Computer Lists
    """
    url_regex = r'ldap/computers/$'

    @rest_utils.ajax()
    def get(self, request):
        conn = bind()
        if conn.bind():
            return retriveComputers(conn)
        else:
            return "Authendication Failed"


@urls.register
class AvailableComputers(generic.View):
    """ API for Available Computer Lists
    """
    url_regex = r'ldap/available_computers/$'

    @rest_utils.ajax()
    def get(self, request):
        conn = bind()
        if conn.bind():
            return retriveAvailableComputers(conn)
        else:
            return "Authendication Failed"


@urls.register
class Map(generic.View):
    """ API for User - VM Mapping
    """
    url_regex = r'ldap/map/$'

    @rest_utils.ajax(data_required=True)
    def post(self, request):
        """Map User-Vm in Active Directory Directive Services.

        Map User-Vm using the parameters supplied in the POST
        application/json object. The parameters are:

        :param map : array of users, vms

         Each map array must have
        :user_dn: the distiniguished name of user
        :computer: the name given to the computer

        This returns status of user creation.
        """
        global user  
        ip=get_ip(request)
        user = request.user       
        d={'clientip':ip,'username':user}       
        adminlog.info("Assing Virtual Machine to users",extra=d)
        try:
            args = (
                request,
                request.DATA['map'],
                request.DATA['autoMap']
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])
        result = []
        map_data = request.DATA['map']
        isAuto = request.DATA['autoMap']
        conn = bind()

        if(isAuto == 'True'):
            map_data = autoAssignUsersWithVms(map_data, conn)
            adminlog.debug("Status Assing Virtual Machine to users:%s",map_data,extra=d)

        if conn.bind():
            for data in map_data:
                user_dn = data['user_dn']
                computer = data['computer']
                # 1. Add User to 'allowed' group
                allowed_group_name = settings.ALLOWED_USERS_GROUP_DN
                response = addToGroup(allowed_group_name, user_dn, conn)

                # 2. If user added to 'allowed' group successfully then map the
                # user to vm
                if response == 'success' or response == 'entryAlreadyExists':
                    response = mapUserToVm(user_dn, computer, conn)
                else:
                    response = response + " in the group"

                result.append({"user": user_dn, "assigned_computer": computer,
                               "action": "maping",
                               "status": response})
            unbind(conn)
            adminlog.debug(" Assing Virtual Machine to users:%s",result,extra=d)
            return result

        else:
            return "Authentication Failed"


def bind():    
    d={'clientip':ip,'username':user} 
    try:        
        s = Server(settings.LDAP_SERVER[0], port=settings.LDAP_SERVER_PORT,
               use_ssl=settings.LDAP_SSL, get_info=ALL)
        conn = Connection(s, user=settings.LDAP_ADMIN_USERNAME,
                      password=settings.LDAP_ADMIN_PASSWORD, auto_bind=True)
        conn.start_tls()
        return conn      
    except ldap3.LDAPSocketOpenError:                
        adminlog.info("Error occured to Connect:: %s the Windows Server",settings.LDAP_SERVER[0],extra=d)             
        try:
            s = Server(settings.LDAP_SERVER[1], port=settings.LDAP_SERVER_PORT,
               use_ssl=settings.LDAP_SSL, get_info=ALL)
            conn = Connection(s, user=settings.LDAP_ADMIN_USERNAME,
                          password=settings.LDAP_ADMIN_PASSWORD, auto_bind=True)
            conn.start_tls()
            return conn             
        except Exception, e:
            adminlog.info("Error occured to  Connect  both %s the Windows Servers",settings.LDAP_SERVER,extra=d)             
            adminlog.exception("Error occured to Connect the Windows Server",extra=d)       
        
def unbind(c):
    c.unbind()

def getdn(username):
    return ("cn=%s," + settings.WINDOWS_SERVER_USERPATH + "," + settings.WINDOWS_SERVER_DOMAINPATH) % username
    #return 'cn=%s,ou=users,ou=Police,dc=naanal,dc=local' % (username)


def createNewUser(dn, username, mail, conn):    
    d={'clientip':ip,'username':user}     
    conn.add(dn, ['Top', 'person', 'user'],
             {'cn': username,
              'userPrincipalName': '%s@%s' % (username, settings.LDAP_DNS),
              'userWorkstations': settings.LDAP_SERVER_MACHINE_NAME,
              'mail': mail,
              'sAMAccountName': username})
    adminlog.info(" Create New User:%s  %s",username,conn.result['description'],extra=d)
    return conn.result['description']


def disableUser(dn, conn):
    conn.modify(dn, {'userAccountControl': [(MODIFY_REPLACE, ['514'])]})
    return conn.result['description']


def enableUser(dn, conn):
    conn.modify(dn, {'userAccountControl': [(MODIFY_REPLACE, ['512'])]})
    return conn.result['description']


def changePassword(dn, password, conn):    
    d={'clientip':ip,'username':user}     
    unicode_pass = unicode('"' + password + '"', 'iso-8859-1')
    encoded_pass = unicode_pass.encode('utf-16-le')
    conn.modify(dn, {'unicodePwd': [(MODIFY_REPLACE, [encoded_pass])]})
    conn.modify(dn, {'unicodePwd': [(MODIFY_REPLACE, [encoded_pass])]})
    adminlog.info(" change_password of the user:%s   %s",dn,conn.result['description'],extra=d)
    return conn.result['description']


def addToGroup(group_dn, user_dn, conn):
    conn.modify(group_dn, {'member': [(MODIFY_ADD, user_dn)]})
    return conn.result['description']


def retriveUsers(conn):    
    users = []    
    conn.search(search_base=settings.LDAP_BASE_DIR,
                search_filter='(&(objectCategory=person)(objectClass=user))',
                search_scope=SUBTREE, attributes=[ALL_ATTRIBUTES,
                                                  ALL_OPERATIONAL_ATTRIBUTES])
    for entry in conn.response:
        if 'attributes' in entry:

            if 'userWorkstations' in entry['attributes']:
                assigned_computer = entry['attributes']['userWorkstations']
            else:
                assigned_computer = None
            if 'mail' in entry['attributes']:
                mail = entry['attributes']['mail']
            else:
                mail = None
            if 'memberOf' in entry['attributes']:
                groups = entry['attributes']['memberOf']
            else:
                groups = None
            if 'lastLogon' in entry['attributes']:
                lastLogon=entry['attributes']['lastLogon'].isoformat(" ").split(".")[0]
            else:
                lastLogon=''
            users.append({
                "user_dn": entry['dn'],
                "username": entry['attributes']['cn'],
                "mail": mail,
                "group": groups,
                "lastLogon": lastLogon,
                "computer": assigned_computer,
                "status": entry['attributes']['userAccountControl']
            })
    return users


def retriveAvailableUsers(conn):        
    available_users = []
    conn.search(search_base=settings.LDAP_BASE_DIR,
                search_filter='(&(objectCategory=person)(objectClass=user)(memberof='+settings.WINDOWS_SERVER_USER_GROUP+')(|(userAccountControl=512)(userAccountControl=66048)))',
                search_scope=SUBTREE, attributes=[ALL_ATTRIBUTES,
                                                  ALL_OPERATIONAL_ATTRIBUTES])
    for entry in conn.response:
        if 'attributes' in entry:
            if 'userWorkstations' not in entry['attributes'] or entry['attributes']['userWorkstations'] == settings.LDAP_SERVER_MACHINE_NAME:
                available_users.append({
                    "user_dn": entry['dn'],
                    "username": entry['attributes']['cn']
                })
    return available_users


def assignedComputers(conn):       
    assigned_computers = []   
    conn.search(search_base=settings.WINDOWS_SERVER_DOMAINPATH,
                search_filter='(&(objectCategory=person)(objectClass=user))',
                search_scope=SUBTREE, attributes=[ALL_ATTRIBUTES,
                                                  ALL_OPERATIONAL_ATTRIBUTES])
    for entry in conn.response:
        if 'attributes' in entry:
            if 'userWorkstations' in entry['attributes']:

                computers = entry['attributes']['userWorkstations']
                computerArray = computers.split(',')
                for c in computerArray:
                    assigned_computers.append(c)
    return assigned_computers


def retriveComputers(conn):    
    computers = []
    assignedCom = assignedComputers(conn)
    conn.search(search_base='cn=computers,'+settings.WINDOWS_SERVER_DOMAINPATH,
                search_filter='(&(objectCategory=computer)(objectClass=computer))',
                search_scope=SUBTREE, attributes=[ALL_ATTRIBUTES,
                                                  ALL_OPERATIONAL_ATTRIBUTES])

    for entry in conn.response:
        if 'attributes' in entry:
            if entry['attributes']['cn'] in assignedCom:
                status = "not available"
                computername=entry['attributes']['cn']
                username=findUsername(computername,conn)
            else:
                status = "available"
                username="-----"

            computers.append({
                "dn": entry['dn'],
                "username":username,
                "computername": entry['attributes']['cn'],
                "status": status
            })
    unbind(conn)
    return computers
def findUsername(computername,conn):
    users=retriveUsers(conn)        
    assigned_computer=[]
    for user in users:
        computer=user['computer']        
        if computer is not None:       
            computerArray = computer.split(',')
            if computername in computerArray:
                username=user['username']               
                return username 


def retriveAvailableComputers(conn):
    available_computers = []
    assignedCom = list(set(assignedComputers(conn)))
    conn.search(search_base='cn=computers,'+settings.WINDOWS_SERVER_DOMAINPATH,
                search_filter='(&(objectCategory=computer)(objectClass=computer))',
                search_scope=SUBTREE, attributes=[ALL_ATTRIBUTES,
                                                  ALL_OPERATIONAL_ATTRIBUTES])

    for entry in conn.response:
        if 'attributes' in entry:
            if entry['attributes']['cn'] not in assignedCom:
                available_computers.append({
                    "dn": entry['dn'],
                    "computername": entry['attributes']['cn']
                })
    return available_computers


def mapUserToVm(user_dn, computer, conn):     
    d={'clientip':ip,'username':user}     
    computers = computer + ',' + settings.LDAP_SERVER_MACHINE_NAME
    conn.modify(user_dn, {'userWorkstations': [(MODIFY_REPLACE, computers)]})
    adminlog.info(" Map virtual Machine to user: %s  computer Name: %s   %s",user_dn,computer,conn.result['description'],extra=d)
    return conn.result['description']


def autoAssignUsersWithVms(map_data, conn):
    users = map_data
    map_data = []
    available_vms = retriveAvailableComputers(conn)
    user_len = len(users)
    vm_len = len(available_vms)    
    d={'clientip':ip,'username':user} 
    if (user_len > vm_len):
        adminlog.error( "You have selected %s users. But %s computers only available" , user_len, vm_len,extra=d)
        return {"message": "You have selected %s users. But %s computers only available" % (user_len, vm_len)}
    else:
        sliced_vms = available_vms[:user_len]
        for user, vm in zip(users, sliced_vms):
            map_data.append(
                {"user_dn": user['user_dn'], "computer": vm['computername']})
    adminlog.info("Automatically assign user with vm:: %s",map_data)
    return map_data


def change_userPrincipalName(user_dn, new_username, conn):     
    d={'clientip':ip,'username':user} 
    adminlog.info("change_userPrincipalName Process",extra=d)
    new_username = new_username +'@'+settings.DOMAIN_NAME
    conn.modify(user_dn,
                {'userPrincipalName': [(MODIFY_REPLACE, [new_username])]})
    return conn.result['description']


def change_sAMAccountName(user_dn, new_username, conn):     
    d={'clientip':ip,'username':user} 
    adminlog.info("Change _sAMAccountName Process",extra=d)
    conn.modify(user_dn,
                {'sAMAccountName': [(MODIFY_REPLACE, [new_username])]
                 })
    return conn.result['description']


def change_userEmail(user_dn, E_mail, conn):
    conn.modify(user_dn,
                {'mail': [(MODIFY_REPLACE, [E_mail])]})
    return conn.result['description']


def change_userDN(user_dn, new_username, conn):               
    d={'clientip':ip,'username':user}     
    new_username = 'cn=' + new_username
    conn.modify_dn(user_dn, new_username)
    adminlog.info("change CommonName user:%s with new username:  %s   %s",user_dn,new_username,conn.result['description'],extra=d)
    return conn.result['description']


def userCreationWorkflow(users, isAssignVm, isAssignAuto, conn):    
    user_creation_result = []
    if isAssignVm == "True":
        available_vms = retriveAvailableComputers(conn)
        user_len = len(users)
        vm_len = len(available_vms)
        if (user_len > vm_len):
            notSufficentVMs = "True"
        else:
            notSufficentVMs = "False"
    for user in users:
        username = user['username']
        password = user['password'].encode('ascii', 'ignore')
        if 'mail' in user:
            mail = user['mail']
        else:
            mail = '----'
        if 'computer' in user:
            computer = user['computer']
        dn = getdn(username)

        # 1. Create a new User
        response = createNewUser(dn, username, mail, conn)

        # 2. If User Creation success then modify the password
        if response == 'success':
            response = changePassword(dn, password, conn)

            # 3. If Password Modification success then enable user
            # account
            if response == 'success':
                response = enableUser(dn, conn)

                # 4. If user account enabled then add user to 'normaluser'
                # group
                if response == 'success':
                    response = addToGroup(
                        settings.DEFAULT_USERS_GROUP_DN, dn, conn)

                    # 5. For Vm Mapping, map a vm to user
                    if response == 'success':
                        response = username + " successfully created."
                        if isAssignVm == 'True':
                            if notSufficentVMs == 'False':
                                if isAssignAuto == 'True':
                                    computer = available_vms.pop()['computername']
                                response = mapUserToVm(dn, computer, conn)

                                # 6. Finally if VM get Mapped then add user account to
                                # allowed group
                                if response == 'success':
                                    response = addToGroup(
                                        settings.ALLOWED_USERS_GROUP_DN, dn, conn)
                                    if response != 'success':
                                        response = response + "while adding to allowed group for " + username
                                    else:
                                        response = username + " successfully created and " + computer + " is assigned."
                                else:
                                    response = username + " created. But " + response + " while map to workstation"
                            else:
                                response = "Not Having Sufficient VMs"
                    else:
                        response = response + "while adding to default users group for " + username
                else:
                    response = response + " while enabling" + username + " account"
            else:
                response = response + " while changing password for " + username
        else:
            response = response + " while creating " + username
        user_creation_result.append({
            "user": username,
            "user_dn": dn,
            "action": "creation",
            "status": response
        })    
    return user_creation_result

def get_ip(request):
    global ip
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:       
        ip = request.META.get('REMOTE_ADDR') 
    return ip