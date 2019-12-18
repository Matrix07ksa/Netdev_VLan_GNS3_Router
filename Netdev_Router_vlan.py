#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Code By hejab Zaeri
import asyncio
import netdev
import re # Filter 
import os, time, sys ,socket
from termcolor import colored # Color 
from prettytable import PrettyTable 
from getpass import getpass
import logging         # Dbbuging Login 

try :
    os.mkdir("output_file") # mkdir Dir 
except : 
    pass
os.chdir("output_file") # cd output_file


USER = "admin"#input("Username Roter: ") # Your 
PASSWORD = "admin"#getpass(prompt='Password: ', stream=None)  # Your Password
netdev.logger.setLevel(logging.INFO)
logging.basicConfig(filename="hejab_Net.log",level=netdev.logger.setLevel(logging.DEBUG))
Switches_IP=["20.20.20.1","10.1.1.1","20.20.20.5"]# List ip Login 
Table3 = PrettyTable([colored('Device IP Login ' , 'magenta', attrs=['bold'])])
Table3.add_row([Switches_IP])
Table = PrettyTable([colored('Device Name ' ,'magenta', attrs=['bold']),'IP adress ','Stauts'," Username","Password"])#Device Name
Table1 = PrettyTable(["IP Address"])
Table2 = PrettyTable(["الأ جهزة المتصلة "])


class Connation():
    def __init__(self):       
        try:
            start = time.time() # start Time Programing 

            socket.inet_aton(Switches_IP[0]) #  chack ip 20.20.20.1
            socket.inet_aton(Switches_IP[1]) # chack ip  10.1.1.1
            socket.inet_aton(Switches_IP[2]) # chack ip  20.20.20.5
            # Config  Conitastion Device
            IP = { 'username' : USER,'password' : PASSWORD,'device_type': 'cisco_ios','host':   Switches_IP[1]}
            IP1 = { 'username' : USER,'password' : PASSWORD,'device_type': 'cisco_ios','host': Switches_IP[0]}
            IP2 = { 'username' : USER,'password' : PASSWORD,'device_type': 'cisco_ios','host': Switches_IP[2]} 
        except socket.error:
            print ("Invalid IP address  " + Switches_IP)
        except ConnectionRefusedError :
            print("Login Fild ")
        except ConnectionRefusedError:
            print("Login Fild")

        
                
        

        
        async def Router1() :
            async with netdev.create(**IP) as ios:
                ## 10.1.1.1 Router 
                
                
                # up ip int
                # Filter IP 
                edit_up = await ios.send_command("show ip interface b | section exclude (unassigned|down|IP-Address)")
                edit_up = re.sub(r'\s+\s+\D+\s+',' ',str(edit_up))
                edit_up =re.split("\s+", edit_up)
                global ip , start

                ip , start = lambda x : "ip address " + x , "no sh" # ip address Your netmask start 
                dhcp = lambda name,ip,mask : ["ip dhcp pool "+str(name),"network "+str(ip)+" "+str(mask),"default-router "+str(ip)] # Creat Dhcp
                dhcp1,dhcp2=dhcp("ali","30.30.30.1","255.255.255.0"),dhcp("hejab","40.40.40.1","255.255.255.0")
                dhcp = await ios.send_config_set(dhcp1) # send Router 
                dhcp = await ios.send_config_set(dhcp2)            
                arp_chack =  await ios.send_command("show arp | section exclude (Address|-)") # show arp ip addsress 
                hostname = await ios.send_command("show run | inc hostname")
                admin_h = await ios.send_command("show running-config | section include (username) ")
                admin = await ios.send_config_set(["int f0/1",
                                                   "no sh",
                                                   "int f0/1.1",
                                                   "encapsulation dot1Q 3",
                                                   ip("30.30.30.1 255.255.255.0"),
                                                   start,
                                                   "int f0/1.2",
                                                   ip("40.40.40.1 255.255.255.0"),
                                                   "encapsulation dot1Q 4",
                                                   "int loop 1",
                                                   ip("4.4.4.4 255.255.255.0"),
                                                   start
                                                   ])####### Send Router list
                admin_h = re.split("username|privilege|password|secret|\d+",admin_h) # filter username password 
                password = admin_h[5].split(" ")[1]
                hostname = hostname[9:] # Filter Hostname
                admin = admin_h[1].split(" ")[1]

                hostname.split(" ")
                print (hostname, end='') ,print(colored("  Done","yellow"))
        
                Table.add_row([hostname,Switches_IP[1], "Done",admin,password])
                for i in edit_up:
                        Table1.add_row([i])
                Table2.add_row([arp_chack])
                output = await ios.send_command("show run")
         
                f = open((hostname), "w")
                print((output), file=f)  # Save Output Router 

        async def Sw1():
            try :
                
                async with netdev.create(**IP1)as ios:
                    edit_up = await ios.send_command("show ip interface b | section exclude (unassigned|down|IP-Address)")
                    edit_up = re.sub(r'\s+\s+\D+\s+',' ',str(edit_up))
                    edit_up = re.split("\s+", edit_up)
                    arp_chack =  await ios.send_command("show arp | section exclude (Address|-)")
                    names = ["Ali_net","hejab_net","cloud_net","ahmad_net"]
                    for vlan in range(2,4+1):
                        for name in names :
                            await ios.send_config_set([f"vlan {vlan}",f"name {name}"])                    
                            print(f" Crate Vlan{vlan} ")
                            #### Create Vlan Database Sw1 
                    hostname = await ios.send_command("show run | inc hostname")
                    admin_h = await ios.send_command("show running-config | section include (username) ") # show configuration ram 
                    admin_1 = await ios.send_config_set(["int g0/0",
                                                         "switchport mode trunk ",
                                                         "switchport trunk encapsulation dot1q",
                                                         "vlan 3",
                                                         "name hejab_NET1",
                                                         "vlan 4",
                                                         "name Ali_net",
                                                         "int range g0/2 - 3",
                                                         "switchport access vlan 3 ",
                                                         "int g1/0",
                                                         "switchport access vlan 3",
                                                         "int range g1/1-3",
                                                         "switchport access vlan 4",
                                                         "int g2/0",
                                                         "switchport trunk encapsulation dot1q"
                                                         "switchport mode trank"
                                                         "vtp doamin hejab.com"
                                                           ])  
                    admin_1 = await ios.send_config_set(["int g0/0",
                                                         "switchport trunk encapsulation dot1q",
                                                         "switchport mode trunk",
                                                         "vtp domain hejab.com"
                                                         "int range g0/1-3",
                                                         "switchport access vlan 3",
                                                         "int range g1/0-3",
                                                         "switchport access vlan 3"])     
   
                    admin_h = re.split("username|privilege|password|secret|\d+",admin_h)
                    password = admin_h[5].split(" ")[1]
                    hostname = hostname[9:]
                    admin = admin_h[1].split(" ")[1]
                    edit_ip = [i for i in edit_up]
                    hostname.split(" ")
                    print (hostname, end='') ,print(colored("  Done","yellow"))
                
                    Table.add_row([hostname,Switches_IP[0], "Done",admin,password])
                    for i in edit_up:
                        Table1.add_row([i])
                    Table2.add_row([arp_chack])
                    output = await ios.send_command("show run")
                    f = open((hostname), "w")
                    print((output), file=f)  # python 3

            except OSError:
                print(f"Login Fild {Switches_IP[0]}")
        async def Sw2():
            try :
                async with netdev.create(**IP2)as ios:
                    edit_up = await ios.send_command("show ip interface b | section exclude (unassigned|down|IP-Address)")
                    edit_up = re.sub(r'\s+\s+\D+\s+',' ',str(edit_up))
                    edit_up = re.split("\s+", edit_up)
                    arp_chack =  await ios.send_command("show arp | section exclude (Address|-)")
                    hostname = await ios.send_command("show run | inc hostname")
                    admin_h = await ios.send_command("show running-config | section include (username) ") # show configuration ram 
  
                    Conf_ter = await ios.send_config_set(["int g0/0",
                                                         "switchport trunk encapsulation dot1q",
                                                         "switchport mode trunk",
                                                         "vtp domain hejab.com"
                                                         "int range g0/1-3",
                                                         "switchport access vlan 3",
                                                         "int range g1/0-3",
                                                         "switchport access vlan 3"])     
   
                    admin_h = re.split("username|privilege|password|secret|\d+",admin_h)
                    password = admin_h[5].split(" ")[1]
                    hostname = hostname[9:]
                    admin = admin_h[1].split(" ")[1]
                    edit_ip = [i for i in edit_up]
                    hostname.split(" ")
                    print (hostname, end='') ,print(colored("  Done","yellow"))
                
                    Table.add_row([hostname,Switches_IP[2], "Done",admin,password])
                    for i in edit_up:
                        Table1.add_row([i])
                    Table2.add_row([arp_chack])
                    output = await ios.send_command("show run")
                    f = open((hostname), "w")
                    print((output), file=f)  # python 3

            except OSError:
                print(f"Login Fild {Switches_IP[0]}")
            
        async def run_connations():
            
            await asyncio.wait([Router1()])
            await asyncio.wait([Sw1()])
            await asyncio.wait([Sw2()])
        loop = asyncio.get_event_loop()
        loop.run_until_complete( run_connations())
        
        end = time.time()
        total = int(end - start)
            
        t1= colored('\n حساب الوقت: ' , 'white')#Elapsd Time
        t2=(str(total) + " ثانية\n")#Sec
        t3=colored(t2,'green')        
        print(t1+t3)
            
        print(Table.get_string(title=colored("Hejab_zaeri_Network","red"))) # Get Tables print output 
        print(Table1.get_string(title=colored("عناوين المنافذ","red")))
        print("\n"+Table2.get_string(title=colored("Chack_ARP","red")))
        with open("hejab.html","a") as html_out :
            html_out.write("\n"+Table1.get_html_string()
                           +'\n'+
                           "\n"+
                           Table2.get_html_string()# Output Html File 
                           )
            
            

        sys.exit(1)

if __name__ == '__main__':
    Connation()
