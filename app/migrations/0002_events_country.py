# Generated by Django 3.2.8 on 2021-10-22 06:28

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=746, multiple=True),
        ),
    ]
