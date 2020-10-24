# Generated by Django 3.1.2 on 2020-10-24 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spirsa', '0002_auto_20201022_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbountContactInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, help_text='Use a jpeg or png image (700x700 or larger).', null=True, upload_to='spirsa/%Y/%m/')),
                ('image_title', models.CharField(blank=True, max_length=100, null=True)),
                ('image_timestamp', models.FloatField(default=0.0)),
                ('srcsets', models.JSONField(blank=True, null=True)),
                ('contact_email', models.EmailField(blank=True, max_length=100)),
                ('top_section_title', models.CharField(blank=True, max_length=100)),
                ('top_section_text', models.TextField(blank=True, max_length=1500)),
                ('bottom_section_title', models.CharField(blank=True, max_length=100)),
                ('bottom_section_text', models.TextField(blank=True, max_length=500)),
            ],
            options={
                'verbose_name': 'About and contact page information',
                'verbose_name_plural': 'About and contact page information',
            },
        ),
    ]
