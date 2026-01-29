from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from bran import settings
from bran.base.models import SendEmail
from bran.quotes.forms import QuoteForm
from bran.users.utils.tokens import account_activation_token
from bran.settings import EMAIL_HOST_USER, CURRENT_DOMAIN


def send_mail(subject, message, to, from_email=None, message_to_save=None, attachments=None, html=True,
              fail_silently=False):
    if not isinstance(to, (list, tuple)):
        to = [to]

    from_email = from_email or settings.EMAIL_HOST_USER

    msg = EmailMessage(subject=subject, body=message, to=to, from_email=from_email)

    if html:
        msg.content_subtype = 'html'

    if attachments:
        for attachment in attachments:
            msg.attach_file(attachment)

    is_sent = msg.send(fail_silently=fail_silently)

    if message_to_save:
        SendEmail.objects.create(
            email_from=from_email,
            email_to=', '.join(to),
            subject=subject,
            message=message_to_save,
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

    send_mail(subject, html_content, EMAIL_HOST_USER, from_email=email, message_to_save=message)


def email_get_quote(form_data, formset_data, distance, vehicle_name=None, price=None, price_vat=None):
    subject = 'Quote Request'
    html_content = (
        get_template('emails/get_a_quote_email.html').render(
            {
                'form_data': form_data,
                'formset_data': formset_data,
                'distance': distance,
                'vehicle_name': vehicle_name,
                'price': price,
                'price_vat': price_vat
            }
        )
    )

    send_mail(subject, html_content, EMAIL_HOST_USER, from_email=form_data.get('email'),
              message_to_save=f'Quote request from {form_data["email"]}')


def email_automatic_answer(email):
    subject = 'We’ll Get Back to You Soon!'
    html_content = (
        get_template('emails/automatic_email.html').render({})
    )

    send_mail(subject, html_content, email, from_email=f'Bran Logistics <{EMAIL_HOST_USER}>')


def email_calculator_to_admin(quote_data):
    subject = 'Calculator has been used'
    html_content = (
        get_template('emails/calculator_to_admin_email.html').render({
            'quote_data': quote_data,
        })
    )

    send_mail(subject, html_content, EMAIL_HOST_USER, from_email=EMAIL_HOST_USER)
