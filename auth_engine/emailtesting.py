from smtplib import SMTP

domain = "localhost:1025"

with SMTP(domain) as smtp:
     result = smtp.noop()
     smtp.sendmail("tset@localhost:1025", ["test2@localhost:1025"], "Hi there!")
