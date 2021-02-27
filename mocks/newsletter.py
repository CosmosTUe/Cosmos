from apps.async_requests.sendgrid.newsletter import NewsletterService


class NewsletterServiceMock(NewsletterService):
    def __init__(self):
        self.db = set()

    def is_subscribed(self, email: str):
        return email in self.db

    def add_subscription(self, contacts):
        for contact in contacts:
            self.db.add(contact["email"])
        return True

    def remove_subscription(self, emails):
        for email in emails:
            try:
                self.db.remove(email)
            except KeyError:
                pass
        return True

    def clear_db(self):
        self.db = set()
