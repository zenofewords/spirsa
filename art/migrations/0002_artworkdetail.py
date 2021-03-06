# Generated by Django 3.1.2 on 2020-10-27 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('art', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtworkDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, help_text='Use a jpeg or png image (800x800 or larger).', null=True, upload_to='artwork/detail/%Y/%m/')),
                ('image_timestamp', models.IntegerField(default=0)),
                ('srcsets', models.JSONField(blank=True, null=True)),
                ('ordering', models.IntegerField(default=0, help_text='Higher number equals higher position. Leave 0 for default.')),
                ('artwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='art.artwork')),
            ],
            options={
                'verbose_name': 'Artwork detail',
                'verbose_name_plural': 'Artwork details',
                'ordering': ('-ordering', '-created_at'),
            },
        ),
    ]
