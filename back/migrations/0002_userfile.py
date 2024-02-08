# Generated by Django 3.2.7 on 2024-02-07 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('file_name', models.CharField(max_length=255)),
                ('file_type', models.CharField(max_length=100)),
                ('file_size', models.PositiveIntegerField()),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('folder_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
