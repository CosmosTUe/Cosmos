import json
from typing import List

import sendgrid

from apps.users.newsletter import NewsletterService
from cosmos import settings


class SendgridService(NewsletterService):
    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(api_key=settings.EMAIL_HOST_PASSWORD)

    def __get_sandbox_json(self, request_body: List):
        # https://sendgrid.com/docs/for-developers/sending-email/sandbox-mode/
        if settings.DEBUG or settings.TESTING:
            request_body["mail_settings"] = {"sandbox_mode": {"enable": True}}
        return request_body

    def __get_user_id(self, email: str):
        # https://sendgrid.api-docs.io/v3.0/contacts/search-contacts
        response = self.sg.client.marketing.contacts.search.post(
            request_body=self.__get_sandbox_json({"query": f"email LIKE '{email}'"})
        )
        data = json.loads(response.body.decode("utf-8"))
        if data["contact_count"] == 0:
            return None

        if data["contact_count"] > 1:
            raise AssertionError(f"Duplicate emails registered for {email}")

        # assumes user is first on the list
        return data["result"][0]["id"]

    def is_subscribed(self, email: str):
        # https://sendgrid.api-docs.io/v3.0/contacts/search-contacts
        response = self.sg.client.marketing.contacts.search.post(
            request_body=self.__get_sandbox_json({"query": f"email LIKE '{email}%%'"})
        )
        data = json.loads(response.body.decode("utf-8"))
        matches = data["contact_count"]

        if matches > 1:
            raise AssertionError(f"Duplicate emails registered for {email}")

        return matches == 1

    def add_subscription(self, email: str, first_name: str, last_name: str):
        # https://sendgrid.api-docs.io/v3.0/contacts/add-or-update-a-contact
        response = self.sg.client.marketing.contacts.put(
            request_body=self.__get_sandbox_json(
                {
                    "contacts": [
                        {
                            "email": email,
                            "first_name": first_name,
                            "last_name": last_name,
                        }
                    ]
                }
            )
        )

        # return whether removal was successful
        return response.status_code == 202

    def remove_subscription(self, email: str):
        # https://sendgrid.api-docs.io/v3.0/contacts/delete-contacts
        response = self.sg.client.marketing.contacts.delete(
            query_params=self.__get_sandbox_json({"ids": self.__get_user_id(email)})
        )
        # return whether removal was successful
        return response.status_code == 202
