# Generated by Django 4.1.2 on 2023-09-10 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_alter_activities_hashtag_alter_activities_place'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activities',
            old_name='community',
            new_name='communitys',
        ),
        migrations.RenameField(
            model_name='activities',
            old_name='place',
            new_name='places',
        ),
    ]