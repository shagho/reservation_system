# Generated by Django 4.2.16 on 2024-09-28 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_company_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company_name',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='نام شرکت'),
        ),
    ]
