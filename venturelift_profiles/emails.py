from django.conf import settings
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string


def send_business_connect_request_email(business, investor, subject, from_email, to):
    text_content = 'Investor ' + investor + ' has requested connection to business '+business
    html_content = '<p>Investor ' + investor + ' has requested connection to business '+business+'</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    return msg.send()

