# Generated by Django 4.1.2 on 2022-10-14 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_rename_comment_usercomment_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='updated',
            field=models.BooleanField(default=False),
        ),
    ]
