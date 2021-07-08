import smtplib, ssl, getpass

port = 465  # For SSL

sender_email = "testingthetest22@gmail.com"
email_password = "yav48A34Agfavr;Ahve09a[3ma99qjp7p"

receiver_email = "tintin10q@hotmail.com"

message = """\
Subject: Testing emails

Hi, how are you! Don't mind me I am just testing emails here

Your truly,
- probaly a python script
"""

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, email_password)
    # TODO: Send email here
    server.sendmail(sender_email, receiver_email, message)
