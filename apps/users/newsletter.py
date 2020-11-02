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

from apps.users.models import Profile
from cosmos import settings

sg = sendgrid.SendGridAPIClient(api_key=settings.EMAIL_HOST_PASSWORD)


# TODO consider removing from newsletter list, not from contacts
def __get_list_id(list_name):
    # https://sendgrid.api-docs.io/v3.0/lists/get-all-lists
    response = sg.client.marketing.lists.get()
    data = json.loads(response.body.decode("utf-8"))
    return data["result"][0]["id"]


__newsletter_id = __get_list_id("Newsletter")


def is_subscribed(email):
    # https://sendgrid.api-docs.io/v3.0/contacts/search-contacts
    # TODO consider removing from newsletter list, not from contacts
    # response = sg.client.marketing.contacts.search.post(request_body={
    #     "query": f"email LIKE '{email}%%' AND CONTAINS(list_ids, '{__newsletter_id}')"})
    response = sg.client.marketing.contacts.search.post(request_body={"query": f"email LIKE '{email}%%'"})
    data = json.loads(response.body.decode("utf-8"))
    matches = data["contact_count"]

    if matches > 1:
        print("WARNING: Duplicate emails registered")

    return matches == 1


def __get_user_id(profile: Profile):
    # https://sendgrid.api-docs.io/v3.0/contacts/search-contacts
    response = sg.client.marketing.contacts.search.post(request_body={"query": f"email LIKE '{profile.username}'"})
    data = json.loads(response.body.decode("utf-8"))
    if data["contact_count"] == 0:
        return None

    if data["contact_count"] > 1:
        print("WARNING: Duplicate emails registered")

    # assumes user is first on the list
    return data["result"][0]["id"]


def add_subscription(profile: Profile):
    # https://sendgrid.api-docs.io/v3.0/contacts/add-or-update-a-contact
    response = sg.client.marketing.contacts.put(
        request_body={
            "contacts": [
                {"email": profile.username, "first_name": profile.user.first_name, "last_name": profile.user.last_name}
            ]
        }
    )

    # return whether removal was successful
    return response.status_code == 202


def remove_subscription(profile: Profile):
    # https://sendgrid.api-docs.io/v3.0/contacts/delete-contacts
    response = sg.client.marketing.contacts.delete(query_params={"ids": __get_user_id(profile)})
    # return whether removal was successful
    return response.status_code == 202
