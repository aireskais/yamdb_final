# Generated by Django 2.2.16 on 2021-10-17 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0025_merge_20211017_0757'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('title', 'author')},
        ),
    ]