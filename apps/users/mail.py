from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from sendgrid.helpers.mail import Mail

from .models import Profile
from .tokens import account_activation_token


def create_confirm_account_email(profile: Profile) -> Mail:
    mail_subject = "[Cosmos] Confirm your email address"
    message = render_to_string(
        "user/mail_confirmation.html",
        {
            "name": profile.user.first_name,
            "uid": urlsafe_base64_encode(force_bytes(profile.user.username)),
            "token": account_activation_token.make_token(profile.user),
        },
    )
    email = Mail(
        subject=mail_subject,
        html_content=message,
        from_email="noreply@cosmostue.nl",
        to_emails=profile.user.username,
        # List-Unsubscribe headers allows for easy unsubscribing from the mailing list by sending an email to
        # the specified email automatically. Is needed to not be classified as spam, and very import to handle
        # any requests correctly.
        # headers={"List-Unsubscribe": "mailto:webcom@cosmostue.nl"},
    )
    # email.content_subtype = "html"
    return email
