from django.template.loader import render_to_string
from XDOJ import settings
from utils.tools import get_dict, send_email_sync


def send_register_confirm_email(to_user, confirm_code):
    subject = 'XDOJ注册确认邮件'
    context = get_dict(username=to_user.username,
                       website_name=settings.WEBSITE_NAME,
                       confirm_minutes=settings.CONFIRM_MINUTES,
                       link=settings.WEBSITE_BASE_URL + 'account/confirm/register/?code=' + confirm_code)
    email_html = render_to_string('register_confirm_email.html', context)
    send_email_sync(subject=subject, content=email_html, to=[to_user.email])


def send_reset_password_email(to_user, reset_code):
    subject = 'XDOJ密码重置邮件'
    context = get_dict(username=to_user.username,
                       website_name=settings.WEBSITE_NAME,
                       confirm_minutes=settings.CONFIRM_MINUTES,
                       link=settings.WEBSITE_BASE_URL + 'account/confirm/reset_password/?code=' + reset_code)
    email_html = render_to_string('reset_password_email.html', context)
    send_email_sync(subject=subject, content=email_html, to=[to_user.email])

