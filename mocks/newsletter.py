from apps.async_requests.sendgrid.newsletter import NewsletterService


class NewsletterServiceMock(NewsletterService):
    def __init__(self):
        self.db = set()

    def is_subscribed(self, email: str):
        return email in self.db

    def add_subscription(self, email: str, first_name: str, last_name: str):
        self.db.add(email)
        return True

    def remove_subscription(self, email: str):
        try:
            self.db.remove(email)
        except KeyError:
            pass
        return True
