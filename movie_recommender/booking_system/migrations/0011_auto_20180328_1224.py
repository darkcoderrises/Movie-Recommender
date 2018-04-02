# Generated by Django 2.0.3 on 2018-03-28 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0010_auto_20180327_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_id', models.CharField(max_length=3)),
                ('col_id', models.CharField(max_length=5)),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking_system.Screen')),
            ],
        ),
        migrations.RemoveField(
            model_name='crewprofile',
            name='role',
        ),
        migrations.AlterField(
            model_name='movie',
            name='crew',
            field=models.ManyToManyField(to='booking_system.Crew'),
        ),
        migrations.AddField(
            model_name='crew',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking_system.CrewProfile'),
        ),
        migrations.AddField(
            model_name='crew',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking_system.CastType'),
        ),
        migrations.AlterUniqueTogether(
            name='crew',
            unique_together={('profile', 'role')},
        ),
    ]
