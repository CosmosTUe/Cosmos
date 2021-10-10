from apps.async_requests.sendgrid.newsletter import NewsletterService


class NewsletterServiceMock(NewsletterService):
    def __init__(self):
        self.db = set()
        self.outbox = list()

    def is_subscribed(self, email: str):
        return email in self.db

    # contacts is a list of dictionaries which contain an email, first_name and last_name
    def add_subscription(self, contacts):
        for contact in contacts:
            self.db.add(contact["email"])
        return True

    # emails is a a list of emails
    def remove_subscription(self, emails):
        for email in emails:
            try:
                self.db.remove(email)
            except KeyError:
                pass
        return True

    def send_mail(self, email):
        self.outbox.append(email)
        return True
