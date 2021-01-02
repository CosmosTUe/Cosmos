from celery import shared_task
from celery.utils.log import get_task_logger

from apps.users.exceptions import AuthorizationException
from apps.users.factory import get_newsletter_service
from apps.users.models import Profile

logger = get_task_logger(__name__)
newsletter_service = get_newsletter_service()


@shared_task
def sync_newsletter_subscriptions_task(id_list):
    try:
        for profile_id in id_list:
            newsletter_service.update_newsletter_preferences(Profile.objects.get(id=profile_id), force=True)
    except AuthorizationException:
        logger.error("AuthorizationException: Syncing profile with newsletter backend without authorization")
