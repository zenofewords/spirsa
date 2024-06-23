# Generated by Django 4.0.6 on 2024-06-23 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('art', '0012_auto_20220611_2144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ('ordering', 'show_in_navigation'), 'verbose_name': 'Collection', 'verbose_name_plural': 'Collections'},
        ),
        migrations.AddField(
            model_name='collection',
            name='ordering',
            field=models.PositiveIntegerField(default=1, help_text='Ascending (smallest to largest)'),
        ),
        migrations.AddField(
            model_name='collection',
            name='show_in_navigation',
            field=models.BooleanField(default=False),
        ),
    ]