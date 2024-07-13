# Generated by Django 5.0.4 on 2024-05-12 04:56

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_app', '0005_remove_usersmodel_subscription_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payments',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='payments',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='payments',
            name='start_date',
        ),
        migrations.AddField(
            model_name='plans',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='plans',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='plans',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='plans',
            name='payment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdf_app.payments'),
        ),
        migrations.AddField(
            model_name='plans',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdf_app.usersmodel'),
        ),
        migrations.AddField(
            model_name='usersmodel',
            name='plan',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdf_app.plans'),
        ),
        migrations.AlterField(
            model_name='plans',
            name='plan_name',
            field=models.CharField(default='Free', max_length=100),
        ),
    ]