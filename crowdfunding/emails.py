from django.conf import settings
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string


def send_approval_request_email(campaign_name,campaign_id,subject, from_email, to):
    text_content = 'Campaign ' + campaign_name + ' has been created and is pending approval'
    html_content = '<p>Campaign ' + campaign_name + ' has been created and is pending approval</p><p>Click <a href="http://vlatest.otbafrica.com/admin/crowdfunding/campaign/' + str(
        campaign_id) + '/change/" target="_blank">here</a> to action on it.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    return msg.send()



def send_actioned_campaign_email(campaign_name,campaign_id,subject, from_email, to, status):
    text_content = 'Campaign ' + campaign_name + ' has been '+status
    html_content = '<p>Campaign ' + campaign_name + ' has been '+status+'</p><p>Click <a href="http://vlatest.otbafrica.com/crowdfunding/business/' + str(
        campaign_id) + '/" target="_blank">here</a> to view its comments.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    return msg.send()


def send_campaign_disbursement_email(campaign_name,campaign_id,subject, from_email, to, status):
    text_content = 'Campaign ' + campaign_name + ' has been closed and is pending approval for '+status
    html_content = '<p>Campaign ' + campaign_name + ' has been closed and is pending approval for '+status+'</p><p>Click <a href="http://vlatest.otbafrica.com/admin/crowdfunding/campaigndisbursement/' + str(
        campaign_id) + '/change/" target="_blank">here</a> to authorize '+status+'.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    return msg.send()
