# Generated by Django 3.1.3 on 2020-11-09 22:19

from django.db import migrations, models
import spirsa.utils


class Migration(migrations.Migration):

    dependencies = [
        ('spirsa', '0004_auto_20201103_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutcontactinformation',
            name='image',
            field=models.ImageField(blank=True, help_text='Use a jpeg or png image (760x760 or larger).', null=True, upload_to=spirsa.utils.get_contact_image_path),
        ),
    ]
