# Generated by Django 4.2.3 on 2023-08-01 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Telegram_bot_backend', '0005_rename_user_id_usersrunningtrainingdata_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersrunningtrainingdata',
            name='user_speed',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
