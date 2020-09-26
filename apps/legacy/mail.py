from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_import_token


def create_legacy_account_email(profile):
    mail_subject = "Transfer your old account"
    message = render_to_string(
        "legacy/mail_import.html",
        {
            "name": profile.user.first_name,
            "uid": urlsafe_base64_encode(force_bytes(profile.user.username)),
            "token": account_import_token.make_token(profile.user),
        },
    )
    email = EmailMessage(mail_subject, message, from_email="noreply@cosmostue.nl", to=[profile.user.username])
    email.content_subtype = "html"
    return email
