# Generated by Django 3.1.2 on 2020-10-25 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
        migrations.CreateModel(
            name='MetaInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('meta_title', models.CharField(max_length=100)),
                ('meta_description', models.TextField(max_length=500)),
                ('meta_keywords', models.TextField(help_text='Separate each keyword group with a comma.', max_length=200)),
                ('meta_image', models.ImageField(blank=True, help_text='Use a jpeg or png image (1200x630 or larger).', null=True, upload_to='spirsa/%Y/%m/')),
                ('meta_image_title', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Meta information',
                'verbose_name_plural': 'Meta information',
            },
        ),
    ]
