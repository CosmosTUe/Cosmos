from apps.async_requests.sendgrid.newsletter import NewsletterService
from apps.async_requests.sendgrid.sendgrid import SendgridService
from cosmos import settings
from mocks.newsletter import NewsletterServiceMock


def get_newsletter_service() -> NewsletterService:
    return NewsletterServiceMock() if settings.TESTING else SendgridService()
