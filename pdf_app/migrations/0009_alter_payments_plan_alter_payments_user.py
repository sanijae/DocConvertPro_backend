# Generated by Django 5.0.4 on 2024-05-13 11:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_app', '0008_payments_ref_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='plan',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdf_app.plans'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdf_app.usersmodel'),
        ),
    ]
