# Generated by Django 5.0.7 on 2024-09-23 07:48

import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serve', '0003_alter_reservationrequest_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservationrequest',
            name='schedule',
        ),
        migrations.AlterModelOptions(
            name='place',
            options={'verbose_name': 'سالن', 'verbose_name_plural': 'سالن ها'},
        ),
        migrations.AlterModelOptions(
            name='reservationrequest',
            options={'verbose_name': 'درخواست رزرو', 'verbose_name_plural': 'درخواست های رزرو'},
        ),
        migrations.AddField(
            model_name='reservationrequest',
            name='request_date',
            field=django_jalali.db.models.jDateField(default=None, verbose_name='تاریخ درخواستی برای رزرو'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservationrequest',
            name='time_in',
            field=models.TimeField(default=None, verbose_name='ساعت شروع'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservationrequest',
            name='time_out',
            field=models.TimeField(default=None, verbose_name='ساعت پایان'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
    ]
