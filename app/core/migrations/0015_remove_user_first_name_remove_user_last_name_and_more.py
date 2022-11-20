# Generated by Django 4.1.3 on 2022-11-20 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_follower'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]