# Generated by Django 3.2.8 on 2021-10-12 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_events_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='date',
        ),
        migrations.AddField(
            model_name='events',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
