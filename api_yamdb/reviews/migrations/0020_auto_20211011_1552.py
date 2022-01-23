# Generated by Django 2.2.16 on 2021-10-11 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0019_user_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, username='me'), name='not_me'),
        ),
    ]
