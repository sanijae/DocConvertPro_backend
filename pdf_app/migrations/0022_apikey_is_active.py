# Generated by Django 5.0.4 on 2024-05-16 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_app', '0021_rename_created_apikey_date_created_apikey_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
