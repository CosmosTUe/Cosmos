from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0017_auto_20211208_1848"),
    ]

    operations = [
        migrations.AddField(
            model_name="committee",
            name="hidden",
            field=models.BooleanField(
                default=False,
                help_text="Hide from the committees overview. The page stays reachable through its link.",
            ),
        ),
    ]
