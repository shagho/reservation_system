# Generated by Django 4.2.16 on 2024-09-25 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serve', '0006_alter_reservationrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationrequest',
            name='status',
            field=models.CharField(choices=[('accepted', 'پذیرش'), ('pending', 'در حال بررسی'), ('not accept', 'رد'), ('cancel', 'لغو شده')], max_length=16, verbose_name='وضعیت'),
        ),
    ]
