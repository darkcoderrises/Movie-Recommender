# Generated by Django 2.0.3 on 2018-04-01 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0014_auto_20180329_1345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='age',
        ),
        #migrations.AddField(
        #    model_name='userprofile',
        #    name='date_of_birth',
        #    field=models.DateField(default=22, max_length=8),
        #    preserve_default=False,
        #),
    ]