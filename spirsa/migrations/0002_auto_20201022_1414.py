# Generated by Django 3.1.2 on 2020-10-22 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spirsa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metainformation',
            name='meta_image',
            field=models.ImageField(blank=True, help_text='Use a jpeg or png image (1200x630 or larger).', null=True, upload_to='spirsa/%Y/%m/'),
        ),
    ]