# Generated by Django 4.0.4 on 2023-04-13 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='junior',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='senior',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
