# Generated by Django 5.0.7 on 2024-08-21 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serve', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='image',
            field=models.ImageField(default=None, upload_to=''),
            preserve_default=False,
        ),
    ]
