import json
from http.client import HTTPException
from typing import Dict

import sendgrid

from apps.async_requests.sendgrid.newsletter import NewsletterService
from cosmos import settings


class SendgridService(NewsletterService):
    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(api_key=settings.EMAIL_HOST_PASSWORD)

    @staticmethod
    def __process_status_code(response, expected_status):
        if response.status_code == expected_status:
            return True
        else:
            raise HTTPException

    def __get_sandbox_json(self, request_body: Dict):
        # https://sendgrid.com/docs/for-developers/sending-email/sandbox-mode/
        if settings.DEBUG or settings.TESTING:
            request_body["mail_settings"] = {"sandbox_mode": {"enable": True}}
        return request_body

    # emails is a list of email addresses
    def __get_user_ids(self, emails):
        # https://sendgrid.api-docs.io/v3.0/contacts/search-contacts
        query = "email LIKE '" + emails.pop() + "'"
        for email in emails:
            query = query + "OR email LIKE '" + email + "'"

        response = self.sg.client.marketing.contacts.search.post(request_body=self.__get_sandbox_json({"query": query}))
        self.__process_status_code(response, 200)

        data = json.loads(response.body.decode("utf-8"))
        if data["contact_count"] == 0:
            return None

        if data["contact_count"] != len(emails):
            raise AssertionError(f"Duplicate emails registered for {email}")

        ids = []
        for user in data["result"]:
            ids.append(user["id"])
        return ids

    def is_subscribed(self, email: str):
        # https://sendgrid.api-docs.io/v3.0/contacts/search-contacts
        response = self.sg.client.marketing.contacts.search.post(
            request_body=self.__get_sandbox_json({"query": f"email LIKE '{email}%%'"})
        )
        self.__process_status_code(response)

        data = json.loads(response.body.decode("utf-8"))
        matches = data["contact_count"]

        if matches > 1:
            raise AssertionError(f"Duplicate emails registered for {email}")

        return matches == 1

    # contacts is a list of dictionaries which contain an email, first_name and last_name
    def add_subscription(self, contacts):
        # https://sendgrid.api-docs.io/v3.0/contacts/add-or-update-a-contact
        response = self.sg.client.marketing.contacts.put(
            request_body=self.__get_sandbox_json(
                {
                    "list_ids": ["2ce9f995-6276-4600-81e6-27f8ae7d3e6c"],
                    "contacts": contacts,
                }
            )
        )
        # return whether adding was successful
        return self.__process_status_code(response, 202)

    def remove_subscription(self, emails):
        # https://sendgrid.api-docs.io/v3.0/contacts/delete-contacts
        response = self.sg.client.marketing.contacts.delete(
            query_params=self.__get_sandbox_json({"ids": self.__get_user_ids(emails)})
        )
        # return whether removal was successful
        return self.__process_status_code(response, 202)

    def send_mail(self, email):
        # https://sendgrid.api-docs.io/v3.0/mail-send/v3-mail-send
        response = self.sg.send(request_body=email)
        # return whether sending the email was succesful
        return self.__process_status_code(response, 200)
