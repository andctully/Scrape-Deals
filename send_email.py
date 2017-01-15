import smtplib
import sys

SERVER = 'smtp.gmail.com'
PORT = 587

SENDER = 'pythontestbot@gmail.com' # email address of bot sending
PASSWORD = '120southstreet'

# 'SENDER' 'SENDER_PASSWORD' 'RECEIVER' 'SUBJECT' 'BODY'
args = sys.argv
sndr = args[1]
pswd = args[2]
rcvr = args[3]
sbjct = args[4]
body = args[5]

message = 'Subject: %s\n\n%s' % (subject, body)

mail = smtplib.SMTP(SERVER, PORT)

mail.ehlo()
mail.starttls()

mail.login(sndr, pswd)
mail.sendmail(sndr, rcvr, message)

mail.close()
