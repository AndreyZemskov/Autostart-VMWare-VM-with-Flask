from vmwareweb import mail, app, install_mail
from flask_mail import Message
from flask import Blueprint
from vmwareweb.engines.response_collections import vrt_unreachable
from vmwareweb.models import RecipientsPost, db
from vmwareweb.settings_email import mail_server

send_email_blueprints = Blueprint('send_email', __name__)


def send_mail(subject, sender, recipients):

    """
        This function is simple Send Mail Framework

    """

    msg = Message(subject, sender=sender, recipients=recipients)
    # msg.body = html_body
    install_mail()
    mail.init_app(app)
    mail.send(msg)


def alert():

    """
        This function sends alert on your email from recipients list if monitiring() (/vmwareweb/engine)
        if one VM stops answer for ping

    """
    with app.app_context():
        recipients_list = []
        recipients_get = db.session.query(RecipientsPost.recipients)
        mail_format = (str(recipients_get[0:]).replace("[('", "").replace("',)]", ""))
        mail_recipients = mail_format.replace(",", "").replace("('", "").replace("]", "").replace("['", "").replace(
            "')", "").split()

        for recipient in mail_recipients:
            recipients_list.append(recipient)

        for unreachable in vrt_unreachable:
            for rec in recipients_list:
                send_mail(' !!! ALERT !!! VM {} is down'.format(unreachable), '{}'.format(mail_server), ['{}'.format(rec)])

def successful_autostart():

    """
        This function will be send Successful Autostar message when one of copy VM will be start on other ESX Host

    """

    with app.app_context():
        recipients_list = []
        recipients_get = db.session.query(RecipientsPost.recipients)
        mail_format = (str(recipients_get[0:]).replace("[('", "").replace("',)]", ""))
        mail_recipients = mail_format.replace(",", "").replace("('", "").replace("]", "").replace("['", "").replace(
            "')", "").split()

        for recipient in mail_recipients:
            recipients_list.append(recipient)

        for unreachable in vrt_unreachable:
            for rec in recipients_list:
                send_mail(' !! Successful Autostar !! {} is autostart'.format(unreachable), '{}'.format(mail_server), ['{}'.format(rec)])

def bad_autostart():

    """
        This function will be send Bad Connection message if VM cant autostart

    """


    with app.app_context():
        recipients_list = []
        recipients_get = db.session.query(RecipientsPost.recipients)
        mail_format = (str(recipients_get[0:]).replace("[('", "").replace("',)]", ""))
        mail_recipients = mail_format.replace(",", "").replace("('", "").replace("]", "").replace("['", "").replace(
            "')", "").split()

        for recipient in mail_recipients:
            recipients_list.append(recipient)

        for unreachable in vrt_unreachable:
            for rec in recipients_list:
                send_mail('!!! Bad Connection !!! VM {} cant autostart due to connection error'.format(unreachable), '{}'.format(mail_server), ['{}'.format(rec)])


def mail_test():

    """
        This function will be send just test message

    """

    with app.app_context():
        recipients_list = []
        recipients_get = db.session.query(RecipientsPost.recipients)
        mail_format = (str(recipients_get[0:]).replace("[('", "").replace("',)]", ""))
        mail_recipients = mail_format.replace(",", "").replace("('", "").replace("]", "").replace("['", "").replace(
            "')", "").split()

        for recipient in mail_recipients:
            recipients_list.append(recipient)
            for rec in recipients_list:
                send_mail('Mail Test is Pass', '{}'.format(mail_server), ['{}'.format(rec)])
