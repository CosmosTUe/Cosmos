import json
from collections import deque
from http.client import HTTPException
from typing import Dict

import sendgrid
from python_http_client import UnauthorizedError

from apps.users.newsletter import NewsletterService
from cosmos import settings


class SendgridService(NewsletterService):
    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(api_key=settings.EMAIL_HOST_PASSWORD)
        self.fail_queue = deque()

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

    def __get_user_id(self, email: str):
        # https://sendgrid.api-docs.io/v3.0/contacts/search-contacts
        response = self.sg.client.marketing.contacts.search.post(
            request_body=self.__get_sandbox_json({"query": f"email LIKE '{email}'"})
        )
        self.__process_status_code(response, 200)

        data = json.loads(response.body.decode("utf-8"))
        if data["contact_count"] == 0:
            return None

        if data["contact_count"] > 1:
            raise AssertionError(f"Duplicate emails registered for {email}")

        # assumes user is first on the list
        return data["result"][0]["id"]

    def is_subscribed(self, email: str):
        # https://sendgrid.api-docs.io/v3.0/contacts/search-contacts
        try:
            response = self.sg.client.marketing.contacts.search.post(
                request_body=self.__get_sandbox_json({"query": f"email LIKE '{email}%%'"})
            )
            self.__process_status_code(response, 200)

            data = json.loads(response.body.decode("utf-8"))
            matches = data["contact_count"]

            if matches > 1:
                raise AssertionError(f"Duplicate emails registered for {email}")

            return matches == 1
        except UnauthorizedError:
            self.fail_queue.append((self.is_subscribed, [email]))

    def add_subscription(self, email: str, first_name: str, last_name: str):
        # https://sendgrid.api-docs.io/v3.0/contacts/add-or-update-a-contact
        try:
            response = self.sg.client.marketing.contacts.put(
                request_body=self.__get_sandbox_json(
                    {
                        "list_ids": ["2ce9f995-6276-4600-81e6-27f8ae7d3e6c"],
                        "contacts": [
                            {
                                "email": email,
                                "first_name": first_name,
                                "last_name": last_name,
                            }
                        ],
                    }
                )
            )
            # return whether removal was successful
            return self.__process_status_code(response, 202)
        except UnauthorizedError:
            self.fail_queue.append((self.add_subscription, [email, first_name, last_name]))

    def remove_subscription(self, email: str):
        # https://sendgrid.api-docs.io/v3.0/contacts/delete-contacts
        try:
            response = self.sg.client.marketing.contacts.delete(
                query_params=self.__get_sandbox_json({"ids": self.__get_user_id(email)})
            )
            # return whether removal was successful
            return self.__process_status_code(response, 202)
        except UnauthorizedError:
            self.fail_queue.append((self.remove_subscription, [email]))

    def retry_failed_requests(self):
        try:
            for request, args in self.fail_queue:
                request(*args)
            self.fail_queue.clear()
        except UnauthorizedError:
            pass
