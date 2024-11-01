from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from bran.base.models import SendEmail
from bran.users.utils.tokens import account_activation_token
from bran.settings import EMAIL_HOST_USER, CURRENT_DOMAIN


def send_mail(subject, message, to, from_email=None, attachments=None, html=True, fail_silently=False):
    if not isinstance(to, (list, tuple)):
        to = [to]

    msg = EmailMessage(subject=subject, body=message, to=to, from_email=from_email)

    if html:
        msg.content_subtype = 'html'

    if attachments:
        for attachment in attachments:
            msg.attach_file(attachment)

    is_sent = msg.send(fail_silently=fail_silently)

    SendEmail.objects.create(
        email_from=from_email,
        email_to=', '.join(to),
        subject=subject,
        message=message,
        is_sent=is_sent
    )

    return is_sent


def email_account_activation(user, request):
    subject = 'Account Activation'
    html_content = (
        get_template('emails/users/register_verification.html').render(
            {
                'user': user.email,
                'domain': CURRENT_DOMAIN,
                'request': request,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
        )
    )

    send_mail(subject, html_content, user.email, EMAIL_HOST_USER)


def email_contact_us(name, email, title, message):
    subject = title
    html_content = (
        get_template('emails/contact_us_email.html').render(
            {
                'name': name,
                'email': email,
                'message': message
            }
        )
    )

    # TODO: Update the email that we should send it from
    send_mail(subject, html_content, EMAIL_HOST_USER, EMAIL_HOST_USER)
