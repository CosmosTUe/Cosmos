from apps.async_requests.executor import _Executor
from apps.async_requests.sendgrid.newsletter import NewsletterService
from apps.async_requests.sendgrid.service import SendgridService
from cosmos import settings
from mocks.newsletter import NewsletterServiceMock


class Factory:
    _executor_instance = None
    _newsletter_instance = None

    @staticmethod
    def get_newsletter_service(force_clear=False) -> NewsletterService:
        if Factory._newsletter_instance is None:
            Factory._newsletter_instance = NewsletterServiceMock() if settings.TESTING else SendgridService()
        if force_clear and settings.TESTING:
            Factory._newsletter_instance.db.clear()
            Factory._newsletter_instance.outbox.clear()
        return Factory._newsletter_instance

    @staticmethod
    def get_executor():
        if Factory._executor_instance is None:
            Factory._executor_instance = _Executor()
        return Factory._executor_instance
