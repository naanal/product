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
    ALL_OPERATIONAL_ATTRIBUTES, MODIFY_REPLACE, MODIFY_ADD


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
        :ou: Organizaional Unit of User
        :domain: domain name of active directory

        This returns status of user creation.
        """
        try:
            args = (
                request,
                request.DATA['users'],
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])
        result = []
        conn = bind()
        if conn.bind():
            for user in request.DATA['users']:

                creation_response = password_response = enable_response = ''
                username = user['username']
                password = user['password'].encode('ascii', 'ignore')
                ou = user['ou']
                dns = user['dns']

                dn = getdn(username, ou)

                # 1. Create a New User
                creation_response = createNewUser(dn, username, dns, conn)

                # 2. If user Creation success then modify the password
                if creation_response == 'success':
                    password_response = changePassword(dn, password, conn)

                    # 3. If Password Modification success then enable user
                    # account
                    if password_response == 'success':
                        enable_response = enableUser(dn, conn)

                result.append({"user": username, "action": "creation",
                               "addNewUser": creation_response,
                               "addPassword": password_response,
                               "enableAccount": enable_response})
                unbind(conn)
            return result

        else:
            return "Authendication Failed"

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
                dn = getdn(user['username'], user['ou'])
                response = disableUser(dn, conn)
                result.append(
                    {"user": user['username'], "action": "disable",
                     "status": response})
            unbind(conn)
            return result
        else:
            return "Authentication Failed"


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
class Computers(generic.View):
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
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])
        result = []
        conn = bind()
        if conn.bind():
            for data in request.DATA['map']:

                group_response = map_response = ''
                user_dn = data['user_dn']
                computer = data['computer']

                # 1. Add User to 'allowed' group
                group_response = addToGroup(user_dn, conn)

                # 2. If user added to 'allowed' group successfully then map the
                # user to vm
                if group_response == 'success':
                    map_response = mapUserToVm(user_dn, computer, conn)

                result.append({"user": user_dn, "action": "maping",
                               "addToGroup": group_response,
                               "mapToVm": map_response})
                unbind(conn)
            return result

        else:
            return "Authendication Failed"


def bind():
    s = Server(settings.LDAP_SERVER, port=settings.LDAP_SERVER_PORT,
               use_ssl=settings.LDAP_SSL, get_info=ALL)
    conn = Connection(s, user=settings.LDAP_ADMIN_USERNAME,
                      password=settings.LDAP_ADMIN_PASSWORD, auto_bind=True)
    conn.start_tls()
    return conn


def unbind(c):
    c.unbind()


def getdn(username, ou):
    return 'cn=%s,ou=%s,dc=naanal,dc=local' % (username, ou)


def createNewUser(dn, username, dns, conn):
    conn.add(dn, ['Top', 'person', 'user'],
             {'cn': username, 'userPrincipalName': '%s@%s' % (username, dns),
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
    return conn.result['description']


def addToGroup(user_dn, conn):
    group_dn = settings.ENABLE_USERS_GROUP_DN
    conn.modify(group_dn, {'member': [(MODIFY_ADD, user_dn)]})
    return conn.result['description']


def retriveUsers(conn):
    users = []
    conn.search(search_base='dc=naanal,dc=local',
                search_filter='(&(objectCategory=person)(objectClass=user))',
                search_scope=SUBTREE, attributes=[ALL_ATTRIBUTES,
                                                  ALL_OPERATIONAL_ATTRIBUTES])
    for entry in conn.response:
        if 'attributes' in entry:
            if 'userWorkstations' in entry['attributes']:
                assigned_computer = entry['attributes']['userWorkstations']
            else:
                assigned_computer = None
            users.append({
                "dn": entry['dn'],
                "username": entry['attributes']['cn'],
                "computer": assigned_computer,
                "status": entry['attributes']['userAccountControl']
            })
    return users


def assignedComputers(conn):
    assigned_computers = []
    conn.search(search_base='dc=naanal,dc=local',
                search_filter='(&(objectCategory=person)(objectClass=user))',
                search_scope=SUBTREE, attributes=[ALL_ATTRIBUTES,
                                                  ALL_OPERATIONAL_ATTRIBUTES])
    for entry in conn.response:
        if 'attributes' in entry:
            if 'userWorkstations' in entry['attributes']:
                assigned_computers.append(
                    entry['attributes']['userWorkstations'])
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
    assignedCom = assignedComputers(conn)
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
    unbind(conn)
    return available_computers


def mapUserToVm(user_dn, computer, conn):
    conn.modify(user_dn, {'userWorkstations': [(MODIFY_REPLACE, computer)]})
    return conn.result['description']
