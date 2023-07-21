# Generated by Django 4.2.2 on 2023-07-13 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilitators', '0003_rename_in_band_facilitator_only_in_band_and_more'),
        ('Stat', '0006_alter_service_facilitators_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='facilitators_available',
            field=models.ManyToManyField(blank=True, to='facilitators.facilitator'),
        ),
    ]
