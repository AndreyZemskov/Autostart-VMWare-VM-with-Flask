from vmwareweb.models import MailSettings, db
from simplecrypt import decrypt

mail = db.session.query(MailSettings.mail_server)
username = db.session.query(MailSettings.username)
password = db.session.query(MailSettings.password)
protocol = db.session.query(MailSettings.protocol)
port = db.session.query(MailSettings.port)


mail_server = (str(mail[0]).replace("('", "").replace("',)", ""))
mail_port = int(str(port[0]).replace("(", "").replace(",)", ""))
mail_ssl = bool(str(protocol[0]).replace("('", "").replace("',)", ""))
mail_username = (str(username[0]).replace("('", "").replace("',)", ""))
mail_password = password[0]

protocol_view = protocol[0][0][5:]
pas = mail_password[0]
sd = str(decrypt('password', pas)).replace("b'", "").replace("'", "")












