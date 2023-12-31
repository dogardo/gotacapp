# Generated by Django 4.1.2 on 2023-09-08 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='hashtags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('pic', models.ImageField(blank=True, null=True, upload_to='uploads/hashtags/', verbose_name='pic')),
            ],
        ),
        migrations.CreateModel(
            name='places',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=30, verbose_name='place')),
                ('pic', models.ImageField(blank=True, null=True, upload_to='uploads/places/', verbose_name='pic')),
            ],
        ),
        migrations.CreateModel(
            name='activities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='title')),
                ('description', models.CharField(max_length=1000, verbose_name='description')),
                ('m_time', models.DateTimeField()),
                ('activity', models.CharField(max_length=50, verbose_name='activity')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('hashtag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.places', verbose_name='area')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.hashtags', verbose_name='hashtags')),
            ],
        ),
    ]
