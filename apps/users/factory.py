from apps.users.newsletter import NewsletterService
from apps.users.sendgrid import SendgridService
from cosmos import settings
from mocks.newsletter import NewsletterServiceMock


def get_newsletter_service() -> NewsletterService:
    return NewsletterServiceMock() if settings.TESTING else SendgridService()
