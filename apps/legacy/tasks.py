from celery import shared_task
from celery.utils.log import get_task_logger
from django.core import mail

from apps.legacy.mail import create_legacy_account_email
from apps.legacy.models import MysiteProfile

logger = get_task_logger(__name__)


@shared_task
def send_migration_emails_task(id_list):
    """
    Given a list of legacy profile ids, creates and sends the legacy import mails for the profiles with the given ids.
    This happens asynchronously to reduce load on the webserver, and sends all emails in one batch to reduce the ammount
    of connections to the SMTP server as opening many connections can be classified as spam and result in a timeout.
    """
    emails = []
    for profile_id in id_list:
        emails.append(create_legacy_account_email(MysiteProfile.objects.get(id=profile_id)))
    connection = mail.get_connection()
    connection.send_messages(emails)
