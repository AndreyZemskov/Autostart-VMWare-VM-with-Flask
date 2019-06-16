""" engines/engine """

import os
import subprocess
from vmwareweb.engines.authentications import SSHClient, ssh_cli
from vmwareweb.engines.response_collections import host_cmd_vmid, host_vrt, collection, initialization, vrt_unreachable
from vmwareweb import app
from vmwareweb.engines.send_email import alert, successful_autostart, bad_autostart
import paramiko
import time
import yaml


yaml_dir = os.path.abspath(os.path.dirname(__file__))
stream = open(os.path.join(yaml_dir, 'mp.yaml'))

mp = yaml.load(stream, Loader=yaml.FullLoader)
port = mp['port']
user = mp['user']
password = mp['password']

esx_list = [('vim-cmd vmsvc/power.on', 'ESX67')]
protocol_list = [('True SSL', 'SSL'), ('True TLS', 'TLS')]


def monitoring():

    """
        This function is listen IPs and will be check availability servers if server down then
        will be initialization response to auto start copy VM on other host and will be call SSH Client function

    """
    try_connect = 0
    initialization()
    while True:
        try:
            for vrt, host in host_vrt.items():
                answer = subprocess.call(['ping', '-c', '3', vrt])
                if answer != 0:
                    collection()
                    time.sleep(15)
                    try_connect += 1
                    if try_connect == 2:
                        vrt_unreachable.append(vrt)
                        with app.app_context():
                            alert()
                    if try_connect >= 3:
                        for vm, cmd in host_cmd_vmid.items():
                            if vm == vrt:
                                ssh_cli(SSHClient(host, port, user, password), cmd)
                                try_connect = 0
                                successful_autostart()


                    else:
                        continue

        except TimeoutError:
            print('Connection timed out')

        except paramiko.ssh_exception.NoValidConnectionsError:
            print('NoValidConnectionsError')
            bad_autostart()



