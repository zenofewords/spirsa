# Generated by Django 3.1.2 on 2020-10-29 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('art', '0003_auto_20201029_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='image_timestamp',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='artworkdetail',
            name='image_timestamp',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='artworkdetail',
            name='title',
            field=models.CharField(max_length=100, verbose_name='image title'),
        ),
    ]
