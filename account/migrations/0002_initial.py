# Generated by Django 4.1.2 on 2023-09-08 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activities', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercore',
            name='wantToKnow',
            field=models.ManyToManyField(related_name='wanttoknow+', to='activities.hashtags', verbose_name='want to know'),
        ),
    ]
