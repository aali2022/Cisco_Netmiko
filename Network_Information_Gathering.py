import time
import pandas as pd
from getpass import getpass
import netmiko
import os.path
from datetime import datetime

#file_path = 'output/logs.log'
#sys.stderr = open(file_path, "w+")

def cisco_ios_func(ip, uname, pname):
    cisco_ios = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': uname,
        'password': pname,
    }
    ios_connect = netmiko.ConnectHandler(**cisco_ios)
    print ('Connectivity with '+(Host_Name)+' '+IPAddress+'...........................................[SUCCESS]')

    def inner_function (instruct):
        CISCO_COMMAND = ios_connect.send_command(instruct, use_textfsm=True)
        if (instruct == 'show cdp neighbors detail'):
           cdp_data = {'Device Hostname': Host_Name,
                       'Device IP Address': IPAddress,
                       'Device Local': [entry['local_port'] for entry in CISCO_COMMAND],
                       'Neighbor Hostname': [entry['destination_host'] for entry in CISCO_COMMAND],
                       'Neighbor MGMT IP': [entry['management_ip'] for entry in CISCO_COMMAND],
                       'Neighbor interface': [entry['remote_port'] for entry in CISCO_COMMAND],
                       'Neighbor Platform': [entry['platform'] for entry in CISCO_COMMAND]
                       }
           df = pd.DataFrame(cdp_data, columns=list(cdp_data.keys()))
           #print(df.head())
           if(os.path.isfile('output/'+instruct+'.csv')):
               df.to_csv('output/'+instruct+'.csv', mode='a', index= False,header=False)
               print ('Command '+instruct+' on '+Host_Name+' '+ IPAddress+'......................................[SUCCESS]')
           else:
               df.to_csv('output/'+instruct+'.csv', index= False)
               print ('Command '+instruct+' on '+Host_Name+' '+ IPAddress+'......................................[SUCCESS]')
        elif (instruct == 'show ip route vrf *'):
           routing_data = {'device hostname': Host_Name,
                       'device ip address': IPAddress,
                       'Protocol Type': [entry['protocol'] for entry in CISCO_COMMAND],
                       'Route': [entry['network'] for entry in CISCO_COMMAND],
                       'Subnet Mask': [entry['mask'] for entry in CISCO_COMMAND],
                       'distance': [entry['distance'] for entry in CISCO_COMMAND],
                       'metric': [entry['metric'] for entry in CISCO_COMMAND],
                       'nexthop_ip': [entry['nexthop_ip'] for entry in CISCO_COMMAND],
                       'nexthop_if': [entry['nexthop_if'] for entry in CISCO_COMMAND],
                       'uptime': [entry['uptime'] for entry in CISCO_COMMAND]
                       }
           df = pd.DataFrame(routing_data, columns=list(routing_data.keys()))
           #print(df.head())
           if(os.path.isfile('output/ip_routing_info.csv')):
               df.to_csv('output/ip_routing_info.csv', mode='a', index= False,header=False)
               print ('Command '+instruct+' on '+Host_Name+' '+ IPAddress+'......................................[SUCCESS]')
           else:
               df.to_csv('output/ip_routing_info.csv', index= False)
               print ('Command '+instruct+' on '+Host_Name+' '+ IPAddress+'......................................[SUCCESS]')
        elif (instruct == 'show version'):
           version_data = {'device hostname': [entry['hostname'] for entry in CISCO_COMMAND],
                       'device ip address': IPAddress,
                       'hardware Type': [entry['hardware'] for entry in CISCO_COMMAND],
                       'serial': [entry['serial'] for entry in CISCO_COMMAND],
                       'uptime': [entry['uptime'] for entry in CISCO_COMMAND]
                       }
           df = pd.DataFrame(version_data, columns=list(version_data.keys()))
           #print(df.head())
           if(os.path.isfile('output/'+instruct+'.csv')):
               df.to_csv('output/'+instruct+'.csv', mode='a', index= False,header=False)
               print ('Command '+instruct+' on '+Host_Name+' '+ IPAddress+'......................................[SUCCESS]')
           else:
               df.to_csv('output/'+instruct+'.csv', index= False)
               print ('Command '+instruct+' on '+Host_Name+' '+ IPAddress+'......................................[SUCCESS]')
        elif "Invalid" in CISCO_COMMAND:
            print ('Command '+instruct+' on '+Host_Name+' '+ IPAddress+' [FAIL]')
            print(instruct)
            print(CISCO_COMMAND)
        else:
            print (CISCO_COMMAND)
        time.sleep(1)
    return inner_function

Asset_List= pd.read_csv("csv/asset_list.csv")
USERNAME = input('Enter username:')
PASSWORD = getpass('Password:')

for row in range(len(Asset_List)) :
  Host_Name = Asset_List.loc[row, "hostname"]
  IPAddress = Asset_List.loc[row, "ip_address"]
  Device_type = Asset_List.loc[row, "device_type"]
  if (Device_type == 'cisco_ios'):
      try:
          call_cisco_ios_func = cisco_ios_func(IPAddress, USERNAME, PASSWORD)
      except Exception as e:
          print ('Connectivity with '+(Host_Name)+' '+IPAddress+'..............................................[FAIL]')
          print (e)
          continue
      call_cisco_ios_func('show ip route vrf *')
      call_cisco_ios_func('show cdp neighbors detail')
      call_cisco_ios_func('show version')
      call_cisco_ios_func('show ip interface | section exclude administratively')
  else:
      print ('Sorry the Device '+(Host_Name)+' '+IPAddress+'............................................[NOT SUPPORTED]')
