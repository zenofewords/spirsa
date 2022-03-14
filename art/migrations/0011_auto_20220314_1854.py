# Generated by Django 3.2.12 on 2022-03-14 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('art', '0010_artwork_is_featured'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artwork',
            options={'ordering': ('ordering', '-created_at'), 'verbose_name': 'Artwork', 'verbose_name_plural': 'Artworks'},
        ),
        migrations.AlterField(
            model_name='artwork',
            name='ordering',
            field=models.PositiveIntegerField(default=1, help_text='Ascending (smallest to largest)'),
        ),
    ]