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

""" Replace \\NAANAL-PC\Backup  with your backup shared folder """
backup_location=r"\\NAANAL-PC\Backup"





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
        print (result)
        client_list=result.split('\n')
        client_list=client_list[1:]
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

        """ Drive that want to Backup"""
        drive_want_to_backup=request.DATA['drive']
        for client in cilents:            
            status=[]
            user="\\"+client
            
            user_name=backup_location+user
            #print (user_name)
            backup1=backup_location+user+"\Backup1"

            backup2=backup_location+user+"\Backup2"
            #print (backup1)
            #print(backup2)
            """BACKUP FOLDER CREATION commands"""
            Name_folder="New-Item -ItemType directory -Path "+user_name +"  -Force;"
            Backup1_folder="New-Item -ItemType directory -Path "+backup1 + " "+"-Force;"
            Backup2_folder="New-Item -ItemType directory -Path "+backup2 + " "+"-Force;"
            
            """Remove BACKUP1 commands"""
            Remove_Backup2_contents="Remove-Item -Recurse -Force "+backup2 +"\*;"

            """Move backup2 into backup1 folder after delete the contants of backup2"""
            move_backup1_backup2="Get-ChildItem -Path "+backup1+" | % {  Copy-Item $_.fullname "+backup2+" -Recurse -Force }"


            """ move selected drive into backup1 folder"""
            actual_backup="Get-ChildItem -Path "+'"'+drive_want_to_backup+'"' +"| % { Copy-Item $_.fullname  "+'"'+backup1+'"'+" -Recurse -Force}"

            t1=("salt "+"'"+client+"'"+" cmd.run " +"'"+Name_folder+"'" +" shell=powershell")
            t2=(" salt "+"'"+client+"'"+" cmd.run " +"'"+Backup1_folder+"'" +" shell=powershell")
            t3=(" salt "+"'"+client+"'"+" cmd.run " +"'"+Backup2_folder+"'" +" shell=powershell")
            t4=(" salt "+"'"+client+"'"+" cmd.run " +"'"+Remove_Backup2_contents+"'" +" shell=powershell")
            t5=(" salt "+"'"+client+"'"+" cmd.run " +"'"+move_backup1_backup2+"'" +" shell=powershell")
            t6=(" salt "+"'"+client+"'"+" cmd.run " +"'"+actual_backup+"'" +" shell=powershell")

            command_list=[t1,t2,t3,t4,t5,t6]
            for cmnd in command_list:
                result=os.system(cmnd)

            if result!=0:
                state={"cilent_name":client,"backup_status":"False"}
                status.append(state)
            else:
                state={"cilent_name":client,"backup_status":"True"}
                status.append(state)

            # result=os.system(t1)
            # result=os.system(t2)
            # result=os.system(t3)
            # result=os.system(t4)
            # result=os.system(t5)
            # result=os.system(t6)



            print result
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
        Selected_backup="\\"+request.DATA['backup_name']  

        """ Drive to  restore backup"""
        drive_want_to_restore=request.DATA['drive']
        
        
        for client in cilents:            
            status=[]
            user="\\"+client
            
            user_name=backup_location+user
            # print (user_name)

            Restore_Backup_selection=user_name+Selected_backup
            #print(Restore_Backup_selection)

            Restore="Get-ChildItem -Path "+'"'+Restore_Backup_selection+'"'+" | % {   Copy-Item $_.fullname "+'"'+drive_want_to_restore+'"'+" -Recurse -Force }"
            """BACKUP FOLDER CREATION commands"""
            t1=(" salt "+"'"+client+"'"+" cmd.run " +"'"+Restore+"'" +" shell=powershell")    
            #print(t1)                 
            result=os.system(t1)
            if result!=0:
                state={"cilent_name":client,"restore_status":"False"}
                status.append(state)
            else:
                state={"cilent_name":client,"restore_status":"True"}
                status.append(state)          
        return(status)


