from celery import shared_task

from apps.async_requests.factory import Factory


@shared_task
def execute_async_requests():
    Factory.get_executor().execute()
