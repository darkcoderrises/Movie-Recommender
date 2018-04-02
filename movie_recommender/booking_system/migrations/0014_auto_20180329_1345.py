# Generated by Django 2.0.3 on 2018-03-29 13:45

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('booking_system', '0013_auto_20180329_1138'),
    ]

    operations = [
        migrations.CreateModel(
            name='TheaterOwner',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('age', models.IntegerField(default=0)),
                ('phone', models.CharField(default='', max_length=10)),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking_system.Gender')),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='theater',
            name='owner',
            field=models.ForeignKey(default=22, on_delete=django.db.models.deletion.CASCADE, to='booking_system.TheaterOwner'),
            preserve_default=False,
        ),
    ]
