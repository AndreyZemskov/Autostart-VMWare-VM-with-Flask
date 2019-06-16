import threading
from vmwareweb.engines.engine import monitoring
from vmwareweb.engines.response_collections import collection, check_mail


def monitoring_start():

    """
        This function is separate flow and connected with monitoring() function
        which located vmwareweb/engines/response_collections.py

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

        and connected with collection() function which located vmwareweb/engines/response_collections.py

    """

    threading.Event()
    thread_collection = threading.Thread(target=collection)
    thread_collection.start()
    thread_collection.join()

def mail_start():

    """
        This function is send test email message and connected with check_mail function
        which located vmwareweb/engines/response_collections.py

    """

    threading.Event()
    thread_monitoring_start = threading.Thread(target=check_mail)
    thread_monitoring_start.start()
    thread_monitoring_start.join()