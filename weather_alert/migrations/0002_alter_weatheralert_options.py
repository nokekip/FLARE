# Generated by Django 5.0.6 on 2024-07-26 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather_alert', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weatheralert',
            options={'ordering': ['-created_at']},
        ),
    ]