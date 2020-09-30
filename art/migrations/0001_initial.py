# Generated by Django 3.1.1 on 2020-09-30 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, help_text='Leave empty to create from the title')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('short_description', models.TextField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='artwork/%Y/%m/')),
                ('image_timestamp', models.FloatField(default=0.0)),
                ('srcsets', models.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Artwork',
                'verbose_name_plural': 'Artworks',
                'ordering': ('created_at',),
            },
        ),
    ]
