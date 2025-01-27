# Generated by Django 5.0.4 on 2024-05-12 09:13

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_app', '0006_remove_payments_end_date_remove_payments_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='plans',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
