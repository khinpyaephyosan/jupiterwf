#!/usr/bin/python

# Copyright: (c) 2018, Lillian Phyoe <khinpyaephyosan@gmail.com>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: jupiter_netme

short_description: This is my test module for jupiter vsat modem

version_added: "2.4"

description:
     - "Jump to first host which has well connection with jupiter vsat modem then jump to modem and push commands"

options:
     commands:
       description:
           - This is input of commands to push to modem.
       required: true

     first_host_ip:
       description:
         - This is IP address of host which connected with vsat modem.
       required: true

     first_host_usr:
       description:
          - This is username of host which connected wotj vsat  modem.
       required: true

     first_host_pass:
       description:
         - This is password of host which connected wotj vsat  modem.
       required: true

     sec_host_ip:
       description:
          - This is modem serial number
       required: true

     sec_host_usr:
       description:
          - This is username of jupiter vsat modem.
       required: true

     sec_host_pass:
       description:
         - This is password of jupiter vsat modem.
       required: true

author:
  - Lillian Phyoe 
'''

EXAMPLES = '''
# Push in commands
- name: push command to jupiter vsat modem
  jupiter_netme:
    commands: "route -n"
    first_host_ip: "{{ FirstHostIP }}"
    first_host_usr: "{{ FirstHostUsername }}"
    first_host_pass: "{{ FirstHostPassword }}"
    sec_host_ip: "{{ ModemIP }}"
    sec_host_usr: "{{ ModemUsername }}"
    sec_host_pass: "{{ ModemPassword }}"
'''

RETURN = ''' 
result:
  changed: True,
  original_message=net_me output,
  message='Good Job'
'''

#Ansible imports
from ansible.module_utils.basic import AnsibleModule

#default imports
import paramiko
import sys
import subprocess

def net_me(commands,first_host_ip,first_host_usr,first_host_pass,sec_host_usr,sec_host_pass,sec_host_ip):
    result=""

    first_jump = paramiko.SSHClient()
    first_jump.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    first_jump.connect(first_host_ip, username=first_host_usr, password=first_host_pass, allow_agent=False) #first ssh jump

    first_jumptransport = first_jump.get_transport()
    dest_addr = (sec_host_ip,22)
    local_addr = (first_host_ip, 22)
    first_jumpchannel = first_jumptransport.open_channel("direct-tcpip", dest_addr, local_addr) #second ssh jump

    second_jump = paramiko.SSHClient()
    second_jump.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    second_jump.connect(sec_host_ip, username=sec_host_usr, password=sec_host_pass, allow_agent=False, sock=first_jumpchannel)

    for each_line in commands:
       stdin, stdout, stderr = second_jump.exec_command(each_line + '\n') #push command to modem   
       result += stdout.read()
    
    return result
    second_jump.close()
    first_jump.close()	
		
	

def run_module():
    module_args = dict(
      commands=dict(type='list',required=True),
      first_host_ip=dict(type='str', required=True),
      first_host_usr=dict(type='str',required=True),
      first_host_pass=dict(type='str',required=True),
      sec_host_ip=dict(type='str', required=True),
      sec_host_usr=dict(type='str',required=True),
      sec_host_pass=dict(type='str',required=True),
    )
		
    result = dict(
      changed=False,
      original_message='',
      message=''
    )

    module = AnsibleModule(
      argument_spec=module_args,
      supports_check_mode=True
    )
		
    if module.check_mode:
      module.exit_json(**result)
    
    
    result['original_message']=net_me(module.params['commands'],module.params['first_host_ip'],module.params['first_host_usr'],module.params['first_host_pass'],module.params['sec_host_usr'],module.params['sec_host_pass'],module.params['sec_host_ip'])
              
    result['message']='Good Job'
    result['changed']=True      
    
    module.exit_json(**result)

def main():
    run_module()
				 				 
if __name__ == '__main__':
    main()
