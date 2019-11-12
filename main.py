#!/usr/bin/env python
import re
import os
from netmiko import Netmiko
from getpass import getpass

ipaddress = raw_input("Enter IP address or Hostname: ")
username = raw_input("Username: ")
path1 = raw_input("File path and name (example C:\\test\\testfile.bin): ")

cisco1 = {
    "host": ipaddress,
    "username": username,
    "password": getpass(),
    "device_type": "cisco_ios",
}

net_connect = Netmiko(**cisco1)
command1 = "show flash"
command2 = "show run | i hostname"
command3 = "show version | i image"

output1 = net_connect.send_command(command1)
output2 = net_connect.send_command(command2)
output3 = net_connect.send_command(command3)
net_connect.disconnect()

hostname=re.search("hostname\s(\S+)",output2)
results=re.search("\d+\sbytes\stotal\s[(](\d+)\sbytes\sfree[)]",output1)
image=re.search("\w.+\s.(.*[A-Za-z1-9])",output3)


print ("Hostname: "+hostname.group(1))
print ("Current Image: "+image.group(1))
print("Bytes Free: "+results.group(1))

#### Check size of new image and compare against free space.

##path = r'C:\Users\richa\Downloads\c2691-adventerprisek9-mz.124-25c.bin' #Not used replaced with path1
newfilesize = os.path.getsize(path1)

print ("r""'"+path1+"'")

if results.group(1) > newfilesize:
    print ("We have Space")
else:
    print ("We dont have enough Space")
#future revisions will copy the file, set the boot path and show final config.