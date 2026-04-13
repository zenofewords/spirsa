from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("art", "0018_migrate_titles_to_labels"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="artworkthumbnail",
            name="title",
        ),
    ]
