# Generated by Django 5.0.4 on 2024-05-16 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_app', '0016_remove_usersmodel_conversion_limit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plans',
            name='conversion_limit',
            field=models.IntegerField(default=5),
        ),
    ]