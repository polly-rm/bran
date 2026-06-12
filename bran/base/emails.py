from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

from bran.base.models import SendEmail
from bran.users.utils.tokens import account_activation_token


# -------------------------
# CORE EMAIL SENDER
# -------------------------
def send_mail(
        subject,
        message,
        to,
        from_email=None,
        message_to_save=None,
        attachments=None,
        html=True,
        fail_silently=False,
):
    if not isinstance(to, (list, tuple)):
        to = [to]

    # FIX: always use real sender email, NEVER SMTP username
    from_email = from_email or settings.DEFAULT_FROM_EMAIL

    msg = EmailMessage(
        subject=subject,
        body=message,
        to=to,
        from_email=from_email,
    )

    if html:
        msg.content_subtype = "html"

    if attachments:
        for attachment in attachments:
            msg.attach_file(attachment)

    is_sent = msg.send(fail_silently=fail_silently)

    if message_to_save:
        SendEmail.objects.create(
            email_from=from_email,
            email_to=", ".join(to),
            subject=subject,
            message=message_to_save,
            is_sent=is_sent,
        )

    return is_sent


# -------------------------
# ACCOUNT ACTIVATION
# -------------------------
def email_account_activation(user, request):
    subject = "Account Activation"

    html_content = get_template(
        "emails/users/register_verification.html"
    ).render(
        {
            "user": user.email,
            "domain": settings.CURRENT_DOMAIN,
            "request": request,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        }
    )

    send_mail(
        subject,
        html_content,
        user.email,
        from_email=settings.DEFAULT_FROM_EMAIL,
    )


# -------------------------
# CONTACT US
# -------------------------
def email_contact_us(name, email, title, message):
    subject = title

    html_content = get_template(
        "emails/contact_us_email.html"
    ).render(
        {
            "name": name,
            "email": email,
            "message": message,
        }
    )

    send_mail(
        subject,
        html_content,
        settings.DEFAULT_FROM_EMAIL,
        from_email=email,
        message_to_save=message,
    )


# -------------------------
# QUOTE EMAIL
# -------------------------
def email_get_quote(form_data, formset_data, distance, vehicle_name=None, price=None, price_vat=None):
    subject = "Quote Request"

    html_content = get_template(
        "emails/get_a_quote_email.html"
    ).render(
        {
            "form_data": form_data,
            "formset_data": formset_data,
            "distance": distance,
            "vehicle_name": vehicle_name,
            "price": price,
            "price_vat": price_vat,
        }
    )

    send_mail(
        subject,
        html_content,
        settings.DEFAULT_FROM_EMAIL,
        from_email=form_data.get("email"),
        message_to_save=f'Quote request from {form_data["email"]}',
    )


# -------------------------
# AUTO REPLY
# -------------------------
def email_automatic_answer(email):
    subject = "We'll Get Back to You Soon!"

    html_content = get_template(
        "emails/automatic_email.html"
    ).render({})

    send_mail(
        subject,
        html_content,
        email,
        from_email=settings.DEFAULT_FROM_EMAIL,
    )


# -------------------------
# ADMIN CALCULATOR EMAIL
# -------------------------
def email_calculator_to_admin(quote_data):
    subject = "Calculator has been used"

    html_content = get_template(
        "emails/calculator_to_admin_email.html"
    ).render(
        {
            "quote_data": quote_data,
        }
    )

    send_mail(
        subject,
        html_content,
        settings.DEFAULT_FROM_EMAIL,
        from_email=settings.DEFAULT_FROM_EMAIL,
    )
