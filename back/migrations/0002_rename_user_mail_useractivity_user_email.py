# Generated by Django 3.2.7 on 2024-02-23 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useractivity',
            old_name='user_mail',
            new_name='user_email',
        ),
    ]