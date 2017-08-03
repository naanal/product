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
"""API windows D drive backup 
"""
from django.views import generic
from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils
from django.conf import settings
import json
import os
import subprocess
import time
""" Replace \\NAANAL-PC\Backup  with your backup shared folder """
backup_script=r"\\NAANAL-PC\Backup\Backup.ps1"
restore_latest_script=r"\\NAANAL-PC\Backup\Restore_latest.ps1"
backup_previous_script=r"\\NAANAL-PC\Backup\Restore_previous.ps1"

"""SChdule backup"""
backup_script_location=r'C:\Backup.ps1'

import salt.client
local = salt.client.LocalClient()





@urls.register
class Backup(generic.View):
    """API for salt key list (client machines name)
    """
    url_regex = r'backup/list/$'
    @rest_utils.ajax()
    def get(self, request):
        """ Get a list of salt key (client machines)

        """        
        list_machine_cmd="salt-key -l accepted"
        result = subprocess.check_output(list_machine_cmd, shell=True)
        # print (result)
        client_list=result.split('\n')
        client_list=client_list[1:len(client_list)-1]    
        return(client_list)


    @rest_utils.ajax(data_required=True)
    def post(self, request):

        """
        Inputs: windows machine name , drive letter to make backup

        output [list]:  machine name with backup success of failed status
        """
        try:
            args = (
                request,
                request.DATA['clients'],
                request.DATA['drive']
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])
        cilents=request.DATA['clients']      
        status=[] 
     

        """ Drive that want to Backup"""
        drive_want_to_backup=request.DATA['drive']
        for client in cilents:            
            print client
            backup_cmd='Powershell -noprofile -executionpolicy bypass -file '+backup_script
            result=local.cmd(client, 'cmd.run', [backup_cmd,'shell=powershell'])
            print result

            # if result!=0:
            #     state={"cilent_name":client,"backup_status":"False"}
            #     status.append(state)
            # else:
            #     state={"cilent_name":client,"backup_status":"True"}
            #     status.append(state)

            
                

            # result=os.system(t1)
            # result=os.system(t2)
            # result=os.system(t3)
            # result=os.system(t4)
            # result=os.system(t5)
            # result=os.system(t6)



            
            # if result==0:
            #     result = subprocess.check_output(t2, shell=True)
            #     if result ==0:
            #         result = subprocess.check_output(t3, shell=True)
            #     else:
            #         print("problem in folder creation")

        
        return(status)


@urls.register
class restore(generic.View):
    """API for salt key list (client machines name)
    """
    url_regex = r'restore/list/$'  
    @rest_utils.ajax(data_required=True)
    def post(self, request):

        """
         Restore

        Inputs: windows machine name , backup name to make restore

        output [list]:  machine name with restore success of failed status
        """
        try:
            args = (
                request,
                request.DATA['clients'],
                request.DATA['backup_name'],
                request.DATA['drive']
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])
        cilents=request.DATA['clients']  

        """ Backup name that want to Restore"""
        Selected_backup=request.DATA['backup_name']  

        """ Drive to  restore backup"""
        drive_want_to_restore=request.DATA['drive']
        status=[]
        
        for client in cilents:            
            
            print client
            print("Restore")            
            if Selected_backup=="Latest": 
                print("Latest")               
                backup_cmd='Powershell -noprofile -executionpolicy bypass -file '+restore_latest_script
                result=local.cmd(client, 'cmd.run', [backup_cmd,'shell=powershell'])
                print result
            else:
                print ("Previous")
                backup_cmd='Powershell -noprofile -executionpolicy bypass -file '+backup_previous_script
                result=local.cmd(client, 'cmd.run', [backup_cmd,'shell=powershell'])
                print result
            
        return(status)


@urls.register
class schedule(generic.View):
    """API for salt key list (client machines name)
    """
    url_regex = r'restore/schedule/$'  
    @rest_utils.ajax(data_required=True)
    def post(self, request):     
        try:
            args = (
                request,
                request.DATA['days'],
                request.DATA['times']
            )
        except KeyError as e:
            raise rest_utils.AjaxError(400, 'missing required parameter'
                                            "'%s'" % e.args[0])
        schtask_name="Mybackup"
        days=request.DATA['days']         
        times=request.DATA['times']
        list_machine_cmd="salt-key -l accepted"
        result = subprocess.check_output(list_machine_cmd, shell=True)
        # print (result)
        client_list=result.split('\n')
        client_list=client_list[1:len(client_list)-1]  
        status=[]   
        print(client_list)
        for client in client_list:
            print (client)

            schtask_delete_old='SchTasks /Delete /TN '+schtask_name+' /f'
            schtask='SchTasks /Create /SC WEEKLY /D '+days+' /TN '+'"'+schtask_name+'"'+' /TR '+ backup_script_location+' /ST '+times+' /f'
            ret=local.cmd_iter(client, 'cmd.run', [schtask_delete_old,'shell=powershell'])
            for i in ret:
                print(i)
            time.sleep(5)
            ret=local.cmd_iter(client, 'cmd.run', [schtask,'shell=powershell'])            
            print(schtask_delete_old)
            print(schtask)
            status=[]
            for i in ret:
                print(i)
                status.append(i)
        return(status)


