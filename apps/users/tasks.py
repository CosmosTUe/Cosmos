from celery import shared_task
from celery.utils.log import get_task_logger
from django.core import mail

from apps.users.mail import create_confirm_account_email
from apps.users.models import Profile

logger = get_task_logger(__name__)


@shared_task
def send_confirmation_email_task(profile_id):
    mail.send_mail(create_confirm_account_email(Profile.objects.get(id=profile_id)))
