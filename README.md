# Autostart VMWare Virtual Machines.

This application is listening IPs and check avalability servers. If server is down will be sended a command to start copy VM on other ESX host. Before use this application you should install libraries from requirements.txt just type pip install -r requirements.txt

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

  - Create One;
  - Initialization;
  - Listening Servers;
  
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

Initialization is function which collect information about VMs and reter OK if VM available (have ping) and Down if host not available (haven't ping).

**Listening Servers**
___
This function listen IPs and check availability if servers down. Then after 45 seconds initialization will be respons to autostart copy VM on other host.

**SSH Conection**
___

For SSH connection with ESXI is use Paramico library, for setting connection you should written in **mp.yaml** file.  
mp.yaml file have next parameters:  
port: 22 (defolt)  
user: 'user' (should be your user)  
password 'password' (should be your password)  
mp.yaml file located on **/vmwareweb/engines/mp.yaml**

**Update**
___

Now this application has an ability to send an email and has next function:

  - Mail server settings;
  - Add recipient;
  - Check mail server (avalible or not);
  - Sends test email;
  
 ![alt text](https://github.com/AndreyZemskov/Autostart-VMWare-VM-with-Flask/blob/master/screens/Mail_Panel.PNG?raw=true)
 
 Mail server settings:
 ___
 
If you want to send an email you should specify mail server which will send email, for example smtp.gmail.com. Username its a name of a person who sends an email, for example example@gmail.com. Password field is for username password. You can choose one of two protocols (TLS/SSL) and specify the number of port.

![alt text](https://github.com/AndreyZemskov/Autostart-VMWare-VM-with-Flask/blob/master/screens/Mail_Settings.PNG?raw=true)
 
You can add recipient who will get message.
 
After email server settings you can check server availability - press Check mail server. If you need to check that your email sended use the function Sends test email.

There are 3 varietys:

  - alert() if one VM stops answer for ping;
  - successful_autostart() send message when one of copy VM will be start on other ESX Host;
  - bad_autostart() if VM cant autostart;
  
  **Logging**
___

Application has Logging function. File with entries will be create after application start. You can find file on root folder it named **application.log**

This project is in development, If you encounter errors please send me email.
