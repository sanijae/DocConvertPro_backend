# Generated migration to make username nullable

from django.db import migrations, models
import django.contrib.auth.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(
                error_messages={'unique': 'A user with that username already exists.'},
                help_text='Optional. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                max_length=150,
                unique=True,
                null=True,
                blank=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name='username'
            ),
        ),
    ]
