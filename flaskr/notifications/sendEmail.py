import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage

# Adapted from send_email by Anthony Argatoff
# https://github.com/anthonyargatoff/furlong_co-op_scraping

def send_email(body:str, recipient:str):
    """
    Args:
        body (str): message body
        recipient (str): recipient
    """
    port = 587;
    smtp_server = "smtp.gmail.com";

    # email and app password for the gmail sending the emails.
    sender_email = "quakebot9000@gmail.com";
    password = 'lwdvrqlzofwlgfll';
    subject = "QuakeQuest Notification";


    #msg = MIMEText(body)
    #msg['Subject'] = subject
    #msg['From'] = sender_email
    #msg['To'] = ', '.join(recipient)

    #message = """\
    #From: %s
    #To: %s
    #Subject: %s

    #%s
    #""" % (sender_email, recipient, subject, body);

    #msg = EmailMessage()
    #msg['Subject'] = subject
    #msg['From'] = sender_email
    #msg['To'] = recipient
    #msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo();
            server.starttls();

            server.login(sender_email, password);
            server.sendmail(sender_email, recipient, body);
            server.quit();
    except Exception as error:
        print('Error:', error);
