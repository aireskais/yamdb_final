# Generated by Django 2.2.16 on 2021-10-20 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0037_rolechoices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
