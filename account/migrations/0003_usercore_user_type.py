# Generated by Django 4.1.2 on 2023-09-08 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercore',
            name='user_type',
            field=models.IntegerField(default=2, verbose_name='user_type'),
        ),
    ]