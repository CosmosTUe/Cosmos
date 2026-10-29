from django.db import migrations

# These models used to live in an app called "cosmos", and the site's own pages kept checking
# the old "cosmos.*" permission names after the move to core and users. The pages now check the
# current names, so everyone who holds an old permission gets the matching current one as well.
USERS_MODELS = {"board", "committee", "groupmember", "profile"}


def copy_old_permissions(apps, schema_editor):
    content_type_model = apps.get_model("contenttypes", "ContentType")
    permission_model = apps.get_model("auth", "Permission")
    group_model = apps.get_model("auth", "Group")
    user_model = apps.get_model("auth", "User")

    for old in permission_model.objects.filter(content_type__app_label="cosmos").select_related("content_type"):
        groups = group_model.objects.filter(permissions=old)
        users = user_model.objects.filter(user_permissions=old)
        if not groups.exists() and not users.exists():
            continue
        model = old.content_type.model
        content_type, _ = content_type_model.objects.get_or_create(
            app_label="users" if model in USERS_MODELS else "core", model=model
        )
        new, _ = permission_model.objects.get_or_create(
            content_type=content_type, codename=old.codename, defaults={"name": old.name}
        )
        for group in groups:
            group.permissions.add(new)
        for user in users:
            user.user_permissions.add(new)


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("core", "0005_alter_news_content"),
        ("users", "0018_committee_hidden"),
    ]

    # Only adds permissions; nothing to undo.
    operations = [migrations.RunPython(copy_old_permissions, migrations.RunPython.noop)]
