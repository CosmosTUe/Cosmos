"""
COSMOS uses SendGrid to handle newsletters.

NOTE:
Use the API documentation linked below.
The one linked in `sendgrid/sendgrid-python` is for legacy and not to be used.

References:
https://github.com/sendgrid/sendgrid-python
https://github.com/sendgrid/python-http-client
https://sendgrid.api-docs.io/v3.0/how-to-use-the-sendgrid-v3-api/api-authentication
"""
import json

import sendgrid

from apps.users.models.user.profile import state_prefix, Profile
from cosmos import settings

sg = sendgrid.SendGridAPIClient(api_key=settings.EMAIL_HOST_PASSWORD)


def is_subscribed(email: str):
    # https://sendgrid.api-docs.io/v3.0/contacts/search-contacts
    response = sg.client.marketing.contacts.search.post(request_body={"query": f"email LIKE '{email}%%'"})
    data = json.loads(response.body.decode("utf-8"))
    matches = data["contact_count"]

    if matches > 1:
        print("WARNING: Duplicate emails registered")

    return matches == 1


def __get_user_id(email: str):
    # https://sendgrid.api-docs.io/v3.0/contacts/search-contacts
    response = sg.client.marketing.contacts.search.post(request_body={"query": f"email LIKE '{email}'"})
    data = json.loads(response.body.decode("utf-8"))
    if data["contact_count"] == 0:
        return None

    if data["contact_count"] > 1:
        print("WARNING: Duplicate emails registered")

    # assumes user is first on the list
    return data["result"][0]["id"]


def add_subscription(email: str, first_name: str, last_name: str):
    # https://sendgrid.api-docs.io/v3.0/contacts/add-or-update-a-contact
    response = sg.client.marketing.contacts.put(
        request_body={
            "contacts": [
                {
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                }
            ]
        }
    )

    # return whether removal was successful
    return response.status_code == 202


def remove_subscription(email: str):
    # https://sendgrid.api-docs.io/v3.0/contacts/delete-contacts
    response = sg.client.marketing.contacts.delete(query_params={"ids": __get_user_id(email)})
    # return whether removal was successful
    return response.status_code == 202


def update_newsletter_preferences(profile: Profile):
    # Subscribe user to newsletter when consented

    # extract attributes
    old_is_sub = getattr(profile, f"{state_prefix}subscribed_newsletter")
    old_recipient = getattr(profile, f"{state_prefix}newsletter_recipient")

    is_sub = getattr(profile, "subscribed_newsletter")
    recipient = getattr(profile, "newsletter_recipient")

    # skip if no changes detected
    if old_is_sub == is_sub and old_recipient == recipient:
        return

    # handle old email first
    if old_is_sub:
        # unsubscribe old email
        if old_recipient == "TUE":
            remove_subscription(profile.user.email)
        else:
            remove_subscription(profile.user.username)

    # handle new email next
    if is_sub:
        # subscribe new email
        if old_recipient == "TUE":
            add_subscription(profile.user.email)
        else:
            add_subscription(profile.user.username)
