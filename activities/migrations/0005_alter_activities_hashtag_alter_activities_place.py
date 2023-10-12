# Generated by Django 4.1.2 on 2023-09-10 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_activities_community'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='hashtag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.hashtags', verbose_name='hashtags'),
        ),
        migrations.AlterField(
            model_name='activities',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.places', verbose_name='area'),
        ),
    ]
