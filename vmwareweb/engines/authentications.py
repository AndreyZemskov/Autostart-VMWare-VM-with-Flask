""" engines/authentications """

from flask import Blueprint
import paramiko

auth_blueprints = Blueprint('auth', __name__)

"""
    Parameters of authentications
    which are located in mp.yaml file.
"""

def SSHClient(server, port, user, password):
    """ This function creating to connection. """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    print('Client was created')
    return client

def ssh_cli(client, command):
    """
        This function creating to secure tunnel
        across an SSH Transport.
    """
    channel = client.get_transport().open_session()
    channel.get_pty()
    channel.settimeout(5)
    channel.exec_command(command)
    print('Session was opened')
    print(channel.recv(1024))
    client.close()
    channel.close()