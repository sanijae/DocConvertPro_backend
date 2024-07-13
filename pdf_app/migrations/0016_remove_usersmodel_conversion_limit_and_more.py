# Generated by Django 5.0.4 on 2024-05-16 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_app', '0015_remove_plans_conversion_limit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersmodel',
            name='conversion_limit',
        ),
        migrations.AddField(
            model_name='plans',
            name='conversion_limit',
            field=models.IntegerField(default=0),
        ),
    ]
