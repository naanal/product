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


@urls.register
class Users(generic.View):
    """API for AD User Lists, Creation, Disable.
    """
    url_regex = r'ldap/users/$'

    @rest_utils.ajax()
    def get(self, request):
        """ Get a list of AD Users
        """

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
        try:
            args = (request, request.DATA['users'],)
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter '
                                            "'%s'" % e.args[0])
        result = []
        conn = bind()
        if conn.bind():
            for user in request.DATA['users']:
                dn = user['user_dn']
                username=user['username']                
                response = disableUser(dn, conn)                        
                result.append(
                    {"user": user['username'], "action": "Disable",
                     "status": response})
            unbind(conn)
            return result
        else:
            return "Authentication Failed"

    @rest_utils.ajax()
    def patch(self, request):
        try:
            args = (
                request,
                request.DATA['change_pswd'],
                request.DATA['change_dn']
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])

        change_password = request.DATA['change_pswd']
        change_dn = request.DATA['change_dn']
        if(change_password == "True"):

            try:
                args = (
                    request,
                    request.DATA['user_dn'],
                    request.DATA['password']
                )
            except KeyError as e:
                raise rest_utils.AjaxError(400, 'missing required parameter'
                                           "'%s'" % e.args[0])
            dn = request.DATA['user_dn']
            password = request.DATA['password']
            password = str(password)
            conn = bind()
            if conn.bind():
                change_pswdStatus = changePassword(dn, password, conn)
                unbind(conn)
                return change_pswdStatus
            else:
                return "Authentication Failed"

        if(change_dn == "True"):
            print "change the distniguesd name of the user method"
            try:
                args = (
                    request,
                    request.DATA['user_dn'],
                    request.DATA['new_username'],
                    request.DATA['email']
                )
            except KeyError as e:
                raise rest_utils.AjaxError(400, 'missing required parameter'
                                           "'%s'" % e.args[0])
            user_dn = request.DATA['user_dn']
            new_username = request.DATA['new_username']
            E_mail = request.DATA['email']
            print user_dn, new_username, E_mail
            conn = bind()
            if conn.bind():
                change_userPrincipalNameStatus = change_userPrincipalName(
                    user_dn, new_username, conn)
                change_sAMAccountNameStatus = change_sAMAccountName(
                    user_dn, new_username, conn)
                change_userEmailStatus = change_userEmail(
                    user_dn, E_mail, conn)
                change_dnstatus = change_userDN(user_dn, new_username, conn)
                unbind(conn)
                return change_userPrincipalNameStatus, change_sAMAccountNameStatus, change_dnstatus
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
            return result

        else:
            return "Authentication Failed"


def bind():
    s = Server(settings.LDAP_SERVER, port=settings.LDAP_SERVER_PORT,
               use_ssl=settings.LDAP_SSL, get_info=ALL)
    conn = Connection(s, user=settings.LDAP_ADMIN_USERNAME,
                      password=settings.LDAP_ADMIN_PASSWORD, auto_bind=True)
    conn.start_tls()
    return conn


def unbind(c):
    c.unbind()


def getdn(username):
    return 'cn=%s,ou=users,ou=Police,dc=naanal,dc=local' % (username)


def createNewUser(dn, username, mail, conn):
    conn.add(dn, ['Top', 'person', 'user'],
             {'cn': username,
              'userPrincipalName': '%s@%s' % (username, settings.LDAP_DNS),
              'userWorkstations': settings.LDAP_SERVER_MACHINE_NAME,
              'mail': mail,
              'sAMAccountName': username})

    return conn.result['description']


def disableUser(dn, conn):
    conn.modify(dn, {'userAccountControl': [(MODIFY_REPLACE, ['514'])]})
    return conn.result['description']


def enableUser(dn, conn):
    conn.modify(dn, {'userAccountControl': [(MODIFY_REPLACE, ['512'])]})
    return conn.result['description']


def changePassword(dn, password, conn):
    unicode_pass = unicode('"' + password + '"', 'iso-8859-1')
    encoded_pass = unicode_pass.encode('utf-16-le')
    conn.modify(dn, {'unicodePwd': [(MODIFY_REPLACE, [encoded_pass])]})
    conn.modify(dn, {'unicodePwd': [(MODIFY_REPLACE, [encoded_pass])]})
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
            users.append({
                "user_dn": entry['dn'],
                "username": entry['attributes']['cn'],
                "mail": mail,
                "group": groups,
                "lastLogon": entry['attributes']['lastLogon'].isoformat(" ").split(".")[0],
                "computer": assigned_computer,
                "status": entry['attributes']['userAccountControl']
            })
    return users


def retriveAvailableUsers(conn):
    available_users = []
    conn.search(search_base=settings.LDAP_BASE_DIR,
                search_filter='(&(objectCategory=person)(objectClass=user)(memberof=cn=normalusers,ou=groups,ou=police,dc=naanal,dc=local)(|(userAccountControl=512)(userAccountControl=66048)))',
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
    conn.search(search_base='dc=naanal,dc=local',
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
    conn.search(search_base='cn=computers,dc=naanal,dc=local',
                search_filter='(&(objectCategory=computer)(objectClass=computer))',
                search_scope=SUBTREE, attributes=[ALL_ATTRIBUTES,
                                                  ALL_OPERATIONAL_ATTRIBUTES])

    for entry in conn.response:
        if 'attributes' in entry:
            if entry['attributes']['cn'] in assignedCom:
                status = "not available"
            else:
                status = "available"

            computers.append({
                "dn": entry['dn'],
                "computername": entry['attributes']['cn'],
                "status": status
            })
    unbind(conn)
    return computers


def retriveAvailableComputers(conn):
    available_computers = []
    assignedCom = list(set(assignedComputers(conn)))
    conn.search(search_base='cn=computers,dc=naanal,dc=local',
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
    computers = computer + ',' + settings.LDAP_SERVER_MACHINE_NAME
    conn.modify(user_dn, {'userWorkstations': [(MODIFY_REPLACE, computers)]})
    return conn.result['description']


def autoAssignUsersWithVms(map_data, conn):
    users = map_data
    map_data = []
    available_vms = retriveAvailableComputers(conn)
    user_len = len(users)
    vm_len = len(available_vms)
    if (user_len > vm_len):
        return {"message": "You have selected %s users. But %s computers only available" % (user_len, vm_len)}
    else:
        sliced_vms = available_vms[:user_len]
        for user, vm in zip(users, sliced_vms):
            map_data.append(
                {"user_dn": user['user_dn'], "computer": vm['computername']})
    return map_data


def change_userPrincipalName(user_dn, new_username, conn):
    new_username = new_username + '@naanal.local'
    conn.modify(user_dn,
                {'userPrincipalName': [(MODIFY_REPLACE, [new_username])]})
    print "status of userPrincipal name change:::::" + conn.result['description']
    return conn.result['description']


def change_sAMAccountName(user_dn, new_username, conn):
    conn.modify(user_dn,
                {'sAMAccountName': [(MODIFY_REPLACE, [new_username])]
                 })
    print("status of change_sAMAccountName::::" + conn.result['description'])
    return conn.result['description']


def change_userEmail(user_dn, E_mail, conn):
    conn.modify(user_dn,
                {'mail': [(MODIFY_REPLACE, [E_mail])]})
    print("status of change_userEmail::::" + conn.result['description'])
    return conn.result['description']


def change_userDN(user_dn, new_username, conn):
    new_username = 'cn=' + new_username
    conn.modify_dn(user_dn, new_username)
    print("status of change_userDN::::" + conn.result['description'])
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
                                print notSufficentVMs
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
