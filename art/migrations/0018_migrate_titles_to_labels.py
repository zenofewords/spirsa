from django.db import migrations


def migrate_titles_to_labels(apps, schema_editor):
    ArtworkThumbnail = apps.get_model("art", "ArtworkThumbnail")
    Label = apps.get_model("art", "Label")

    titles = ArtworkThumbnail.objects.values_list("title", flat=True).distinct()
    for title in titles:
        if title:
            label, _ = Label.objects.get_or_create(name=title)
            ArtworkThumbnail.objects.filter(title=title).update(label=label)


class Migration(migrations.Migration):

    dependencies = [
        ("art", "0017_label_artworkthumbnail_label"),
    ]

    operations = [
        migrations.RunPython(migrate_titles_to_labels, migrations.RunPython.noop),
    ]
