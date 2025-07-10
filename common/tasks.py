from django.core.mail import message
from django.core.mail.message import EmailMessage

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import environ

# def SendEmail(subject,body,emailfrom,emailto, attachmentname="",attachment=""):
#     mail = EmailMessage(subject,body,emailfrom,[emailto])
#     if not attachment == "":
#         mail.attach(attachmentname,attachment,'application/pdf')
#     mail.content_subtype="html"
#     mail.send()

def SendEmail(subject,body,emailfrom,emailto, attachmentname="",attachment=""):
    message = Mail(
    from_email=emailfrom,
    to_emails=emailto,
    subject=subject,
    html_content=body)
    try:
        env = environ.Env()
        env.read_env()
        sg = SendGridAPIClient(env('EMAIL_HOST_PASSWORD_WEBAPI'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
