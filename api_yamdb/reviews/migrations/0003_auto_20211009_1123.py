# Generated by Django 2.2.16 on 2021-10-09 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20211009_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verification_code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]