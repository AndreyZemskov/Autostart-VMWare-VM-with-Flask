import re
from vmwareweb import mail, app, dinamic_mail_setting
from flask_mail import Message
from flask import Blueprint
from vmwareweb.engines.response_collections import vrt_unreachable
from vmwareweb.models import RecipientsPost, db
from vmwareweb.models import MailSettings
from flask import flash
import time
import smtplib
import logging

send_email_blueprints = Blueprint('send_email', __name__)


def send_mail(subject, sender, recipients):

    """
        This function is simple Send Mail Framework

    """

    msg = Message(subject, sender=sender, recipients=recipients)
    # msg.body = html_body
    try:
        dinamic_mail_setting()
        mail.init_app(app)
        mail.send(msg)

    except smtplib.SMTPRecipientsRefused:
        print('smtplib.SMTPRecipientsRefused')
        logging.info("!!! Connection Refused !!!{}".format(time.strftime("%d.%m.%y %H:%M")))


def alert():

    """
        This function sends alert on your email from recipients list if monitiring() (/vmwareweb/engine)
        if one VM stops answer for ping

    """

    with app.app_context():
        recipients_list = []
        mail = db.session.query(MailSettings.mail_server)
        mail_server = re.search('[a-zA-Z]', str(mail[0][0])).string

        for recipient in db.session.query(RecipientsPost.recipients):
            recipients_search = re.search(r"[a-zA-Z]", str(recipient[0]))
            recipients_list.append(recipients_search.string)

        for unreachable in vrt_unreachable:
            for rec in recipients_list:
                send_mail(' !!! ALERT !!! VM {} is unreachable'.format(unreachable), '{}'.format(mail_server),
                          ['{}'.format(rec)])
                logging.info("!!! Alert VM is unreachable {} !!!".format(time.strftime("%d.%m.%y %H:%M")))


def successful_autostart():

    """
        This function will be send Successful Autostar message when one of copy VM will be start on other ESX Host

    """

    with app.app_context():
        recipients_list = []
        mail = db.session.query(MailSettings.mail_server)
        mail_server = re.search('[a-zA-Z]', str(mail[0][0])).string

        for recipient in db.session.query(RecipientsPost.recipients):
            recipients_search = re.search(r"[a-zA-Z]", str(recipient[0]))
            recipients_list.append(recipients_search.string)

        for unreachable in vrt_unreachable:
            for rec in recipients_list:
                send_mail(' !! Successful Autostar !! {} is autostart'.format(unreachable), '{}'.format(mail_server),
                          ['{}'.format(rec)])
                logging.info("!!! Successful Autostart !!! {}".format(time.strftime("%d.%m.%y %H:%M")))


def bad_autostart():

    """
        This function will be send Bad Connection message if VM cant autostart
    """

    with app.app_context():
        recipients_list = []
        mail = db.session.query(MailSettings.mail_server)
        mail_server = re.search('[a-zA-Z]', str(mail[0][0])).string

        for recipient in db.session.query(RecipientsPost.recipients):
            recipients_search = re.search(r"[a-zA-Z]", str(recipient[0]))
            recipients_list.append(recipients_search.string)

        for unreachable in vrt_unreachable:
            for rec in recipients_list:
                send_mail('!!! Bad Connection !!! VM {} cant autostart due to connection error'.format(unreachable),
                          '{}'.format(mail_server), ['{}'.format(rec)])
                logging.info("!!! Bad Autostart !!! {}".format(time.strftime("%d.%m.%y %H:%M")))


def mail_test():
    with app.app_context():
        recipients_list = []
        mail = db.session.query(MailSettings.mail_server)
        mail_server = re.search('[a-zA-Z]', str(mail[0][0])).string

        for recipient in db.session.query(RecipientsPost.recipients):
            recipients_search = re.search(r"[a-zA-Z]", str(recipient[0]))
            recipients_list.append(recipients_search.string)

        if not recipients_list:
            flash('Not recipient', 'not_recipient')
            logging.info("!!! Send Message When Havent Recipients {} !!!".format(time.strftime("%d.%m.%y %H:%M")))

        for rec in recipients_list:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", rec):
                flash('Not recipient or bad email address', 'not_recipient')
                logging.info("!!! Bad Address {} !!!".format(time.strftime("%d.%m.%y %H:%M")))

            else:
                flash('Message was sended', 'test')
                send_mail('Mail Test is Pass', '{}'.format(mail_server), ['{}'.format(rec)])
                logging.info("!!! Test Message Send {} !!!".format(time.strftime("%d.%m.%y %H:%M")))
