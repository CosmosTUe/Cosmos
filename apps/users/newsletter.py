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

from cosmos import settings

sg = sendgrid.SendGridAPIClient(api_key=settings.EMAIL_HOST_PASSWORD)


def is_subscribed(email):
    # https://sendgrid.api-docs.io/v3.0/contacts/search-contacts
    response = sg.client.marketing.contacts.search.post(request_body={"query": f"email LIKE '{email}%%'"})
    data = json.loads(response.body.decode("utf-8"))
    matches = data["contact_count"]

    if matches > 1:
        print("WARNING: Duplicate emails registered")

    return matches == 1


if __name__ == "__main__":
    print(f"max is {is_subscribed('max')}")
    print(f"dng is {is_subscribed('dasyad00')}")
