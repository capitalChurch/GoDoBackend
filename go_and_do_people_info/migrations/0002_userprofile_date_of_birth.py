# Generated by Django 2.2.6 on 2019-10-14 03:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('go_and_do_people_info', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
