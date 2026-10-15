from django.db import migrations

# The SendGrid request queue (apps.async_requests) and Celery's result and schedule apps were removed from
# INSTALLED_APPS, so their own migrations can no longer run. This drops the tables they left behind and forgets
# their migration history, so re-adding those apps later would recreate the tables from scratch.
REMOVED_APPS = ("async_requests", "django_celery_results", "django_celery_beat")
REMOVED_TABLES = (
    "async_requests_commandmodel",
    "django_celery_results_taskresult",
    "django_celery_results_chordcounter",
    "django_celery_results_groupresult",
    "django_celery_beat_periodictask",
    "django_celery_beat_periodictasks",
    "django_celery_beat_crontabschedule",
    "django_celery_beat_intervalschedule",
    "django_celery_beat_solarschedule",
    "django_celery_beat_clockedschedule",
)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_testimonial_image"),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                "DROP TABLE IF EXISTS {} CASCADE;".format(", ".join(REMOVED_TABLES)),
                ("DELETE FROM django_migrations WHERE app IN %s;", [REMOVED_APPS]),
            ],
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
