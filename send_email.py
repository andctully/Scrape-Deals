import smtplib
import sys

SERVER = 'smtp.gmail.com'
PORT = 587

# 'SENDER' 'SENDER_PASSWORD' 'RECEIVER' 'SUBJECT' 'BODY'
args = sys.argv
sndr = args[1]
pswd = args[2]
rcvr = args[3]
subject = args[4]
body = args[5]

message = 'Subject: %s\n\n%s' % (subject, body)

mail = smtplib.SMTP(SERVER, PORT)

mail.ehlo()
mail.starttls()

mail.login(sndr, pswd)
mail.sendmail(sndr, rcvr, message)

mail.close()
