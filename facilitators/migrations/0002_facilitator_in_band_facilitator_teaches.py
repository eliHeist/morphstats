# Generated by Django 4.2.2 on 2023-07-12 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilitators', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilitator',
            name='in_band',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='facilitator',
            name='teaches',
            field=models.BooleanField(default=False),
        ),
    ]
