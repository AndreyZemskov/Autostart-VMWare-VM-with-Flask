# Autostart VMWare Virtual Machines.

This application is listening IPs and check avalability servers. If server is down will be sended a command to start copy VM on other ESX host.

Web application have two default accounts:
  - admin (have access to create and initialization VM on database. Defolt password admin)
  - root (have access to administration panel and can create, delete and change values on DB and wab application. Defolt password root)

Password can be changed on account menu.

![alt text](https://github.com/AndreyZemskov/Autostart-VMWare-VM-with-Flask/blob/master/screens/Menu.PNG?raw=true)
![alt text](https://github.com/AndreyZemskov/Autostart-VMWare-VM-with-Flask/blob/master/screens/Account.PNG?raw=true)


Dashboard on start page with function check available servers
___

![alt text](https://github.com/AndreyZemskov/Autostart-VMWare-VM-with-Flask/blob/master/screens/Dashbord.PNG?raw=true)


Managment have next function:

  - Create One
  - Initialization
  - Listening Servers
  
![alt text](https://github.com/AndreyZemskov/Autostart-VMWare-VM-with-Flask/blob/master/screens/Managment.PNG?raw=true)
  
The function Create One is create group to monitoring  
___
**VM IP** field should be specified IP VM which need monitoring  
**Host IP** field should be specified ESX host IP where located virtual machine copy which monitoring  
**ESX Version** field should be choose ESXI host version (just now only 67)  
**VM ID** is number of virtual machine wich can see after type command **vim-cmd vmsvc/getallvms**  

![alt text](https://github.com/AndreyZemskov/Autostart-VMWare-VM-with-Flask/blob/master/screens/Create_One.PNG?raw=true)

**Initialization**
___

Initialization is function which collect information about VMs and reter OK if VM available (have ping) and Down if host not available (haven't ping)  

**Listening Servers**
___
This function listen IPs and check availability if servers down. Then after 45 seconds initialization will be respons to autostart copy VM on other host

