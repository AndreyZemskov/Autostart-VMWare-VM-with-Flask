""" engines/engine """

import os
import threading
import subprocess
from vmwareweb.models import ServerList, db
from vmwareweb.engines.authentications import SSHClient, ssh_cli
import time
import yaml

collection_info = {}
last_check_time = []
host_cmd_vmid = {}
host_vrt = {}

yaml_dir = os.path.abspath(os.path.dirname(__file__))
stream = open(os.path.join(yaml_dir, 'mp.yaml'))

mp = yaml.load(stream, Loader=yaml.FullLoader)
port = mp['port']
user = mp['user']
password = mp['password']

esx_list = [('vim-cmd vmsvc/power.on', 'ESX67')]

def monitoring_start():

    """
        This function is separate flow and connected with monitoring() function.

    """

    threading.Event()
    thread_monitoring_start = threading.Thread(target=monitoring)
    thread_monitoring_start.start()
    thread_monitoring_start.join()


def collection_start():

    """
        This function is collected information about servers with next parameters:

                   - Server IP
                   - Server Status
                   - Last Check

        and connected with collection function

    """

    threading.Event()
    thread_collection = threading.Thread(target=collection)
    thread_collection.start()
    thread_collection.join()


def initialization():

    """
        Function to fill stacks as { host_cmd_vmid, host_vrt }
    """

    for host, cmd, vmid in db.session.query(ServerList.vm_ip, ServerList.esx_version, ServerList.vm_clone):
        format_host = (str(host).replace('"', '').replace('(', "").replace(")", "").replace(',', '').replace("'", ''))
        format_cmd = (str(cmd).replace('"', '').replace('(', "").replace(")", "").replace(',', '').replace("'", ''))
        format_vmid = (str(vmid).replace('"', '').replace('(', "").replace(")", "").replace(',', '').replace("'", ''))
        host_cmd_vmid.update({format_host: format_cmd + ' {}'.format(format_vmid)})

    for host_ip, vrt_ip in db.session.query(ServerList.hosts_ip, ServerList.vm_ip):
        format_host_ip = (str(host_ip).replace('"', '').replace('(', "").replace(")", "").replace(',', '').replace("'", ''))
        format_vrt_ip = (str(vrt_ip).replace('"', '').replace('(', "").replace(")", "").replace(',', '').replace("'", ''))
        host_vrt.update({format_vrt_ip: format_host_ip})

def monitoring():

    """
        This function is listen IPs and will be check availability servers if server down then
        will be initialization response to auto start copy VM on other host and will be call SSH Client function

    """
    count = 0
    initialization()
    while True:
        try:
            for vrt, host in host_vrt.items():
                answer = subprocess.call(['ping', '-c', '3', vrt])
                if answer == 1:
                    time.sleep(5)
                    collection()
                    count += 1
                    if count >= 3:
                        for vm, cmd in host_cmd_vmid.items():
                            if vm == vrt:
                                ssh_cli(SSHClient(host, port, user, password), cmd)
                                count = 0
                    else:
                        continue

        except TimeoutError:
            print('Connection timed out')
            continue


def collection():

    """
        This function is collected information about VMs
    """

    response = str(db.session.query(ServerList.vm_ip.label('vm_ip')).all()).replace("[('", '').replace("',),", '').replace("('",'').replace("',)]", '').split()
    for vrt in response:
        answer = subprocess.call(['ping', '-c', '3', vrt])
        if answer == 0:
            collection_info.update({vrt: 'Ok'})
            last_check = time.ctime(time.time())
            last_check_time.append(last_check)
        if answer == 1:
            collection_info.update({vrt: 'Down'})