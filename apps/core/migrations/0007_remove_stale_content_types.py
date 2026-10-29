from django.db import migrations

# Content types (and with them their permissions) left behind by apps and models the site no
# longer has: the old django CMS setup, its Bootstrap 4 plugins, filer, Celery, easy_thumbnails,
# the "legacy" mirror of the 2019 database, and the models' old "cosmos" app name.
# Runs after 0006, which gave everyone holding an old cosmos.* permission the current one.
# Admin history entries that point at these types are kept; Django clears their type link.
STALE_APPS = {
    "async_requests",
    "bootstrap4_alerts",
    "bootstrap4_badge",
    "bootstrap4_card",
    "bootstrap4_carousel",
    "bootstrap4_collapse",
    "bootstrap4_content",
    "bootstrap4_grid",
    "bootstrap4_jumbotron",
    "bootstrap4_link",
    "bootstrap4_listgroup",
    "bootstrap4_media",
    "bootstrap4_picture",
    "bootstrap4_tabs",
    "bootstrap4_utilities",
    "cms",
    "cms_plugins",
    "cosmos",
    "cosmos_cms",
    "django_celery_beat",
    "django_celery_results",
    "djangocms_file",
    "djangocms_googlemap",
    "djangocms_icon",
    "djangocms_link",
    "djangocms_picture",
    "djangocms_snippet",
    "djangocms_style",
    "djangocms_text_ckeditor",
    "djangocms_video",
    "easy_thumbnails",
    "filer",
    "legacy",
    "menus",
}
# Models that are gone from apps that are still installed.
STALE_MODELS = {("corsheaders", "corsmodel"), ("users", "groupmember")}


def remove_stale_content_types(apps, schema_editor):
    content_type_model = apps.get_model("contenttypes", "ContentType")
    content_type_model.objects.filter(app_label__in=STALE_APPS).delete()
    for app_label, model in STALE_MODELS:
        content_type_model.objects.filter(app_label=app_label, model=model).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("admin", "0003_logentry_add_action_flag_choices"),
        ("core", "0006_copy_old_cosmos_permissions"),
    ]

    # The deleted rows describe models that no longer exist; nothing to put back.
    operations = [migrations.RunPython(remove_stale_content_types, migrations.RunPython.noop)]
