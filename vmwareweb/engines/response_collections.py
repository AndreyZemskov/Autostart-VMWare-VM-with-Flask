import time
import subprocess
from vmwareweb.models import ServerList, MailSettings, db
import re


collection_info = {}
last_check_time = []
host_cmd_vmid = {}
host_vrt = {}
vrt_unreachable = []
mail_info = {}

def initialization():

    """
        Function to fill stacks as { host_cmd_vmid, host_vrt }
    """

    for host, cmd, vmid in db.session.query(ServerList.vm_ip, ServerList.esx_version, ServerList.vm_clone):

        list_format_host = str(host)
        list_format_vmid = str(vmid)
        find_required_host = re.findall(r"\b\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}\b", list_format_host)
        search_match_cmd = re.search(r"[a-z]", cmd)
        find_required = re.findall(r"^\d{1,3}", list_format_vmid)
        host_cmd_vmid.update({find_required_host[0]: search_match_cmd.string + ' {}'.format(find_required[0])})

    for host_ip, vrt_ip in db.session.query(ServerList.hosts_ip, ServerList.vm_ip):

        list_format_host_ip = str(host_ip)
        list_format_vrt = str(vrt_ip)
        format_host_ip = re.findall(r"\b\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}\b", list_format_host_ip)
        format_host_vrt_ip = re.findall(r"\b\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}\b", list_format_vrt)
        host_vrt.update({format_host_vrt_ip[0]: format_host_ip[0]})


def collection():

    """
        This function is collected information about VMs
    """

    collection_info.clear()
    for host in db.session.query(ServerList.vm_ip):
        ls = str(host)
        format_host = re.findall(r"\b\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3}\b", ls)
        answer = subprocess.call(['ping', '-c', '3', format_host[0]])
        if answer == 0:
            collection_info.update({host[0]: 'Ok'})
            last_check = time.ctime(time.time())
            last_check_time.append(last_check)
        if answer == 1:
            collection_info.update({host[0]: 'Down'})



def check_mail():

    """
        This function is check mail server status
    """

    mail_ls = db.session.query(MailSettings.mail_server)
    mail_server = (str(mail_ls[0]).replace("('", "").replace("',)", ""))
    answer = subprocess.call(['ping', '-c', '3', mail_server])
    if answer == 0:
        mail_info.clear()
        mail_info.update({mail_server: 'Ok'})

    else:
        mail_info.clear()
        mail_info.update({mail_server: 'Down'})