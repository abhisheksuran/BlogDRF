# Generated by Django 4.1.1 on 2022-09-19 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_usercomment_post_alter_userreply_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='usercomment',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='usercomment',
            name='updated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userreply',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='userreply',
            name='updated',
            field=models.BooleanField(default=False),
        ),
    ]
