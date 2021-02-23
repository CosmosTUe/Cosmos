from celery import shared_task

from apps.async_requests.factory import get_executor


@shared_task
def execute_async_requests():
    get_executor.execute()
