# Generated by Django 3.2.13 on 2022-04-27 07:54

import django.core.validators
from django.db import migrations, models
import projectshop.main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_alter_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(max_length=25, validators=[django.core.validators.MinLengthValidator(2), projectshop.main.validators.only_letters_validator]),
        ),
    ]
