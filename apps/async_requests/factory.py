from apps.async_requests.executor import _Executor
from apps.async_requests.sendgrid.newsletter import NewsletterService
from apps.async_requests.sendgrid.sendgrid import SendgridService
from cosmos import settings
from mocks.newsletter import NewsletterServiceMock


class Factory:
    _executor_instance = None
    _newsletter_instance = None

    def get_newsletter_service() -> NewsletterService:
        if Factory._newsletter_instance is None:
            Factory._newsletter_instance = NewsletterServiceMock() if settings.TESTING else SendgridService()
        if settings.TESTING:
            Factory._newsletter_instance.db.clear()
        return Factory._newsletter_instance

    def get_executor():
        if Factory._executor_instance is None:
            Factory._executor_instance = _Executor()
        return Factory._executor_instance
