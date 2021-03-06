# Generated by Django 4.0.4 on 2022-05-16 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilitators', '0002_alter_facilitator_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrayerRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prayer_request', models.TextField()),
                ('is_answered', models.BooleanField(default=False)),
                ('facilitator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prayer_requests', to='facilitators.facilitator')),
            ],
        ),
    ]
