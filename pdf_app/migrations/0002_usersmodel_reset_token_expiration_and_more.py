# Generated by Django 5.0.4 on 2024-05-09 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersmodel',
            name='reset_token_expiration',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usersmodel',
            name='password_reset_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]