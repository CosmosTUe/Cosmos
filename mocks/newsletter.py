from apps.async_requests.sendgrid.newsletter import NewsletterService


class NewsletterServiceMock(NewsletterService):
    def __init__(self):
        self.db = {}
        self.outbox = list()

    def is_subscribed(self, email: str, list_id: str):
        return email in self.db

    # contacts is a list of dictionaries which contain an email, first_name and last_name
    def add_subscription(self, contacts, list_id: str):
        if list_id not in self.db.keys():
            self.db[list_id] = set()
        for contact in contacts:
            self.db[list_id].add(contact["email"])
        return True

    # emails is a a list of emails
    def remove_subscription(self, emails, list_id: str):
        for email in emails:
            try:
                self.db[list_id].remove(email)
            except KeyError:
                pass
        return True

    def send_mail(self, email):
        self.outbox.append(email)
        return True
